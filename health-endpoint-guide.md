# /api/health Endpoint Implementation Guide

응답 형식: `{"status":"ok","service":"<name>","timestamp":"2026-06-22T00:00:00Z"}`

## Flask (aws, waf, ids, takedown)

```python
from datetime import datetime, timezone

@app.route('/api/health')
def health():
    return {
        "status": "ok",
        "service": "aws-admin",  # 프로젝트별 변경
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
```

배포: `sudo systemctl restart <service>` 또는 `docker compose restart`

## Docker Compose (sns / Mixpost, monica / Monica PRM)

### Option A - App-level (Mixpost는 Laravel, Monica는 Laravel)
```php
// routes/api.php
Route::get('/health', function () {
    return response()->json([
        'status' => 'ok',
        'service' => 'mixpost',
        'timestamp' => now()->toIso8601String()
    ]);
});
```

### Option B - Traefik label (sns 전용)
```yaml
# docker-compose.yml
labels:
  - "traefik.http.routers.health.rule=Host(`sns.iviewio.com`) && Path(`/api/health`)"
  - "traefik.http.routers.health.service=api@internal"
```

### Option C - Caddy reverse proxy (monica 전용)
```
# Caddyfile
sns.iviewio.com {
    handle /api/health {
        respond "{\"status\":\"ok\",\"service\":\"monica\"}" 200
    }
    reverse_proxy app:80
}
```

## Azure Function (dba-azure)
```python
import azure.functions as func
import datetime

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({
            "status": "ok",
            "service": "dba-azure",
            "timestamp": datetime.datetime.utcnow().isoformat()
        }),
        mimetype="application/json",
        status_code=200
    )
```

## AWS Lambda/Express (dashboard.iviewio.com)
```javascript
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'iot-dashboard',
    timestamp: new Date().toISOString()
  });
});
```

## GCP VM 접근 (waf, ids, takedown, sns, monica)

```bash
# SSH into VM
gcloud compute ssh <instance-name> --zone=<zone>

# Flask apps - app.py에 위 route 추가 후 restart
sudo systemctl restart nginx
sudo systemctl restart flask-app

# Docker apps - docker-compose.yml 수정 후
docker compose down && docker compose up -d
```
