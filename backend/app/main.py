"""
main.py — FastAPI application entry point.

Responsibilities:
- Create and configure the FastAPI app instance
- Register routers from the api/ layer
- Apply middleware (CORS, logging, etc.)
- Define startup/shutdown lifecycle hooks

Design decision: All route definitions live in api/routes.py.
This file stays thin — infrastructure only, no business logic.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# App initialisation
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AI Football Research System",
    description="LangChain-powered football match analysis API",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# CORS — configured via environment variables for production
# ---------------------------------------------------------------------------

# Parse allowed origins from settings (handles both string and list)
allowed_origins = settings.allowed_origins
if isinstance(allowed_origins, str):
    # Split comma-separated string into list
    allowed_origins = [origin.strip() for origin in allowed_origins.split(",")]

logger.info(f"CORS allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers — imported here once all sub-packages are implemented.
# ---------------------------------------------------------------------------

from app.api.routes import router

app.include_router(router, prefix="/api/v1", tags=["Analysis"])


# ---------------------------------------------------------------------------
# Health-check — always useful for deployment pipelines
# ---------------------------------------------------------------------------

@app.get("/health", tags=["System"])
async def health_check():
    """Comprehensive health check for monitoring."""
    # Determine which LLM is active (priority: Gemini > OpenAI > Ollama)
    if settings.google_api_key:
        llm_status = "gemini"
    elif settings.openai_api_key and not settings.use_ollama:
        llm_status = "openai"
    elif settings.use_ollama:
        llm_status = "ollama"
    else:
        llm_status = "disabled"
    
    health_status = {
        "status": "healthy",
        "environment": settings.environment,
        "checks": {
            "llm": llm_status,
            "data_source": "tavily" if settings.tavily_api_key else "mock"
        }
    }
    return health_status


@app.on_event("startup")
async def startup_event():
    """Log application startup information."""
    logger.info(f"Starting AI Football Research System")
    logger.info(f"Environment: {settings.environment}")
    
    # Priority: Gemini (FREE) > OpenAI (PAID) > Ollama (LOCAL)
    if settings.google_api_key:
        logger.info(f"LLM: Google Gemini ({settings.gemini_model}) - FREE TIER")
    elif settings.openai_api_key and not settings.use_ollama:
        logger.info("LLM: OpenAI (gpt-4o-mini) - PAID")
    elif settings.use_ollama:
        logger.info(f"LLM: Ollama ({settings.ollama_model}) at {settings.ollama_base_url} - LOCAL")
    else:
        logger.info("LLM: Not configured (using rule-based fallback)")
    
    logger.info(f"Tavily API: {'Configured' if settings.tavily_api_key else 'Not configured'}")


@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown."""
    logger.info("Shutting down AI Football Research System")
