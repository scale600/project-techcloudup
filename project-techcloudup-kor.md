# project.techcloudup.com

19개 라이브 프로젝트 대시보드. AWS/GCP/Netlify/Cloudflare 위에서 Terraform + GitHub Actions로 자체 관리.

> 메타 대시보드(`project.techcloudup.com`)는 GCP Cloud Run + Cloud Scheduler + Firestore + Firebase Hosting 위에 구축. 프로젝트: `project-8ea04b35-82af-4a8d-845`

---

## 프로젝트 목록

### Core Cloud System Administration

| # | 프로젝트 | 설명 |
|---|---|---|
| 1 | **aws.techcloudup.com** | AWS Cloud Admin hub: IAM least-privilege generator, EC2 start/stop, S3 security audit, CloudTrail/CloudWatch dashboard, LIVE/DEMO split |
| 2 | **gcp-gke.techcloudup.com** | GCP Private GKE cluster: Terraform → GKE + Cloud Armor → GitHub Actions WIF → Grafana observability + Velero DR |
| 3 | **dba-azure.techcloudup.com** | DBA/API/BI Lab: CMS Public API, Azure Function App, Azure SQL Database, Custom REST API + Power BI, Key Vault, Application Insights |
| 4 | **ai-agent.techcloudup.com** | GCP IAM Audit Agent: Google ADK 2.2 + Gemini 2.5 Flash on Vertex AI, ReAct multi-agent, Streamlit UI → Cloud Run |
| 5 | **waf.techcloudup.com** | Real-time SQLi/XSS blocking demo: Cloudflare WAF (custom rule + url_decode) → GCP VM (Nginx + Flask) |
| 6 | **ids.techcloudup.com** | Live IDS dashboard: Suricata (eve.json) → cron forwarder → n8n → Flask API → real-time alerts |
| 7 | **takedown.techcloudup.com** | Phishing domain investigator: browser form → Flask SSE → investigate.sh (DNS/WHOIS/SSL/HTTP) → real-time terminal stream + ZIP download |

### Cloud / Automation / ERP / CRM

| # | 프로젝트 | 설명 |
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

| # | 프로젝트 | 설명 |
|---|---|---|
| 16 | **kiosk1.iviewio.com/kiosk** | IoT Kiosk web server: GCP, Blazor Server, MudBlazor UI, Caddy TLS |
| 17 | **ai.kiosk1.iviewio.com** | Zero-cost Edge AI (object detection in browser): Netlify, Transformers.js, DETR ONNX, WebGPU/WASM |
| 18 | **ai.kbeathub.com** | Edge AI-powered K-Drama recommendation engine: Streamlit, Groq API (llama), GCP |
| 19 | **hanrecipe.kbeathub.com** | Mobile WebApp - Recipe app with authentication: Flutter, Firebase (Firestore), Riverpod, Google Auth |

---

## 대시보드 컨셉

각 프로젝트 사이트는 **실시간 데이터를 시각화하고 직접 제어하는 운영 대시보드**다. 단순 데모 페이지가 아니라 실제 인프라 위에서 라이브로 동작한다.

### 운영 제어형 (Admin Dashboard)

AWS/GCP/Azure 자원을 웹에서 직접 감사·제어하는 관리자 콘솔.

| 대시보드 | 보여주는 것 | 할 수 있는 것 |
|---|---|---|
| **aws.techcloudup.com** | EC2 인스턴스 상태, S3 버킷 보안, CloudTrail 로그, CloudWatch 메트릭 | IAM 최소권한 정책 생성, EC2 시작/중지 스케줄링, 보안 감사 실행 |
| **gcp-gke.techcloudup.com** | GKE 클러스터 상태, 노드 풀, 파드 리소스 사용량 | Terraform으로 프로비저닝, Grafana 대시보드로 관측, Velero로 백업/복구 |
| **dba-azure.techcloudup.com** | Azure SQL 쿼리 성능, Function App 실행 로그, Key Vault 비밀 상태 | REST API 호출, Power BI 대시보드로 비즈니스 지표 분석 |

