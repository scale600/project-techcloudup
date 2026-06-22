# project.techcloudup.com

19 live project dashboards. Self-managed via Terraform + GitHub Actions on AWS/GCP/Netlify/Cloudflare.

> The meta dashboard (`project.techcloudup.com`) is built on GCP Cloud Run + Cloud Scheduler + Firestore. Project: `project-8ea04b35-82af-4a8d-845`

---

## Project List

### Core Cloud System Administration

| # | Project | Description |
|---|---|---|
| 1 | **aws.techcloudup.com** | AWS Cloud Admin hub: IAM least-privilege generator, EC2 start/stop, S3 security audit, CloudTrail/CloudWatch dashboard, LIVE/DEMO split |
| 2 | **gcp-gke.techcloudup.com** | GCP Private GKE cluster: Terraform → GKE + Cloud Armor → GitHub Actions WIF → Grafana observability + Velero DR |
| 3 | **dba-azure.techcloudup.com** | DBA/API/BI Lab: CMS Public API, Azure Function App, Azure SQL Database, Custom REST API + Power BI, Key Vault, Application Insights |
| 4 | **ai-agent.techcloudup.com** | GCP IAM Audit Agent: Google ADK 2.2 + Gemini 2.5 Flash on Vertex AI, ReAct multi-agent, Streamlit UI → Cloud Run |
| 5 | **waf.techcloudup.com** | Real-time SQLi/XSS blocking demo: Cloudflare WAF (custom rule + url_decode) → GCP VM (Nginx + Flask) |
| 6 | **ids.techcloudup.com** | Live IDS dashboard: Suricata (eve.json) → cron forwarder → n8n → Flask API → real-time alerts |
| 7 | **takedown.techcloudup.com** | Phishing domain investigator: browser form → Flask SSE → investigate.sh (DNS/WHOIS/SSL/HTTP) → real-time terminal stream + ZIP download |

### Cloud / Automation / ERP / CRM

| # | Project | Description |
|---|---|---|
| 8 | **dashboard.iviewio.com** | AWS IoT Core: MQTT/mTLS, OTA, Device Shadow, Jobs, Lambda, API Gateway, DynamoDB, CloudFront, ISO 21434 |
| 9 | **n8n.techcloudup.com** | Self-hosted n8n automation on GCP: Groq Llama, Tavily, Google Sheets trigger → auto-publishes to 9 WordPress sites |
| 10 | **techcloudup.com** | Cloud technology blog: AI-driven automated post WordPress, Nginx, PHP-FPM, GCP, Cloudflare CDN |
| 11 | **erp.iviewio.com** | ERP on GCP: ERPNext (Frappe), Debian, MariaDB, Redis, Node.js, Nginx, Supervisor, Let's Encrypt SSL |
| 12 | **crm.iviewio.com** | CRM on GCP: EspoCRM, Ubuntu, MariaDB, PHP, Nginx, Let's Encrypt SSL |
| 13 | **emailm.iviewio.com** | Listmonk mailing service on GCP: Docker Compose, PostgreSQL 17, 2GB swap |
| 14 | **sns.iviewio.com** | Mixpost Lite on GCP: Docker Compose (Traefik + MySQL + Redis), HTTPS |
| 15 | **monica.iviewio.com** | Self-hosted Monica PRM on GCP: Docker, MariaDB, Caddy, Let's Encrypt TLS |

### Web, IoT, AI

| # | Project | Description |
|---|---|---|
| 16 | **kiosk1.iviewio.com/kiosk** | IoT Kiosk web server: GCP, Blazor Server, MudBlazor UI, Caddy TLS |
| 17 | **ai.kiosk1.iviewio.com** | Zero-cost Edge AI (object detection in browser): Netlify, Transformers.js, DETR ONNX, WebGPU/WASM |
| 18 | **ai.kbeathub.com** | Edge AI-powered K-Drama recommendation engine: Streamlit, Groq API (llama), GCP |
| 19 | **hanrecipe.kbeathub.com** | Mobile WebApp - Recipe app with authentication: Flutter, Firebase (Firestore), Riverpod, Google Auth |

