"""
services/analysis_service.py — Match analysis business logic.

This service orchestrates the match analysis workflow by delegating
to the LangChain agent.

Design decision: The API layer (routes.py) should never contain business
logic. All analysis logic flows through this service, making it easy to
swap implementations without touching the HTTP layer.
"""

from app.models.analysis import AnalysisResponse
from app.agents.football_agent import run_analysis
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def analyze_match(query: str) -> AnalysisResponse:
    """
    Analyze a football match based on a natural-language query.
    
    Args:
        query: Natural language description of the match to analyze
               (e.g., "Analyze Arsenal vs Chelsea")
    
    Returns:
        AnalysisResponse containing structured match analysis
    
    Design notes:
        - This function delegates to the football agent
        - All logging happens here and in the agent
        - Service layer provides a clean interface for the API layer
    """
    logger.info(f"Processing match analysis request: {query}")
    
    # Delegate to the football agent
    result = await run_analysis(query)
    
    logger.info("Match analysis completed successfully")
    return result
