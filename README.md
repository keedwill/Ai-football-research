<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React"/>
  <img src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white" alt="Gemini"/>
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
</p>

<h1 align="center">⚽ AI Football Research System</h1>

<p align="center">
  <strong>Production-ready full-stack application for intelligent football match analysis</strong>
</p>

<p align="center">
  Powered by <strong>Gemini</strong> • <strong>Tavily</strong> • <strong>LangChain</strong> • <strong>FastAPI</strong> • <strong>React</strong>
</p>

<p align="center">
  <a href="#-features"><strong>Features</strong></a> •
  <a href="#-architecture"><strong>Architecture</strong></a> •
  <a href="#-quick-start"><strong>Quick Start</strong></a> •
  <a href="#-api-documentation"><strong>API Docs</strong></a> •
  <a href="#-tech-stack"><strong>Tech Stack</strong></a>
</p>

---

## 📖 About

**AI Football Research System** is an advanced full-stack application that leverages artificial intelligence to provide comprehensive football match analysis. The system uses a LangChain agent powered by **Google Gemini** (free tier) with OpenAI GPT-4 fallback, orchestrating a single comprehensive Tavily search for real-time football data and synthesizing intelligent insights.

### Why This Project?

This project demonstrates:

- **Clean Architecture** - Proper separation of concerns across API, service, agent, and data layers
- **AI Integration** - Real-world implementation of LLM-powered analysis with fallback strategies
- **Production Practices** - Error handling, logging, validation, environment configuration
- **Modern Stack** - FastAPI async backend, React SPA frontend, AI orchestration layer
- **Type Safety** - Pydantic models for API contracts, comprehensive type hints

---

## ✨ Features

### 🤖 **AI-Powered Analysis**

- **Multi-LLM Support**: Google Gemini (free, priority) → OpenAI GPT-4 → Ollama (local)
- **Intelligent Synthesis**: LLM analyzes comprehensive match data into tactical insights
- **Fallback Logic**: Graceful degradation when LLM unavailable
- **Context-Aware**: Analyzes form, statistics, and historical data
- **Optimized**: Single Tavily search (85% reduction in API calls)

### 📊 **Comprehensive Data**

- **Recent Form**: Last 5 match results with W/D/L patterns
- **Head-to-Head**: Historical matchups between teams
- **League Standings**: Current position, points, goal difference
- **Season Statistics**: Goals, xG, possession, clean sheets

### 🏗️ **Production Architecture**

- **Clean Separation**: API → Service → Agent → Tools layers
- **Error Handling**: Custom exception classes with proper HTTP status codes
- **Logging**: Structured logging across all components
- **Validation**: Pydantic models for request/response validation

### 🌐 **Live Data Support**

- **Tavily API**: Real-time web search for latest match data, team form, and statistics
- **Comprehensive Search**: Single query fetching form, H2H, league standings, and stats
- **Optimized Volume**: 8 results, 800 chars each, 8000 total limit for speed

### 💻 **Modern Frontend**

- **React 18**: Component-based UI with hooks
- **Responsive Design**: Works on desktop and mobile
- **Real-time Feedback**: Loading states, error handling
- **Clean UX**: Intuitive input, structured result display

---

## 🏛️ Architecture

### System Overview