---

## Dashboard Concepts

Each project site is an **operational dashboard that visualizes real-time data and enables direct control**. Not a demo page — they run live on actual infrastructure.

### Admin Dashboard

Web-based audit and control console for AWS/GCP/Azure resources.

| Dashboard | Displays | Capabilities |
|---|---|---|
| **aws.techcloudup.com** | EC2 instance status, S3 bucket security, CloudTrail logs, CloudWatch metrics | Generate IAM least-privilege policies, schedule EC2 start/stop, run security audits |
| **gcp-gke.techcloudup.com** | GKE cluster status, node pools, pod resource usage | Provision via Terraform, observe via Grafana dashboards, backup/restore via Velero |
| **dba-azure.techcloudup.com** | Azure SQL query performance, Function App execution logs, Key Vault secret status | Call REST APIs, analyze business metrics via Power BI dashboards |

### Security Dashboard

Real-time detection, blocking, and investigation of network threats.

| Dashboard | Detection Target | Response Method |
|---|---|---|
| **ids.techcloudup.com** | Suricata IDS detects real-time network intrusion attempts (eve.json streaming) | Auto-classification via n8n workflow → real-time alerts on Flask dashboard |
| **waf.techcloudup.com** | Cloudflare WAF blocks SQLi/XSS attacks in real time | Custom rules + url_decode filters bypass attacks, log visualization |
| **takedown.techcloudup.com** | Full investigation of phishing domain DNS/WHOIS/SSL records | Enter domain in browser → real-time terminal-style streaming results + ZIP report download |

### AI Agent Dashboard

Intelligent dashboards where AI agents automate cloud operations.

| Dashboard | AI Model | Automation Target |
|---|---|---|
| **ai-agent.techcloudup.com** | Gemini 2.5 Flash (Vertex AI), Google ADK 2.2 ReAct Multi-Agent | GCP IAM permission audit → Supervisor agent distributes work to sub-agents → view results via Streamlit UI |
| **n8n.techcloudup.com** | Groq Llama, Tavily Search API | Detect Google Sheets updates → AI content generation → auto-publish to 9 WordPress sites |

### IoT Dashboard

Monitoring console for hardware device connectivity, status, and OTA updates.

| Dashboard | Connectivity | Monitoring Target |
|---|---|---|
| **dashboard.iviewio.com** | AWS IoT Core (MQTT/mTLS) | Device shadows, OTA firmware updates, IoT Jobs execution, DynamoDB state storage, ISO 21434 security logging |

### Application Dashboard

Self-hosted production-ready applications (ERP, CRM, blog, etc.)

| Dashboard | Platform | Infrastructure |
|---|---|---|
| **erp.iviewio.com** | ERPNext (Frappe) | GCP + Debian + MariaDB + Redis + Nginx |
| **crm.iviewio.com** | EspoCRM | GCP + Ubuntu + MariaDB + PHP + Nginx |
| **techcloudup.com** | AI auto-publishing blog | GCP + WordPress + Nginx + PHP-FPM + Cloudflare CDN |
| **monica.iviewio.com** | Monica PRM (Personal Relationship Manager) | GCP + Docker + MariaDB + Caddy |
| **sns.iviewio.com** | Mixpost Lite (Social Scheduler) | GCP + Docker (Traefik + MySQL + Redis) |
| **emailm.iviewio.com** | Listmonk (Mailing Service) | GCP + Docker Compose + PostgreSQL 17 |
| **kiosk1.iviewio.com** | IoT Kiosk Web Server | GCP + Blazor Server + MudBlazor UI |
| **ai.kiosk1.iviewio.com** | Edge AI Object Detection | Netlify + Transformers.js + DETR ONNX + WebGPU/WASM |
| **ai.kbeathub.com** | AI Drama Recommendation Engine | GCP + Streamlit + Groq API (llama) |
| **hanrecipe.kbeathub.com** | Recipe Mobile WebApp | Flutter + Firebase (Firestore + Auth) + Riverpod |