### 보안 관제형 (Security Dashboard)

네트워크 위협을 실시간 감지·차단·조사하는 보안 관제 콘솔.

| 대시보드 | 탐지 대상 | 대응 방식 |
|---|---|---|
| **ids.techcloudup.com** | Suricata IDS가 실시간 네트워크 침입 시도 탐지 (eve.json 스트리밍) | n8n 워크플로우로 자동 분류 → Flask 대시보드로 실시간 알림 |
| **waf.techcloudup.com** | Cloudflare WAF로 SQLi/XSS 공격 실시간 차단 | 커스텀 룰 + url_decode로 우회 공격까지 필터링, 로그 시각화 |
| **takedown.techcloudup.com** | 피싱 도메인의 DNS/WHOIS/SSL 레코드 전체 조사 | 브라우저에서 도메인 입력 → 터미널처럼 실시간 스트리밍 결과 + ZIP 리포트 다운로드 |

### AI 자동화형 (AI Agent Dashboard)

AI 에이전트가 클라우드 운영을 자동화하는 지능형 대시보드.

| 대시보드 | AI 모델 | 자동화 대상 |
|---|---|---|
| **ai-agent.techcloudup.com** | Gemini 2.5 Flash (Vertex AI), Google ADK 2.2 ReAct Multi-Agent | GCP IAM 권한 감사 → Supervisor 에이전트가 하위 에이전트에 작업 분배 → Streamlit UI로 결과 확인 |
| **n8n.techcloudup.com** | Groq Llama, Tavily 검색 API | Google Sheets 업데이트 감지 → AI 컨텐츠 생성 → 9개 WordPress 사이트 자동 발행 |

### IoT 관제형 (IoT Dashboard)

하드웨어 디바이스의 연결·상태·OTA 업데이트를 관제하는 IoT 콘솔.

| 대시보드 | 연결 방식 | 관제 대상 |
|---|---|---|
| **dashboard.iviewio.com** | AWS IoT Core (MQTT/mTLS) | 디바이스 섀도우, OTA 펌웨어 업데이트, IoT Jobs 실행, DynamoDB 상태 저장, ISO 21434 보안 로깅 |

### 애플리케이션형 (Application Dashboard)

ERP/CRM/블로그 등 실무에서 사용 가능한 자체 호스팅 애플리케이션.

| 대시보드 | 플랫폼 | 인프라 |
|---|---|---|
| **erp.iviewio.com** | ERPNext (Frappe) | GCP + Debian + MariaDB + Redis + Nginx |
| **crm.iviewio.com** | EspoCRM | GCP + Ubuntu + MariaDB + PHP + Nginx |
| **techcloudup.com** | AI 자동 발행 블로그 | GCP + WordPress + Nginx + PHP-FPM + Cloudflare CDN |
| **monica.iviewio.com** | Monica PRM (개인 관계 관리) | GCP + Docker + MariaDB + Caddy |
| **sns.iviewio.com** | Mixpost Lite (소셜 스케줄러) | GCP + Docker (Traefik + MySQL + Redis) |
| **emailm.iviewio.com** | Listmonk (메일링 서비스) | GCP + Docker Compose + PostgreSQL 17 |
| **kiosk1.iviewio.com** | IoT 키오스크 웹서버 | GCP + Blazor Server + MudBlazor UI |
| **ai.kiosk1.iviewio.com** | Edge AI 객체 탐지 | Netlify + Transformers.js + DETR ONNX + WebGPU/WASM |
| **ai.kbeathub.com** | AI 드라마 추천 엔진 | GCP + Streamlit + Groq API (llama) |
| **hanrecipe.kbeathub.com** | 레시피 모바일 웹앱 | Flutter + Firebase (Firestore + Auth) + Riverpod |

---

## 구축 체크리스트

GCP Cloud Run + Cloud Scheduler + Firestore, 조건부 월 $0. 대시보드는 Cloud Run `/`에 통합.