```
┌───────────────────────────────────────────────────────────┐
│                React Frontend (Vite)                       │
│               http://localhost:5173                        │
│                                                            │
│  ┌─────────┐  ┌──────────┐  ┌──────────────────────┐    │
│  │ Match   │  │ Result   │  │  API Client          │    │
│  │ Input   │  │ Display  │  │  (services/api.js)   │    │
│  └─────────┘  └──────────┘  └──────────────────────┘    │
└────────────────────┬──────────────────────────────────────┘
                     │ POST /api/v1/analyze-match
                     │ { "query": "Arsenal vs Chelsea" }
                     ▼
┌───────────────────────────────────────────────────────────┐
│              FastAPI Backend (Uvicorn)                     │
│              http://localhost:8000                         │
│                                                            │
│  ┌──────────────────────────────────────────────────┐    │
│  │  API Layer (routes.py)                           │    │
│  │  • Request validation • Error handling • CORS    │    │
│  └─────────────────┬────────────────────────────────┘    │
│                    │                                       │
│  ┌─────────────────▼────────────────────────────────┐    │
│  │  Service Layer (analysis_service.py)             │    │
│  │  • Business logic orchestration                  │    │
│  └─────────────────┬────────────────────────────────┘    │
│                    │                                       │
│  ┌─────────────────▼────────────────────────────────┐    │
│  │  Agent Layer (football_agent.py)                 │    │
│  │  • Team extraction • Single Tavily search        │    │
│  │  • Gemini/OpenAI/Ollama synthesis                │    │
│  └─────────────────┬────────────────────────────────┘    │
│                    │                                       │
│  ┌─────────────────▼────────────────────────────────┐    │
│  │  Data Source (tavily_client.py)                  │    │
│  │  • Single comprehensive web search               │    │
│  │  • Returns: Form + H2H + League + Stats          │    │
│  │  • 8 results, 800 chars each (optimized)         │    │
│  └───────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer       | Location            | Purpose                                   | Key Principles                         |
| ----------- | ------------------- | ----------------------------------------- | -------------------------------------- |
| **API**     | `app/api/routes.py`  | HTTP endpoints, request/response handling | No business logic, only I/O            |
| **Service** | `app/services/`      | Business logic orchestration              | Stateless, transaction boundaries      |
| **Agent**   | `app/agents/`        | AI orchestration, data synthesis          | LLM integration, intelligent analysis  |
| **Data**    | `app/services/`      | Tavily web search client                  | Single comprehensive search            |
| **Models**  | `app/models/`        | Data schemas (Pydantic)                   | Single source of truth for contracts   |
| **Config**  | `app/config/`        | Environment settings                      | Centralized configuration              |
| **Utils**   | `app/utils/`         | Shared utilities                          | Logging, exceptions, constants         |

### Data Flow

1. **User Input**: React form captures query (e.g., "Analyze Arsenal vs Chelsea")
2. **HTTP Request**: Frontend POST to `/api/v1/analyze-match`
3. **Validation**: Pydantic validates request body
4. **Service Call**: Route delegates to `analysis_service.analyze_match()`
5. **Agent Execution**: Agent extracts teams, makes single comprehensive Tavily search
6. **Synthesis**: Gemini/OpenAI/Ollama analyzes search data and generates insights
7. **Response**: Structured JSON flows back through layers to frontend
8. **Display**: React components render analysis sections

**Optimization**: Single Tavily search (85% reduction in API calls vs old 7-tool approach)

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (backend)
- **Node.js 18+** (frontend)
- **Google Gemini API Key** (recommended, free tier with 1,500 requests/day)
- **OpenAI API Key** (optional, fallback LLM)
- **Tavily API Key** (optional, 1,000 searches/month free)

### Installation

#### 1. Clone Repository

```bash
git clone https://github.com/keedwill/Ai-football-research
cd ai-football-research
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate
# Activate (macOS/Linux)
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys (optional)
```

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### Running the Application

#### Start Backend (Terminal 1)

```bash
cd backend
.\.venv\Scripts\activate  # or source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Backend will run at: **http://localhost:8000**

- Health Check: http://localhost:8000/health
- API Docs: http://localhost:8000/docs

#### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will run at: **http://localhost:5173**

### Usage

1. **Open http://localhost:5173** in your browser
2. **Enter a match query**: "Analyze Arsenal vs Chelsea"
3. **Click "Analyze"** or press Enter
4. **View results**: Summary, Form, H2H, League Position, Insights, Verdict

---

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Endpoints

#### `POST /analyze-match`

Analyzes a football match based on natural language query.

**Request:**

```http
POST /api/v1/analyze-match HTTP/1.1
Content-Type: application/json

{
  "query": "Analyze Arsenal vs Chelsea"
}
```

**Request Schema:**

| Field   | Type   | Required | Description                  | Constraints      |
| ------- | ------ | -------- | ---------------------------- | ---------------- |
| `query` | string | Yes      | Natural language match query | 3-200 characters |

**Response (200 OK):**