---

## Build Checklist

GCP Cloud Run + Cloud Scheduler + Firestore, conditionally $0/month. Dashboard integrated at Cloud Run `/`.

| GCP Service | Free Quota | Dashboard Usage | Overage Risk |
|---|---|---|---|
| Cloud Run | 2M req/month | ~8,640 req/month | None |
| Cloud Scheduler | 3 jobs free | 1 job | None |
| Firestore | 50K read + 20K write/day | ~288 writes/day, ~1,000 reads/day | None |
| Artifact Registry | 0.5GB storage | ~150MB | None |

### Phase 0 — GCP Project Setup

| # | Task | Status |
|---|---|---|
| 0.1 | `gcloud config set project project-8ea04b35-82af-4a8d-845` | ✅ |
| 0.2 | Billing account linked (free tier activation) → `billingAccounts/0106B7-472D16-5AF0B7` | ✅ |
| 0.3 | Cloud Run API, Cloud Scheduler API, Cloud Build API, Firestore API enabled | ✅ |
| 0.4 | Firestore DB created → `nam5`, Native mode, free tier | ✅ |

### Phase 1 — Health Endpoints (per project)

> Check results: 11 responding (9 OK + 2 auth-gated), 8 missing (404)

| # | Task | Status |
|---|---|---|
| 1.1 | `aws.techcloudup.com` → `/api/health` (Flask) | ❌ 404 |
| 1.2 | `gcp-gke.techcloudup.com` → `/api/health` (Flask) | ✅ 200 |
| 1.3 | `dba-azure.techcloudup.com` → `/api/health` (Azure Function) | ❌ 404 |
| 1.4 | `ai-agent.techcloudup.com` → `/api/health` (Streamlit) | ✅ 200 |
| 1.5 | `waf.techcloudup.com` → `/api/health` (Flask) | ❌ 404 |
| 1.6 | `ids.techcloudup.com` → `/api/health` (Flask) | ❌ 404 |
| 1.7 | `takedown.techcloudup.com` → `/api/health` (Flask) | ❌ 404 |
| 1.8 | `dashboard.iviewio.com` → `/api/health` (Express/Lambda) | ❌ 404 |
| 1.9 | `n8n.techcloudup.com` → `/healthz` (n8n built-in) | ✅ 200 |
| 1.10 | `techcloudup.com` → `/wp-json/` (WordPress REST) | ✅ 200 |
| 1.11 | `erp.iviewio.com` → `/api/method/ping` (ERPNext built-in) | ✅ 200 |
| 1.12 | `crm.iviewio.com` → `/api/v1/` (EspoCRM built-in) | ✅ auth(401) |
| 1.13 | `emailm.iviewio.com` → `/api/health` (Listmonk built-in) | ✅ auth(403) |
| 1.14 | `sns.iviewio.com` → `/api/health` (Mixpost) | ❌ 404 |
| 1.15 | `monica.iviewio.com` → `/api/health` (Monica) | ❌ 404 |
| 1.16 | `kiosk1.iviewio.com` → `/health` (Blazor) | ✅ 200 |
| 1.17 | `ai.kiosk1.iviewio.com` → Netlify status (200=OK) | ✅ 200 |
| 1.18 | `ai.kbeathub.com` → `/healthz` (Streamlit) | ✅ 200 |
| 1.19 | `hanrecipe.kbeathub.com` → Firebase Hosting (200=OK) | ✅ 200 |

Response format: `{ "status": "ok", "service": "...", "timestamp": "..." }`

### Phase 2 — Health Checker (Cloud Run + Cloud Scheduler + Firestore)

