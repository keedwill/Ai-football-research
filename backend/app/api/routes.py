"""
api/routes.py — FastAPI route definitions.

All endpoints are registered on a single APIRouter that main.py mounts.
Each handler:
  1. Validates the incoming request against a Pydantic model (models/)
  2. Delegates work to the service layer (services/)
  3. Returns a typed Pydantic response model

Design decision: Routes own HTTP concerns ONLY. No business logic here.
"""

from fastapi import APIRouter, HTTPException, status
from app.models.analysis import AnalysisRequest, AnalysisResponse
from app.services.analysis_service import analyze_match as analyze_match_service
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/analyze-match",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze a football match",
    description="""
    Accepts a natural-language query about a football match and returns
    structured analysis using a LangChain agent with football data tools.
    
    Example queries:
    - "Analyze Arsenal vs Chelsea"
    - "Who will win Man United vs Liverpool?"
    - "Predict Tottenham vs Manchester City"
    """
)
async def analyze_match(request: AnalysisRequest):
    """
    Main endpoint for match analysis.
    
    Architecture:
        API Layer (here)    → validates HTTP request
        Service Layer       → orchestrates business logic
        Agent Layer         → calls tools and synthesizes results
        Tools Layer         → fetches data
    
    This handler owns HTTP concerns only. All business logic is delegated
    to the service layer (services/analysis_service.py).
    """
    try:
        logger.info(f"Received analysis request: {request.query}")
        result = await analyze_match_service(request.query)
        return result
    except Exception as e:
        logger.exception(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )
