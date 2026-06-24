# 🚀 Quick Deployment Reference

## Backend (Render Web Service)

**Build Command:**

```bash
cd backend && pip install -r requirements.txt
```

**Start Command:**

```bash
cd backend && gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

**Environment Variables:**

```bash
ENVIRONMENT=production
ALLOWED_ORIGINS=https://your-frontend.onrender.com
OPENAI_API_KEY=sk-proj-your-key-here
FOOTBALL_API_KEY=your-api-key
LOG_LEVEL=INFO
```

**Health Check:**

```
/health
```

---

## Frontend (Render Static Site)

**Build Command:**

```bash
cd frontend && npm install && npm run build
```

**Publish Directory:**

```
frontend/dist
```

**Environment Variables:**

```bash
VITE_API_URL=https://your-backend.onrender.com
```

**Rewrite Rule:**

```
Source: /*
Destination: /index.html
Status: 200
```

---

## Deployment Order

1. **Deploy Backend First**
   - Get backend URL: `https://backend-xxx.onrender.com`

2. **Deploy Frontend**
   - Set `VITE_API_URL` to backend URL
   - Get frontend URL: `https://frontend-xxx.onrender.com`

3. **Update Backend CORS**
   - Set `ALLOWED_ORIGINS` to frontend URL
   - Manual deploy backend

4. **Test**
   - Visit frontend URL
   - Submit analysis query
   - Verify results

---

## Testing Commands

```bash
# Test backend health
curl https://your-backend.onrender.com/health

# Test backend API
curl -X POST https://your-backend.onrender.com/api/v1/analyze-match \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze Arsenal vs Chelsea"}'

# Test frontend
open https://your-frontend.onrender.com
```

---

## Common Issues

| Issue                | Solution                              |
| -------------------- | ------------------------------------- |
| CORS errors          | Update `ALLOWED_ORIGINS` and redeploy |
| 404 errors           | Add rewrite rule `/* → /index.html`   |
| Slow first request   | Free tier cold start (30-60s)         |
| Build fails          | Check logs, verify commands           |
| Env vars not working | Manual deploy after changing          |

---

## Quick Links

- Render Dashboard: https://dashboard.render.com
- FastAPI Docs: `/docs` (on backend URL)
- Full Guide: [DEPLOYMENT.md](DEPLOYMENT.md)