| # | Task | Status |
|---|---|---|
| 2.1 | Firestore: `health-checks` collection auto-provisioned (created on doc write) | ✅ |
| 2.2 | Cloud Run service deployed: FastAPI, `GET /check-all` → polls 19 endpoints → writes to Firestore | ✅ |
| 2.3 | `GET /api/status` → reads latest status from Firestore, returns JSON | ✅ |
| 2.4 | Cloud Scheduler: every 5 min → HTTP Target → Cloud Run `/check-all` | ✅ |
| 2.5 | Cloud Run `--min-instances 0` + `--max-instances 1` + `256MiB` | ✅ |
| 2.6 | Static dashboard integrated into Cloud Run at `/` (replaces Firebase Hosting) | ✅ |

### Phase 3 — Dashboard UI (integrated into Cloud Run)

> Firebase CLI non-interactive auth failed; dashboard deployed at Cloud Run `/` path

| # | Task | Status |
|---|---|---|
| 3.1 | `index.html` — sticky toolbar + Healthy/Degraded/Down summary cards | ✅ |
| 3.2 | Category filters (All / Admin / AI / Security / IoT / Apps / Automation) | ✅ |
| 3.3 | JS `fetch('/api/status')` → 3-column grid rendering, 60s auto-refresh | ✅ |
| 3.4 | Each card: "Visit →" external link, domain name + status badge + time elapsed | ✅ |

### Phase 4 — Polish

| # | Task | Status |
|---|---|---|
| 4.1 | Project Visit links on cards + Footer GitHub link (badges TBD) | ✅ |
| 4.2 | DNS: `project.techcloudup.com` → nginx reverse proxy on wp-instance → Cloud Run | ✅ |
| 4.3 | Responsive (900px→2col, 600px→1col) + dark/light mode toggle (localStorage) | ✅ |
| 4.4 | Terraform `main.tf` + `variables.tf` + `outputs.tf` written and passed `validate` | ✅ |

### DNS Setup (4.2 — Done ✅)

Cloud Run Domain Mapping is blocked by Google OAuth siteverification scope restriction in CLI. REST API `forceOverride` created the mapping but stuck in `PermissionDenied` state.

**Workaround**: nginx reverse proxy on wp-instance VM → Cloudflare proxy integration.

**Data flow**:
```
Browser → https://project.techcloudup.com (Cloudflare proxy, SSL)
       → wp-instance :80 (34.169.66.81)
       → nginx proxy_pass https://health-checker-289767126530.us-central1.run.app
```

**nginx config**: `/etc/nginx/conf.d/project-techcloudup.conf` (written, nginx reloaded)

**Cloudflare DNS** (1 manual step remaining):
- Type: `A`, Name: `project`, Content: `34.169.66.81`, Proxy: ✅ ON (orange cloud)
- Once done, `https://project.techcloudup.com/` will be accessible

**Current access**: `https://health-checker-289767126530.us-central1.run.app/`

### Health Endpoint Guide

For the 8 projects missing `/api/health` → see `health-endpoint-guide.md`

| Project | Platform | Accessibility |
|---|---|---|
| aws.techcloudup.com | AWS (Flask) | 🔒 AWS account required |
| dba-azure.techcloudup.com | Azure Function | 🔒 Azure account required |
| waf.techcloudup.com | GCP VM (Flask) | 🔒 Other GCP project suspected |
| ids.techcloudup.com | GCP VM (Flask) | 🔒 Other GCP project suspected |
| takedown.techcloudup.com | GCP VM (Flask) | 🔒 Other GCP project suspected |
| dashboard.iviewio.com | AWS (Express/Lambda) | 🔒 AWS account required |
| sns.iviewio.com | GCP + Docker | 🔒 Other GCP project suspected |
| monica.iviewio.com | GCP + Docker | 🔒 Other GCP project suspected |

---