```json
{
  "analysis": {
    "summary": "Arsenal faces Chelsea in a crucial London derby...",
    "form": "Arsenal:\nWWWDW\n  Arsenal 3-1 Brentford (W)...",
    "head_to_head": "Last 5 matches:\n  Arsenal 5-0 Chelsea...",
    "league_position": "Arsenal: Position 2/20 (68 points)...",
    "insights": "Arsenal's consistent performances are reflected...",
    "final_verdict": "Based on current form, Arsenal enters as favorites..."
  }
}
```

**Error Responses:**

| Code | Description           | Example                                                             |
| ---- | --------------------- | ------------------------------------------------------------------- |
| 400  | Invalid query format  | `{"detail": "String should have at least 3 characters"}`            |
| 422  | Validation error      | `{"detail": [{"loc": ["body", "query"], "msg": "field required"}]}` |
| 500  | Internal server error | `{"detail": "An error occurred processing your request"}`           |

#### `GET /health`

Health check endpoint for monitoring.

**Response (200 OK):**

```json
{
  "status": "ok"
}
```

### Interactive Documentation

FastAPI provides auto-generated interactive docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🛠️ Tech Stack

### Backend

| Technology              | Purpose            | Version |
| ----------------------- | ------------------ | ------- |
| **Python**              | Runtime            | 3.11+   |
| **FastAPI**             | Web framework      | 0.111+  |
| **Uvicorn**             | ASGI server        | 0.29+   |
| **Gunicorn**            | Production server  | 21.2+   |
| **Pydantic**            | Data validation    | 2.7+    |
| **LangChain**           | AI orchestration   | 0.2+    |
| **Google Gemini**       | Primary LLM (free) | 1.5     |
| **OpenAI**              | Fallback LLM       | GPT-4   |
| **Tavily**              | Web search API     | Latest  |
| **httpx**               | Async HTTP client  | 0.27+   |

### Frontend

| Technology     | Purpose      | Version |
| -------------- | ------------ | ------- |
| **React**      | UI framework | 18.3+   |
| **Vite**       | Build tool   | 5.3+    |
| **JavaScript** | Language     | ES2022  |

### External APIs

- **Google Gemini API**: Primary LLM (free tier, 1,500 requests/day)
- **OpenAI API**: Fallback LLM for intelligent analysis synthesis
- **Tavily API**: Real-time web search for match data (1,000 searches/month free)

---

## 📂 Project Structure

```
aifootball/
├── backend/                          # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app entry point
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py             # HTTP endpoints
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   └── football_agent.py     # LangChain agent
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── settings.py           # Environment config
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── analysis.py           # Pydantic schemas
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── analysis_service.py   # Business logic
│   │   │   ├── football_service.py   # Football operations
│   │   │   └── tavily_client.py      # Tavily API search client
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── async_helper.py       # Async utilities
│   │       ├── constants.py          # App constants
│   │       ├── exceptions.py         # Custom exceptions
│   │       └── logger.py             # Logging config
│   ├── tests/
│   │   ├── test_agent.py
│   │   ├── test_api.py
│   │   ├── test_architecture.py
│   │   ├── test_frontend_integration.py
│   │   └── test_llm_integration.py
│   ├── .env.example                  # Environment template
│   ├── .gitignore
│   ├── requirements.txt              # Python dependencies
│   └── start.sh                      # Production startup script
│
├── frontend/                         # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── MatchInput.jsx        # Query input form
│   │   │   └── ResultDisplay.jsx     # Analysis display
│   │   ├── pages/
│   │   │   └── Home.jsx              # Main page
│   │   ├── services/
│   │   │   └── api.js                # Backend API client
│   │   ├── App.css                   # Global styles
│   │   ├── App.jsx                   # Root component
│   │   └── main.jsx                  # Entry point
│   ├── index.html
│   ├── package.json                  # Node dependencies
│   ├── vite.config.js                # Vite configuration
│   └── .gitignore
│
├── render.yaml                        # Render deployment config
├── DEPLOYMENT.md                      # Deployment guide
├── README.md                          # This file
└── LICENSE                            # MIT License
```

---