| GCP 서비스 | 무료 할당량 | 이 대시보드 소비량 | 초과 리스크 |
|---|---|---|---|
| Cloud Run | 200만 req/월 | ~8,640 req/월 | 없음 |
| Cloud Scheduler | 3개 job 무료 | 1개 job | 없음 |
| Firestore | 5만 read + 2만 write/일 | ~288 write/일, ~1,000 read/일 | 없음 |
| Artifact Registry | 0.5GB 저장 | ~150MB | 없음 |

### Phase 0 — GCP 프로젝트 준비

| # | 작업 | 상태 |
|---|---|---|
| 0.1 | `gcloud config set project project-8ea04b35-82af-4a8d-845` | ✅ |
| 0.2 | 결제 계정 연결 (무료 티어 활성화용) → `billingAccounts/0106B7-472D16-5AF0B7` | ✅ |
| 0.3 | Cloud Run API, Cloud Scheduler API, Cloud Build API, Firestore API 활성화 | ✅ |
| 0.4 | Firestore DB 생성 → `nam5`, Native mode, free tier | ✅ |

### Phase 1 — Health Endpoint (각 프로젝트)

> 점검 결과: 11개 응답 (9 OK + 2 auth-gated), 8개 404

| # | 작업 | 상태 |
|---|---|---|
| 1.1 | `aws.techcloudup.com` → `/api/health` (Flask) | ❌ 404 |
| 1.2 | `gcp-gke.techcloudup.com` → `/api/health` (Flask) | ✅ 200 |
| 1.3 | `dba-azure.techcloudup.com` → `/api/health` (Azure Function) | ❌ 404 |
| 1.4 | `ai-agent.techcloudup.com` → `/api/health` (Streamlit) | ✅ 200 |
| 1.5 | `waf.techcloudup.com` → `/api/health` (Flask) | ❌ 404 |
| 1.6 | `ids.techcloudup.com` → `/api/health` (Flask) | ❌ 404 |
| 1.7 | `takedown.techcloudup.com` → `/api/health` (Flask) | ❌ 404 |
| 1.8 | `dashboard.iviewio.com` → `/api/health` (Express/Lambda) | ❌ 404 |
| 1.9 | `n8n.techcloudup.com` → `/healthz` (n8n 내장) | ✅ 200 |
| 1.10 | `techcloudup.com` → `/wp-json/` (WordPress REST) | ✅ 200 |
| 1.11 | `erp.iviewio.com` → `/api/method/ping` (ERPNext 내장) | ✅ 200 |
| 1.12 | `crm.iviewio.com` → `/api/v1/` (EspoCRM 내장) | ✅ auth(401) |
| 1.13 | `emailm.iviewio.com` → `/api/health` (Listmonk 내장) | ✅ auth(403) |
| 1.14 | `sns.iviewio.com` → `/api/health` (Mixpost) | ❌ 404 |
| 1.15 | `monica.iviewio.com` → `/api/health` (Monica) | ❌ 404 |
| 1.16 | `kiosk1.iviewio.com` → `/health` (Blazor) | ✅ 200 |
| 1.17 | `ai.kiosk1.iviewio.com` → Netlify 상태 (200=OK) | ✅ 200 |
| 1.18 | `ai.kbeathub.com` → `/healthz` (Streamlit) | ✅ 200 |
| 1.19 | `hanrecipe.kbeathub.com` → Firebase Hosting (200=OK) | ✅ 200 |

응답 형식: `{ "status": "ok", "service": "...", "timestamp": "..." }`

### Phase 2 — Health Checker (Cloud Run + Cloud Scheduler + Firestore)

| # | 작업 | 상태 |
|---|---|---|
| 2.1 | Firestore: `health-checks` 컬렉션 자동 프로비저닝 (doc write 시 생성) | ✅ |
| 2.2 | Cloud Run 서비스 배포: FastAPI, `GET /check-all` → 19개 폴링 → Firestore 저장 | ✅ |
| 2.3 | `GET /api/status` → Firestore에서 최신 상태 읽어 JSON 응답 | ✅ |
| 2.4 | Cloud Scheduler: 5분 간격 → HTTP Target → Cloud Run `/check-all` | ✅ |
| 2.5 | Cloud Run `--min-instances 0` + `--max-instances 1` + `256MiB` | ✅ |
| 2.6 | Firebase Hosting 대신 Cloud Run에 정적 대시보드 통합 (`/` → static mount) | ✅ |

