# Frontend-Backend Integration Guide

## ✅ Connection Status: WORKING

Both servers are running and communicating successfully:

- **Backend**: http://localhost:8000 (FastAPI)
- **Frontend**: http://localhost:5173 (React + Vite)

---

## 🔌 How It Works

### 1. **Frontend API Client** (`src/services/api.js`)

```javascript
// Sends POST request to backend
export async function analyzeMatch(query) {
  const response = await fetch(`/api/v1/analyze-match`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  return response.json();
}
```

### 2. **Vite Proxy** (`vite.config.js`)

```javascript
// Proxies /api/* to backend (avoids CORS issues)
proxy: {
  "/api": {
    target: "http://localhost:8000",
    changeOrigin: true,
  },
}
```

### 3. **Backend CORS** (`backend/app/main.py`)

```python
# Allows frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. **API Contract** (`backend/app/models/analysis.py`)

```python
# Request
{ "query": "Analyze Arsenal vs Chelsea" }

# Response
{
  "analysis": {
    "summary": "...",
    "form": "...",
    "head_to_head": "...",
    "league_position": "...",
    "insights": "...",
    "final_verdict": "..."
  }
}
```

---

## 🧪 Test Results

All integration tests passed:

✅ **Health Check** - Backend reachable  
✅ **CORS Headers** - Proper headers set for localhost:5173  
✅ **Analyze Endpoint** - Request/response cycle works  
✅ **Error Handling** - Validation errors handled gracefully  
✅ **Full Flow** - Complete user journey works end-to-end

---

## 🚀 How to Use

### Option 1: Browser UI

1. Open http://localhost:5173
2. Enter a match query (e.g., "Arsenal vs Chelsea")
3. Click "Analyze"
4. View structured results

### Option 2: Direct API Call

```powershell
# PowerShell
$body = @{ query = "Arsenal vs Chelsea" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/analyze-match" -Method Post -Body $body -ContentType "application/json"
```

### Option 3: Run Integration Tests

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python test_frontend_integration.py
```

---

## 🔄 Complete Request Flow

```
User Input (Frontend)
    ↓
services/api.js
    ↓ fetch("/api/v1/analyze-match")
Vite Proxy (localhost:5173 → localhost:8000)
    ↓
FastAPI CORS Middleware
    ↓
app/api/routes.py (validates request)
    ↓
app/services/analysis_service.py (orchestrates)
    ↓
app/agents/football_agent.py (extracts teams, calls tools)
    ↓ ↓ ↓ ↓
tools/ (form_tool, h2h_tool, league_tool, stats_tool)
    ↓
Agent synthesizes analysis
    ↓
Response flows back through layers
    ↓
Frontend displays structured result
```

---

## 🎯 What's Working

### Loading States

- ✅ Shows spinner while fetching
- ✅ Disables input during request
- ✅ "Analyzing..." button text

### Success States

- ✅ Displays all 6 analysis sections
- ✅ Proper formatting (summary, form, h2h, league, insights, verdict)
- ✅ Color-coded sections with emojis

### Error States

- ✅ Network errors caught and displayed
- ✅ Validation errors shown to user
- ✅ Server errors handled gracefully

### User Experience

- ✅ Example queries clickable
- ✅ Auto-focus on input field
- ✅ Submit on Enter key
- ✅ Responsive design (mobile + desktop)

---

## 📊 Sample Output

**Query**: "Arsenal vs Chelsea"

**Response Structure**:

```json
{
  "analysis": {
    "summary": "Match Analysis: Arsenal vs Chelsea. Based on current form...",
    "form": "Arsenal:\nWWDWW\n...",
    "head_to_head": "Last 5 matches between Arsenal and Chelsea...",
    "league_position": "Arsenal: Position 2/20...",
    "insights": "Arsenal are in excellent form...",
    "final_verdict": "Arsenal enter this match with momentum..."
  }
}
```

---

## 🔧 Troubleshooting

### Backend Not Responding

```powershell
# Restart backend
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

### Frontend Not Loading

```powershell
# Restart frontend
cd frontend
npm run dev
```

### CORS Errors

- Check `backend/app/main.py` includes `http://localhost:5173` in `allow_origins`
- Verify Vite proxy in `frontend/vite.config.js` points to `http://localhost:8000`

---

## ✨ Summary

**Connection Type**: Proxy-based (development)  
**State Management**: React useState hooks  
**Error Handling**: Try-catch with user-friendly messages  
**Loading UX**: Spinner + disabled inputs  
**API Method**: Fetch API (native, no dependencies)  
**CORS**: Configured in FastAPI middleware

**Status**: 🟢 Fully operational
