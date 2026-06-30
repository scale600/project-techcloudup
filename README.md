# project.techcloudup.com

Multi-cloud production infrastructure dashboard — live health monitoring for services across AWS, GCP, and Azure.

> **Live**: [project.techcloudup.com](https://project.techcloudup.com)

---

## Architecture

```
Cloud Scheduler (every 5 min)
        │
        ▼
┌───────────────────────────┐
│   Cloud Run (FastAPI)     │
│   health-checker          │
│   ┌──────────┬──────────┐ │
│   │ /check-all│ /api/status│
│   │ (write)   │ (read)    │
│   └─────┬─────┴────┬─────┘│
└─────────┼──────────┼──────┘
          │          │
          ▼          ▼
    ┌──────────┐  ┌──────────────┐
    │ Firestore│  │ firebase.json │
    │ (health- │  │ Hosting proxy │
    │  checks) │  │ /api/** → CR  │
    └──────────┘  └──────────────┘
```

The meta dashboard itself is a health-checker that probes live project endpoints and surfaces their status in real time.

---

## Tech Stack

### Meta Dashboard (this repo)

| Layer | Technology |
|---|---|
| **Runtime** | Python 3.12, FastAPI, Uvicorn |
| **HTTP Client** | httpx (async, HTTP/2) |
| **Database** | Firestore (GCP) |
| **Scheduling** | Cloud Scheduler → `/check-all` every 5 min |
| **Hosting** | Cloud Run (serverless) + Firebase Hosting (CDN proxy) |
| **Container** | Docker, Artifact Registry |
| **IaC** | Terraform (Cloud Run v2, Artifact Registry, IAM) |
| **CI/CD** | manual `gcloud run deploy` / Docker push |

### Monitored Services

| Domain | Stack |
|---|---|
| **Cloud Admin** | AWS IAM, EC2, S3, CloudTrail, CloudWatch |
| **Kubernetes** | GCP GKE, Cloud Armor, Grafana, Velero |
| **DBA/BI** | Azure SQL, Function App, Key Vault, Power BI |
| **AI Agents** | Vertex AI (Gemini 2.5 Flash), Google ADK 2.2, Streamlit |
| **WAF** | Cloudflare (custom rules + url_decode), Nginx, Flask |
| **IDS** | Suricata (eve.json), n8n automation, Flask |
| **Phishing** | Flask SSE, investigate.sh (DNS/WHOIS/SSL/HTTP) |
| **IoT** | AWS IoT Core (MQTT/mTLS, Device Shadow, OTA, Lambda, DynamoDB) |
| **Edge AI** | Transformers.js, DETR ONNX, WebGPU/WASM, Groq API |
| **ERP/CRM** | ERPNext (Frappe), EspoCRM, MariaDB, Redis |
| **Mail/Social** | Listmonk (PostgreSQL 17), Mixpost (Traefik, MySQL, Redis) |
| **PRM** | Monica (Docker, Caddy) |
| **Mobile** | Flutter, Firebase (Firestore, Auth), Riverpod |
| **Blog** | WordPress (AI auto-publishing), Nginx, PHP-FPM |

---

## Project Structure

```
health-checker/
├── main.py              # FastAPI app (health probe + API + static serve)
├── projects.json        # Monitored endpoint definitions with categories
├── Dockerfile           # Python 3.12-slim + uvicorn
├── requirements.txt     # fastapi, uvicorn, httpx, firebase-admin
└── static/
    └── index.html       # Dashboard UI (dark/light theme, category filter)

dashboard/
└── firebase.json        # Firebase Hosting → Cloud Run proxy

terraform/
├── main.tf              # Cloud Run v2 service, Artifact Registry binding
├── variables.tf
└── outputs.tf
```

---

## Deployment

```bash
cd health-checker

# Build & push
docker build --platform linux/amd64 -t <registry>/health-checker:latest .
docker push <registry>/health-checker:latest

# Deploy
gcloud run deploy health-checker \
  --region=us-central1 \
  --image=<registry>/health-checker:latest \
  --project=<project-id>
```

The health-checker picks up `projects.json` at container start — no environment variable changes needed when adding/updating monitored endpoints.

---

## API

| Endpoint | Trigger | Description |
|---|---|---|
| `GET /check-all` | Cloud Scheduler | Probes all endpoints, writes to Firestore |
| `GET /api/status` | Dashboard UI | Reads latest status from Firestore, sorted by `order` |
| `GET /` | Browser | Static dashboard (HTML/JS) with auto-refresh every 60s |
