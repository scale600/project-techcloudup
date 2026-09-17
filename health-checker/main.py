import asyncio
import json
import logging
import os
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from curl_cffi.requests import AsyncSession
from curl_cffi.requests.exceptions import (
    ConnectionError,
    RequestException,
    SSLError,
    Timeout,
)
from firebase_admin import credentials, firestore, initialize_app
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Config ──────────────────────────────────────────────────────────
PROJECT_ID = os.environ["GCP_PROJECT"]  # project-8ea04b35-82af-4a8d-845
TIMEOUT = 10  # seconds per attempt
MAX_ATTEMPTS = 3  # total attempts per URL (1 try + 2 retries)
RETRY_BACKOFF_BASE = 1.0  # seconds; exponential backoff: 1s, 2s, ...
MAX_CONNECTIONS = 10  # concurrent probes
DOWN_THRESHOLD = 3  # consecutive failures before a site flips to "down"
# Impersonate a real browser's TLS fingerprint (JA3/JA4) so Cloudflare/CloudFront
# bot protection stops dropping us at the handshake.
IMPERSONATE = "chrome124"
PROJECTS_FILE = Path(__file__).parent / "projects.json"

# ── Firestore init ──────────────────────────────────────────────────
cred = credentials.ApplicationDefault()
initialize_app(cred, options={"projectId": PROJECT_ID})
db = firestore.client()
logger.info(f"Firestore initialized for project {PROJECT_ID}")

