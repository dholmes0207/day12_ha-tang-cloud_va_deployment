# Deployment Information

## Public URL
https://day12-agent-production.up.railway.app

## Platform
Railway

## Test Commands

### Health Check
```bash
curl https://day12-agent-production.up.railway.app/health
# Expected: {"status": "ok"}
```

### API Test (with authentication)
```bash
curl -X POST https://day12-agent-production.up.railway.app/ask \
  -H "X-API-Key: super-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is AI?"}'
```

## Environment Variables Set
- PORT=8000
- REDIS_URL=redis://redis:6379/0
- AGENT_API_KEY=super-secret-key-123
- RATE_LIMIT_PER_MINUTE=10
- LOG_LEVEL=INFO

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