## 🔧 Development

### Environment Variables

Create a `.env` file in `backend/` directory:

```env
# Google Gemini (RECOMMENDED - free tier, 1,500 requests/day)
GOOGLE_API_KEY=AIza...your_gemini_key
GEMINI_MODEL=gemini-1.5-flash-latest

# OpenAI (optional fallback)
OPENAI_API_KEY=sk-proj-your_key_here

# Tavily Search (optional - 1,000 searches/month free)
TAVILY_API_KEY=tvly-dev-your_key

# Ollama (optional local LLM)
USE_OLLAMA=false
OLLAMA_MODEL=llama3.1
OLLAMA_BASE_URL=http://localhost:11434

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

**Important**: Never commit `.env` to version control. Use `.env.example` as a template.

### Running Tests

```bash
cd backend
.\.venv\Scripts\Activate.ps1

# Run all tests
pytest

# Run specific test file
python test_architecture.py
python test_llm_integration.py
python test_frontend_integration.py
```

### Code Quality

The project follows best practices:

- ✅ **Type Hints**: Comprehensive type annotations
- ✅ **Docstrings**: All functions documented
- ✅ **Error Handling**: Custom exception classes
- ✅ **Logging**: Structured logging throughout
- ✅ **Validation**: Pydantic models for all I/O
- ✅ **Testing**: Integration and unit tests
- ✅ **Code Organization**: Clean architecture patterns

---

## 🚀 Deployment

This project is ready for production deployment to **Render** (or similar platforms).

### Quick Deploy to Render

1. **Push to GitHub**

   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy Backend** (Render Web Service)
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
   - Environment Variables:
     ```
     ENVIRONMENT=production
     ALLOWED_ORIGINS=https://your-frontend.onrender.com
     OPENAI_API_KEY=sk-proj-...
     FOOTBALL_API_KEY=...
     ```

3. **Deploy Frontend** (Render Static Site)
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`
   - Environment Variable:
     ```
     VITE_API_URL=https://your-backend.onrender.com
     ```

4. **Configure CORS**
   - Update backend `ALLOWED_ORIGINS` with frontend URL
   - Redeploy backend

### Detailed Deployment Guide

For complete deployment instructions, troubleshooting, and best practices, see:

- **📘 [DEPLOYMENT.md](DEPLOYMENT.md)** - Comprehensive deployment guide
- **📋 [DEPLOY_QUICK_REFERENCE.md](DEPLOY_QUICK_REFERENCE.md)** - Quick reference card

### Alternative Deployment Options

- **Vercel**: Frontend deployment (similar to Render Static Site)
- **Railway**: Alternative to Render for backend
- **Heroku**: Classic PaaS option (requires buildpack)
- **AWS/GCP/Azure**: For enterprise deployments
- **Docker**: See [CODE_REVIEW.md](CODE_REVIEW.md) for containerization guide

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Write docstrings for all public functions
- Add tests for new features
- Update documentation as needed

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name**

- GitHub: [@yourusername](https://github.com/keedwill)
- LinkedIn: [Your Name](https://www.linkedin.com/in/princewill-owoh-201745131/)
- Portfolio: [yourwebsite.com](https://princewillowoh.onrender.com/)

---

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 API
- **API-Football** for comprehensive football data
- **FastAPI** team for excellent framework
- **LangChain** community for AI orchestration tools

---

## 📈 Future Enhancements

- [ ] Add authentication and user accounts
- [ ] Implement caching layer (Redis)
- [ ] Add more leagues (La Liga, Serie A, Bundesliga)
- [ ] Real-time match notifications
- [ ] Historical analysis and trends
- [ ] Machine learning predictions
- [ ] Mobile app (React Native)
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Kubernetes deployment configs

---

## 🌐 Live Demo

- **Frontend**: https://aifootball-frontend.onrender.com
- **Backend API**:https://ai-football-backend.onrender.com
- **API Docs**: https://ai-football-backend.onrender.com/docs

---

<p align="center">
  Made with ❤️ and ☕
</p>

<p align="center">
  <strong>If you found this project helpful, please consider giving it a ⭐️</strong>
</p>