# ── FastAPI app ─────────────────────────────────────────────────────
app = FastAPI(title="Health Checker", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ── Load projects ───────────────────────────────────────────────────
_projects_cache: list[dict] | None = None


def _projects() -> list[dict]:
    global _projects_cache
    if _projects_cache is None:
        _projects_cache = json.loads(PROJECTS_FILE.read_text())
    return _projects_cache


def _classify_status(
    http_code: int | None,
    body_size: int = 0,
    error_type: str | None = None,
) -> tuple[str, str]:
    """Return (status, label)."""
    if http_code is None:
        label = f"no response ({error_type})" if error_type else "no response"
        return "down", label
    if 200 <= http_code < 300:
        return "live", f"HTTP {http_code}"
    if http_code in (401, 403):
        return "live", f"auth-gated (HTTP {http_code})"
    if http_code == 404 and body_size > 500:
        return "live", f"HTTP {http_code} (SPA)"
    if 400 <= http_code < 500:
        return "down", f"client error (HTTP {http_code})"
    return "down", f"server error (HTTP {http_code})"


def _is_success(http_code: int | None, body_size: int = 0) -> bool:
    """Whether a response means 'the site is reachable'."""
    if http_code is None:
        return False
    return (
        200 <= http_code < 300
        or http_code in (401, 403)
        or (http_code == 404 and body_size > 500)
    )


# ── Core logic ──────────────────────────────────────────────────────
async def _check_url(
    client: AsyncSession,
    url: str,
    attempts: int = MAX_ATTEMPTS,
) -> tuple[int | None, int, int, str | None]:
    """Fetch a URL with retries + exponential backoff.

    Return (status_code, elapsed_ms, body_size, error_type).
    """
    error_type: str | None = None
    last_elapsed = 0
    for attempt in range(attempts):
        t0 = time.perf_counter()
        try:
            resp = await client.get(url, timeout=TIMEOUT)
            return (
                resp.status_code,
                int((time.perf_counter() - t0) * 1000),
                len(resp.content),
                None,
            )
        except Timeout as exc:
            error_type = "timeout"
            last_elapsed = int((time.perf_counter() - t0) * 1000)
            logger.warning("attempt %d/%d timeout: %s (%s)", attempt + 1, attempts, url, exc)
        except SSLError as exc:
            error_type = "tls"
            last_elapsed = int((time.perf_counter() - t0) * 1000)
            logger.warning("attempt %d/%d tls error: %s (%s)", attempt + 1, attempts, url, exc)
        except ConnectionError as exc:
            error_type = "connect"
            last_elapsed = int((time.perf_counter() - t0) * 1000)
            logger.warning("attempt %d/%d connect error: %s (%s)", attempt + 1, attempts, url, exc)
        except RequestException as exc:
            error_type = "error"
            last_elapsed = int((time.perf_counter() - t0) * 1000)
            logger.warning("attempt %d/%d request error: %s (%r)", attempt + 1, attempts, url, exc)

        if attempt < attempts - 1:
            await asyncio.sleep(RETRY_BACKOFF_BASE * (2 ** attempt))

    return None, last_elapsed, 0, error_type


def _root_url(proj: dict) -> str:
    """Derive the root URL from the health endpoint URL."""
    try:
        parsed = urlsplit(proj["url"])
        return f"{parsed.scheme}://{parsed.netloc}/"
    except Exception:
        return proj["url"]


async def _check_one(client: AsyncSession, proj: dict) -> dict:
    ts = datetime.now(timezone.utc).isoformat()
    url = proj["url"]

    # 1. Try the health endpoint
    code, response_ms, body_size, error_type = await _check_url(client, url)
    if _is_success(code, body_size):
        status, label = _classify_status(code, body_size)
        return {"status": status, "label": label, "checked_at": ts, "response_ms": response_ms}

    # 2. Health endpoint failed — fall back to root URL
    root = _root_url(proj)
    if root != url:
        root_code, root_ms, root_body_size, _ = await _check_url(client, root)
        if _is_success(root_code, root_body_size):
            return {
                "status": "live",
                "label": "root only",
                "source": "root",
                "checked_at": ts,
                "response_ms": root_ms,
            }

    # 3. Both failed — classify the original failure
    status, label = _classify_status(code, body_size, error_type)
    return {"status": status, "label": label, "checked_at": ts, "response_ms": response_ms}


def _apply_debounce(pid: str, result: dict) -> None:
    """Debounce DOWN transitions so a transient blip doesn't flip a site to "down".

    Persists a consecutive-failure counter in Firestore; requires
    DOWN_THRESHOLD failures in a row before the status actually becomes "down".
    Recovery to "live" is instant.
    """
    doc_ref = db.collection("health-checks").document(pid)

    if result["status"] == "live":
        result["failures"] = 0
        return

    # result["status"] == "down"
    try:
        prev = doc_ref.get()
    except Exception as exc:
        logger.warning("Firestore read failed for %s during debounce: %s", pid, exc)
        result["failures"] = 1
        return

    if not prev.exists:
        # No history yet — trust the first check, start the failure counter.
        result["failures"] = 1
        return

    data = prev.to_dict() or {}
    prev_status = data.get("status", "live")
    prev_failures = data.get("failures", 0)
    failures = prev_failures + 1

    if failures >= DOWN_THRESHOLD:
        result["failures"] = failures
        # status remains "down"
    else:
        # Not yet confirmed — keep the previous status (instant recovery bias).
        result["status"] = prev_status if prev_status == "down" else "live"
        result["failures"] = failures
        result["label"] = f"{result.get('label', '')} · unconfirmed ({failures}/{DOWN_THRESHOLD})"


async def check_all() -> dict:
    projects = [p for p in _projects() if p.get("active") is not False]
    now = datetime.now(timezone.utc).isoformat()
    results: dict[str, dict] = {}

    async with AsyncSession(impersonate=IMPERSONATE, allow_redirects=True) as client:
        sem = asyncio.Semaphore(MAX_CONNECTIONS)

        async def run(proj: dict) -> tuple[dict, dict]:
            async with sem:
                return proj, await _check_one(client, proj)

        checked = await asyncio.gather(*(run(p) for p in projects))

    for proj, result in checked:
        pid = proj["id"]
        result["name"] = proj["name"]
        result["url"] = proj["url"]
        result["category"] = proj["category"]
        result["order"] = proj.get("order", 999)
        result["stars"] = proj.get("stars", 0)
        result["active"] = proj.get("active", True)

        _apply_debounce(pid, result)
        results[pid] = result

        # Write to Firestore
        try:
            doc_ref = db.collection("health-checks").document(pid)
            doc_ref.set({
                "id": pid,
                "name": proj["name"],
                "url": proj["url"],
                "category": proj["category"],
                "order": proj.get("order", 999),
                "stars": proj.get("stars", 0),
                "active": proj.get("active", True),
                **result,
            })
        except Exception as exc:
            logger.error(f"Firestore write failed for {pid}: {exc}")

    # Summary
    summary = {
        "live": sum(1 for r in results.values() if r["status"] == "live"),
        "down": sum(1 for r in results.values() if r["status"] == "down"),
    }

    return {"checked_at": now, "summary": summary, "projects": results}


# ── Routes ──────────────────────────────────────────────────────────
@app.get("/check-all")
async def route_check_all():
    """Triggered by Cloud Scheduler every 5 minutes."""
    try:
        result = await check_all()
        return result
    except Exception as e:
        logger.error(f"/check-all failed: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status")
async def route_status():
    """Read latest health from Firestore."""
    inactive_ids = {p["id"] for p in _projects() if p.get("active") is False}
    docs = db.collection("health-checks").stream()
    projects = {}
    for doc in docs:
        if doc.id not in inactive_ids:
            projects[doc.id] = doc.to_dict()

    if not projects:
        return {"checked_at": None, "summary": {"live": 0, "down": 0}, "projects": {}}

    # Attach static project metadata (e.g. description) from projects.json
    descriptions = {
        p["id"]: p.get("description")
        for p in _projects()
        if p.get("description")
    }
    for pid, desc in descriptions.items():
        if pid in projects:
            projects[pid]["description"] = desc

    live = sum(1 for p in projects.values() if p.get("status") == "live")
    down = sum(1 for p in projects.values() if p.get("status") == "down")

    # Use the most recent checked_at
    checked_at = max(
        (p.get("checked_at", "") for p in projects.values()),
        default=None,
    )

    # Sort by `order` field from projects.json
    sorted_ids = sorted(projects.keys(), key=lambda pid: (
        projects[pid].get("order", 999),
    ))

    return {
        "checked_at": checked_at,
        "summary": {"live": live, "down": down},
        "projects": {pid: projects[pid] for pid in sorted_ids},
    }


# ── Static dashboard (must be last) ──────────────────────────────────
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
