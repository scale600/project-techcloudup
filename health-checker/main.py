import json
import logging
import os
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import httpx
from firebase_admin import credentials, firestore, initialize_app
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Config ──────────────────────────────────────────────────────────
PROJECT_ID = os.environ["GCP_PROJECT"]  # project-8ea04b35-82af-4a8d-845
TIMEOUT = 10  # seconds per health check
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


def _classify_status(http_code: int | None) -> tuple[str, str]:
    """Return (status, label)."""
    if http_code is None:
        return "down", "no response"
    if 200 <= http_code < 300:
        return "live", f"HTTP {http_code}"
    if http_code in (401, 403):
        return "live", f"auth-gated (HTTP {http_code})"
    if 400 <= http_code < 500:
        return "down", f"client error (HTTP {http_code})"
    return "down", f"server error (HTTP {http_code})"


# ── Core logic ──────────────────────────────────────────────────────
async def _check_url(client: httpx.AsyncClient, url: str) -> tuple[int | None, int]:
    """Try fetching a URL. Return (status_code, elapsed_ms)."""
    t0 = time.perf_counter()
    try:
        resp = await client.get(url, timeout=TIMEOUT)
        elapsed = int((time.perf_counter() - t0) * 1000)
        return resp.status_code, elapsed
    except httpx.TimeoutException:
        return None, TIMEOUT * 1000
    except Exception:
        return None, int((time.perf_counter() - t0) * 1000)


def _root_url(proj: dict) -> str:
    """Derive the root URL from the health endpoint URL."""
    try:
        parsed = httpx.URL(proj["url"])
        return f"{parsed.scheme}://{parsed.host}/"
    except Exception:
        return proj["url"]


async def _check_one(client: httpx.AsyncClient, proj: dict) -> dict:
    ts = datetime.now(timezone.utc).isoformat()
    url = proj["url"]

    # 1. Try the health endpoint
    code, response_ms = await _check_url(client, url)
    if code is not None and (200 <= code < 300 or code in (401, 403)):
        status, label = _classify_status(code)
        return {"status": status, "label": label, "checked_at": ts, "response_ms": response_ms}

    # 2. Health endpoint failed — fall back to root URL
    root = _root_url(proj)
    if root != url:
        root_code, root_ms = await _check_url(client, root)
        if root_code is not None and (200 <= root_code < 300 or root_code in (401, 403)):
            return {
                "status": "live",
                "label": "root only",
                "source": "root",
                "checked_at": ts,
                "response_ms": root_ms,
            }

    # 3. Both failed — classify the original failure
    status, label = _classify_status(code)
    return {"status": status, "label": label, "checked_at": ts, "response_ms": response_ms}


async def check_all() -> dict:
    projects = _projects()
    results: dict[str, dict] = {}
    now = datetime.now(timezone.utc).isoformat()

    async with httpx.AsyncClient(
        verify=False,
        follow_redirects=True,
        limits=httpx.Limits(max_connections=10),
    ) as client:
        for proj in projects:
            pid = proj["id"]
            result = await _check_one(client, proj)
            result["name"] = proj["name"]
            result["url"] = proj["url"]
            result["category"] = proj["category"]
            result["order"] = proj.get("order", 999)
            result["stars"] = proj.get("stars", 0)
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
    docs = db.collection("health-checks").stream()
    projects = {}
    for doc in docs:
        projects[doc.id] = doc.to_dict()

    if not projects:
        return {"checked_at": None, "summary": {"live": 0, "down": 19}, "projects": {}}

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