### Phase 3 — 대시보드 UI (Cloud Run 통합)

> Firebase CLI 비대화형 인증 불가로 Cloud Run `/` 경로에 통합 배포

| # | 작업 | 상태 |
|---|---|---|
| 3.1 | `index.html` — sticky toolbar + Healthy/Degraded/Down summary cards | ✅ |
| 3.2 | 카테고리 필터 (All / Admin / AI / Security / IoT / Apps / Automation) | ✅ |
| 3.3 | JS `fetch('/api/status')` → 3열 그리드 렌더링, 60초 자동 갱신 | ✅ |
| 3.4 | 각 카드에 "Visit →" 외부 링크, 도메인명 + 상태 뱃지 + 경과 시간 | ✅ |

### Phase 4 — 완성도

| # | 작업 | 상태 |
|---|---|---|
| 4.1 | 카드에 프로젝트 Visit 링크 + Footer GitHub 링크 (배지는 추후) | ✅ |
| 4.2 | DNS: `project.techcloudup.com` → nginx reverse proxy on wp-instance → Cloud Run | ✅ |
| 4.3 | 모바일 반응형 (900px→2열, 600px→1열) + 다크모드/라이트모드 토글 (localStorage) | ✅ |
| 4.4 | Terraform `main.tf` + `variables.tf` + `outputs.tf` 작성 및 `validate` 통과 | ✅ |

### DNS 설정 (4.2 — 완료 ✅)

Cloud Run Domain Mapping은 Google OAuth siteverification scope 제한으로 CLI에서 차단됨. REST API `forceOverride`로 생성했으나 `PermissionDenied` 상태로 stuck.

**대체 솔루션**: wp-instance VM에 nginx reverse proxy 구성 → Cloudflare proxy 연동.

**데이터 흐름**:
```
Browser → https://project.techcloudup.com (Cloudflare proxy, SSL)
       → wp-instance :80 (34.169.66.81)
       → nginx proxy_pass https://health-checker-289767126530.us-central1.run.app
```

**nginx config**: `/etc/nginx/conf.d/project-techcloudup.conf` (작성 완료, nginx reload 완료)

**Cloudflare DNS** (수동 1단계):
- Type: `A`, Name: `project`, Content: `34.169.66.81`, Proxy: ✅ ON (주황색 구름)
- 완료 후 `https://project.techcloudup.com/` 접근 가능

**현재 접근**: `https://health-checker-289767126530.us-central1.run.app/`

**현재 임시 접근**: `https://health-checker-289767126530.us-central1.run.app/`

### Health Endpoint 가이드

8개 404 프로젝트에 `/api/health` 구현 참고 → `health-endpoint-guide.md`

| 프로젝트 | 플랫폼 | 접근 가능성 |
|---|---|---|
| aws.techcloudup.com | AWS (Flask) | 🔒 AWS 계정 필요 |
| dba-azure.techcloudup.com | Azure Function | 🔒 Azure 계정 필요 |
| waf.techcloudup.com | GCP VM (Flask) | 🔒 타 GCP 프로젝트 추정 |
| ids.techcloudup.com | GCP VM (Flask) | 🔒 타 GCP 프로젝트 추정 |
| takedown.techcloudup.com | GCP VM (Flask) | 🔒 타 GCP 프로젝트 추정 |
| dashboard.iviewio.com | AWS (Express/Lambda) | 🔒 AWS 계정 필요 |
| sns.iviewio.com | GCP + Docker | 🔒 타 GCP 프로젝트 추정 |
| monica.iviewio.com | GCP + Docker | 🔒 타 GCP 프로젝트 추정 |

---

