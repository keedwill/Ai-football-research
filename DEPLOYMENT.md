# 🚀 Render Deployment Guide

Complete guide for deploying AI Football Research System to Render.

---

## 📋 Pre-Deployment Checklist

- [ ] GitHub repository created and code pushed
- [ ] Render account created (https://render.com)
- [ ] Google Gemini API key obtained (recommended, free tier)
- [ ] Tavily API key obtained (recommended, 1,000 searches/month free)
- [ ] OpenAI API key obtained (optional, paid fallback)
- [ ] Review and test code locally

---

## 🎯 Deployment Overview

**Architecture:**

- **Backend**: Render Web Service (FastAPI + Gunicorn + Uvicorn)
- **Frontend**: Render Static Site (Vite + React)

**Deployment Order:**

1. Deploy Backend first (get the URL)
2. Deploy Frontend with Backend URL

---

## 🔧 Backend Deployment (FastAPI)

### Option 1: Using render.yaml (Recommended)

1. **Push code to GitHub** with `render.yaml` in the root

2. **Create New Blueprint in Render**
   - Go to: https://dashboard.render.com/blueprints
   - Click "New Blueprint Instance"
   - Connect your GitHub repository
   - Render will detect `render.yaml` and create both services

3. **Set Environment Variables** (in Render Dashboard)

   Go to Backend service settings → Environment:

   ```bash
   # Required
   ENVIRONMENT=production
   ALLOWED_ORIGINS=https://your-frontend-name.onrender.com

   # Recommended (free tier LLM)
   GOOGLE_API_KEY=AIza...your-gemini-key
   GEMINI_MODEL=gemini-1.5-flash-latest

   # Recommended (free tier data source)
   TAVILY_API_KEY=tvly-dev-...your-key

   # Optional (paid LLM fallback)
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

4. **Deploy**
   - Render will automatically deploy
   - Wait for build to complete (~3-5 minutes)
   - Note your backend URL: `https://aifootball-backend-xxx.onrender.com`

### Option 2: Manual Setup

1. **Create New Web Service**
   - Dashboard → New → Web Service
   - Connect GitHub repository
   - Configure:

   ```yaml
   Name: aifootball-backend
   Region: Oregon (or your choice)
   Branch: main
   Root Directory: (leave empty)
   Runtime: Python 3
   Build Command: cd backend && pip install -r requirements.txt
   Start Command: cd backend && gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   Plan: Free (or Starter for production)
   ```

2. **Advanced Settings**

   ```yaml
   Health Check Path: /health
   Auto-Deploy: Yes
   ```

3. **Environment Variables** (same as Option 1)

4. **Deploy**

---

## 🎨 Frontend Deployment (React + Vite)

### Prerequisites

- Backend URL from previous step: `https://aifootball-backend-xxx.onrender.com`

### Deployment Steps

1. **Create New Static Site**
   - Dashboard → New → Static Site
   - Connect GitHub repository
   - Configure:

   ```yaml
   Name: aifootball-frontend
   Region: Oregon (match backend)
   Branch: main
   Root Directory: (leave empty)
   Build Command: cd frontend && npm install && npm run build
   Publish Directory: frontend/dist
   Auto-Deploy: Yes
   ```

2. **Set Environment Variable**

   In Environment tab:

   ```bash
   VITE_API_URL=https://aifootball-backend-xxx.onrender.com
   ```

   ⚠️ **Important**: No trailing slash!

3. **Configure Redirects** (for SPA routing)

   In Redirects/Rewrites tab:

   ```
   Source: /*
   Destination: /index.html
   Status: 200 (Rewrite)
   ```

4. **Deploy**
   - Render will build and deploy
   - Wait for build (~2-3 minutes)
   - Your app will be live at: `https://aifootball-frontend-xxx.onrender.com`

---

## 🔐 Backend CORS Configuration

After frontend is deployed, **update backend CORS**:

1. Go to Backend service → Environment
2. Update `ALLOWED_ORIGINS`:

   ```bash
   ALLOWED_ORIGINS=https://aifootball-frontend-xxx.onrender.com,http://localhost:5173
   ```

   Note: Comma-separated, no spaces

3. Save and trigger manual deploy

---

## 🧪 Testing Deployment

### Backend Health Check

```bash
curl https://aifootball-backend-xxx.onrender.com/health
```

Expected response:

```json
{
  "status": "healthy",
  "environment": "production",
  "checks": {
    "llm": "gemini",
    "data_source": "tavily"
  }
}
```

### Backend API Test

```bash
curl -X POST https://aifootball-backend-xxx.onrender.com/api/v1/analyze-match \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze Arsenal vs Chelsea"}'
```

### Frontend Test

1. Open: `https://aifootball-frontend-xxx.onrender.com`
2. Enter query: "Analyze Arsenal vs Chelsea"
3. Click "Analyze"
4. Verify results display correctly

---

## 📊 Environment Variables Reference

### Backend Environment Variables

| Variable           | Required    | Description                        | Example                      |
| ------------------ | ----------- | ---------------------------------- | ---------------------------- |
| `ENVIRONMENT`      | Yes         | Deployment environment             | `production`                 |
| `ALLOWED_ORIGINS`  | Yes         | Frontend URLs (comma-separated)    | `https://myapp.onrender.com` |
| `GOOGLE_API_KEY`   | Recommended | Gemini API key (free tier)         | `AIza...`                    |
| `GEMINI_MODEL`     | No          | Gemini model name                  | `gemini-1.5-flash-latest`    |
| `TAVILY_API_KEY`   | Recommended | Tavily search API (1,000 free/mo) | `tvly-dev-...`               |
| `OPENAI_API_KEY`   | No          | OpenAI API key (paid fallback)     | `sk-proj-...`                |
| `LOG_LEVEL`        | No          | Logging level                      | `INFO` (default)             |

### Frontend Environment Variables

| Variable       | Required | Description          | Example                        |
| -------------- | -------- | -------------------- | ------------------------------ |
| `VITE_API_URL` | Yes      | Backend API base URL | `https://backend.onrender.com` |

---

## 🐛 Common Issues & Solutions

### Issue 1: Backend Won't Start

**Symptoms:**

- Build succeeds but service crashes
- Health check fails

**Solutions:**

1. Check logs in Render dashboard
2. Verify Python version (should be 3.11+)
3. Ensure all dependencies in `requirements.txt`
4. Check `gunicorn` is installed
5. Verify start command includes `cd backend`

**Debug command:**

```bash
cd backend && python -m app.main
```

### Issue 2: CORS Errors

**Symptoms:**

- Frontend shows "CORS policy" error in browser console
- Network requests blocked

**Solutions:**

1. Check `ALLOWED_ORIGINS` includes exact frontend URL
2. Ensure no trailing slash in frontend URL
3. Include `https://` protocol
4. Check for typos in URL
5. Wait ~1 minute after updating env vars

**Test CORS:**

```bash
curl -X OPTIONS https://backend.onrender.com/api/v1/analyze-match \
  -H "Origin: https://frontend.onrender.com" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

### Issue 3: Frontend Shows API Errors

**Symptoms:**

- "Failed to fetch" errors
- 404 or 500 errors

**Solutions:**

1. Verify `VITE_API_URL` is set correctly
2. Test backend health endpoint directly
3. Check browser Network tab for actual error
4. Ensure backend is deployed and running
5. Check API path is `/api/v1/...`

### Issue 4: Environment Variables Not Working

**Symptoms:**

- Settings not applied
- API keys not found

**Solutions:**

1. Render requires **manual deploy** after env var changes
2. In service settings → Manual Deploy → Deploy latest commit
3. Check env vars are in correct service (backend vs frontend)
4. Verify env var names match exactly (case-sensitive)

### Issue 5: Build Fails

**Backend build fails:**

```bash
# Check requirements.txt syntax
# Verify Python version compatibility
# Look for import errors in logs
```

**Frontend build fails:**

```bash
# Check package.json dependencies
# Verify Node version (18+)
# Check for TypeScript errors
# Ensure build command is correct
```

### Issue 6: Free Tier Limitations

**Render Free Tier:**

- Services spin down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month free

**Solutions:**

1. Upgrade to Starter plan ($7/month) for always-on
2. Use external uptime monitoring (cron-job.org) to keep alive
3. Warn users about cold start delay

### Issue 7: Frontend Routing Issues

**Symptoms:**

- Direct URL access shows 404
- Refresh on route breaks app

**Solutions:**

1. Add rewrite rule in Render dashboard:
   ```
   Source: /*
   Destination: /index.html
   Status: 200
   ```
2. Or use render.yaml with routes configuration (already included)

### Issue 8: Slow Backend Response

**Symptoms:**

- Requests timeout
- Long response times

**Solutions:**

1. Check OpenAI API response time
2. Increase Gunicorn workers (if on paid plan)
3. Implement caching for repeated queries
4. Monitor with Render metrics
5. Consider upgrading plan for more resources

---

## 📈 Performance Optimization

### Backend Optimization

1. **Gunicorn Workers**

   ```bash
   # Default: 2 workers
   # For paid plans, increase to: (2 x CPU cores) + 1
   --workers 4
   ```

2. **Caching** (future enhancement)
   - Redis for query results
   - In-memory cache for hot queries

3. **Database Connection Pooling** (if adding DB)
   - SQLAlchemy with connection pool
   - PostgreSQL for persistence

### Frontend Optimization

1. **Already optimized:**
   - ✅ Vite build optimizations
   - ✅ Code splitting
   - ✅ Asset compression

2. **Future enhancements:**
   - Service worker for offline support
   - Progressive Web App (PWA)
   - Image optimization

---

## 🔍 Monitoring & Logging

### Render Built-in Monitoring

1. **Metrics Dashboard**
   - CPU usage
   - Memory usage
   - Request rate
   - Response time

2. **Logs**
   - View in Render dashboard
   - Real-time streaming
   - Search and filter

### Access Logs

```bash
# Backend logs show:
- Startup messages
- Request logs (Gunicorn)
- Error traces
- Health check pings

# Frontend logs show:
- Build output
- Deploy status
- Static file serving
```

### External Monitoring (Optional)

1. **UptimeRobot** - Free uptime monitoring
2. **Sentry** - Error tracking
3. **LogRocket** - Session replay
4. **Google Analytics** - Usage analytics

---

## 🔄 CI/CD & Auto-Deploy

### Enable Auto-Deploy

1. Go to service settings
2. Enable "Auto-Deploy: Yes"
3. Every push to `main` branch triggers deploy

### Deploy on PR (Optional)

1. Enable "Pull Request Previews"
2. Each PR gets temporary preview URL
3. Test before merging to main

### Manual Deploy

```bash
# Option 1: Push to GitHub
git push origin main

# Option 2: Render Dashboard
Settings → Manual Deploy → Deploy Latest Commit

# Option 3: Render API
curl -X POST https://api.render.com/v1/services/YOUR_SERVICE_ID/deploys \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## 💰 Cost Estimation

### Free Tier

- Backend: Free (750 hours/month)
- Frontend: Free (100 GB bandwidth)
- **Total: $0/month** ✅

### Starter Plan (Recommended for Production)

- Backend Web Service: $7/month
- Frontend Static Site: Free
- **Total: $7/month**

### Professional Use

- Backend (Starter): $7/month
- Backend (Standard): $25/month (more CPU/memory)
- PostgreSQL Database: $7/month (if needed)
- Redis: $10/month (for caching)

---

## 🚀 Post-Deployment Steps

### 1. Update README.md

Add live demo link:

```markdown
## 🌐 Live Demo

- **Frontend**: https://aifootball-frontend-xxx.onrender.com
- **Backend API**: https://aifootball-backend-xxx.onrender.com
- **API Docs**: https://aifootball-backend-xxx.onrender.com/docs
```

### 2. Set Up Custom Domain (Optional)

1. Buy domain (Namecheap, Google Domains)
2. In Render: Settings → Custom Domains
3. Add CNAME record to your DNS
4. Render provides free SSL certificate

### 3. Enable Notifications

1. Settings → Notifications
2. Add email or Slack webhook
3. Get alerts for:
   - Deploy failures
   - Service down
   - High resource usage

### 4. Security Hardening

1. ✅ HTTPS enabled (automatic)
2. ✅ CORS configured
3. ✅ API keys in environment variables
4. ⚠️ Consider rate limiting (future)
5. ⚠️ Consider authentication (future)

---

## 📞 Support Resources

- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Support**: help@render.com
- **Community**: https://community.render.com

---

## ✅ Deployment Success Checklist

- [ ] Backend deployed and health check returns 200
- [ ] Frontend deployed and loads in browser
- [ ] CORS configured correctly (no console errors)
- [ ] Can submit analysis query and get results
- [ ] Gemini LLM working (check startup logs)
- [ ] Tavily search returning data
- [ ] Environment variables set correctly
- [ ] Auto-deploy enabled
- [ ] Logs accessible in Render dashboard
- [ ] README updated with live URLs
- [ ] Tested from different devices/browsers

---

## 🎉 You're Live!

Your AI Football Research System is now deployed to production!

**Next Steps:**

1. Share your live URL
2. Add to portfolio/resume
3. Monitor usage and errors
4. Iterate based on user feedback
5. Consider adding features:
   - User authentication
   - Analysis history
   - Favorite teams
   - Email notifications

**Congratulations!** 🚀⚽
