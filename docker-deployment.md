# Docker Deployment Guide

How the `health-checker` image is built and shipped to Cloud Run — **local Docker** vs **web (Cloud Build)**.

## Target

| Item | Value |
|---|---|
| Artifact Registry image | `us-central1-docker.pkg.dev/project-8ea04b35-82af-4a8d-845/health-checker/health-checker:latest` |
| Cloud Run service | `health-checker` (region `us-central1`) |
| Source | `health-checker/` (Dockerfile + `projects.json` + `main.py`) |

The container bakes `projects.json` in at build time, so any change to monitored projects requires a rebuild + redeploy.

---

## Option A — Local Docker

**Prerequisites:** Docker Desktop installed **and running**, `gcloud` authenticated.

```bash
cd health-checker

# Build (linux/amd64 for Cloud Run)
docker build --platform linux/amd64 \
  -t us-central1-docker.pkg.dev/project-8ea04b35-82af-4a8d-845/health-checker/health-checker:latest .

# Push to Artifact Registry
docker push us-central1-docker.pkg.dev/project-8ea04b35-82af-4a8d-845/health-checker/health-checker:latest

# Deploy to Cloud Run
gcloud run deploy health-checker \
  --region=us-central1 \
  --image=us-central1-docker.pkg.dev/project-8ea04b35-82af-4a8d-845/health-checker/health-checker:latest \
  --project=project-8ea04b35-82af-4a8d-845
```

---

## Option B — Web (Cloud Build)

**Prerequisites:** only `gcloud` (no Docker Desktop). The `cloudbuild.yaml` at the repo root runs **build → push → deploy** on GCP-managed workers.

```bash
gcloud builds submit \
  --config=cloudbuild.yaml \
  --region=us-central1 \
  --project=project-8ea04b35-82af-4a8d-845 .
```

`cloudbuild.yaml` has three steps:

| Step | Builder | Action |
|---|---|---|
| 0 | `gcr.io/cloud-builders/docker` | `docker build` (in `health-checker/`) |
| 1 | `gcr.io/cloud-builders/docker` | `docker push` to Artifact Registry |
| 2 | `gcr.io/google.com/cloudsdktool/cloud-sdk` | `gcloud run deploy health-checker` |

---

## Local vs Web — Comparison

| | Local Docker | Web (Cloud Build) |
|---|---|---|
| **Build environment** | Your machine (Docker Desktop) | GCP-managed worker (us-central1) |
| **Prerequisites** | Docker Desktop + daemon running | `gcloud` only |
| **Speed** | Fast (local layer cache) | ~2–5 min (cold start, but AR caches layers) |
| **Cost** | Free | Free (120 build-min/day tier) |
| **Where the build runs** | Locally | Cloud (works from any machine / CI) |
| **CI/CD reuse** | Manual | `cloudbuild.yaml` is commit-able → wire to a Cloud Build trigger or GitHub |
| **Permissions** | Your `gcloud` account (owner) | Build SA needs `run.admin` + `iam.serviceAccountUser` + `artifactregistry.writer` |
| **Best for** | Quick one-off deploys on your dev box | Automated, reproducible, no local Docker dependency |

Both paths are **$0** under GCP free tier (see `project-techcloudup.md` → Build Checklist).

---

## Required IAM (web deploy)

The Cloud Build worker authenticates as the project's build service account. In this project that is the legacy compute SA (`289767126530-compute@developer.gserviceaccount.com`), which needs:

```bash
SA="serviceAccount:289767126530-compute@developer.gserviceaccount.com"

gcloud projects add-iam-policy-binding project-8ea04b35-82af-4a8d-845 \
  --member="$SA" --role="roles/run.admin"              # deploy Cloud Run
gcloud projects add-iam-policy-binding project-8ea04b35-82af-4a8d-845 \
  --member="$SA" --role="roles/iam.serviceAccountUser"  # act as the runtime SA
gcloud projects add-iam-policy-binding project-8ea04b35-82af-4a8d-845 \
  --member="$SA" --role="roles/artifactregistry.writer" # push the image
```

> Symptom if missing: `ERROR: (gcloud.run.deploy) PERMISSION_DENIED: Permission 'run.services.get' denied`.

---

## Rollback

```bash
# List revisions
gcloud run revisions list --service health-checker --region us-central1

# Route 100% back to a previous revision
gcloud run services update-traffic health-checker \
  --to-revisions=<REVISION>=100 \
  --region us-central1
```
