"""
tools/h2h_tool.py — Tool: get head-to-head history between two teams.

Returns the recent head-to-head record between two teams (club or national).
Uses Tavily AI search for live data exclusively.
"""

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from app.services.tavily_client import get_tavily_client
from app.config.settings import settings
from app.utils.logger import get_logger
from app.utils.async_helper import run_async

logger = get_logger(__name__)


async def get_head_to_head_live(team_a: str, team_b: str) -> str:
    """
    Get head-to-head history using Tavily AI search + GPT-4 extraction.
    
    Args:
        team_a: First team name
        team_b: Second team name
    
    Returns:
        String describing recent head-to-head results
    """
    try:
        client = get_tavily_client()
        
        # Search for H2H history
        search_results = await client.search_head_to_head(team_a, team_b)
        if not search_results:
            logger.warning(f"No Tavily results for '{team_a}' vs '{team_b}' H2H")
            return None
        
        # Use GPT-4 to extract structured H2H data
        if not (settings.use_ollama or settings.openai_api_key):
            logger.warning("No LLM configured, cannot extract H2H data")
            return None
        
        if settings.use_ollama:
            llm = Ollama(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url,
                temperature=0
            )
        else:
            llm = ChatOpenAI(model="gpt-4", temperature=0, api_key=settings.openai_api_key)
        
        prompt = f"""Extract the last 5 head-to-head match results between {team_a} and {team_b} from this text.

Format your response EXACTLY like this:
Head-to-Head: {team_a} vs {team_b} (Last 5 matches):
    [Match result 1]
    [Match result 2]
    [Match result 3]
    [Match result 4]
    [Match result 5]

Example:
Head-to-Head: Arsenal vs Chelsea (Last 5 matches):
    Arsenal 5-0 Chelsea (Apr 2024)
    Chelsea 2-2 Arsenal (Oct 2023)
    Arsenal 3-1 Chelsea (May 2023)

Text to extract from:
{search_results}

IMPORTANT INSTRUCTIONS:
- If you can find ANY head-to-head match results (even just 1-3 matches), extract them in the format above
- If you cannot find ANY H2H match results at all, respond with EXACTLY: "NO_DATA_FOUND"
- Do NOT provide explanations about missing data
- Do NOT say things like "The text provided does not contain..."
- Either provide match results in the format above OR respond with exactly "NO_DATA_FOUND"""
        
        response = llm.invoke(prompt)
        extracted_h2h = response.content if hasattr(response, 'content') else response
        
        # Check if GPT-4 couldn't extract data
        if "NO_DATA_FOUND" in extracted_h2h or "does not contain" in extracted_h2h.lower() or "cannot find" in extracted_h2h.lower() or len(extracted_h2h) < 50:
            logger.warning(f"GPT-4 could not extract H2H data for {team_a} vs {team_b}, response: {extracted_h2h[:100]}")
            return None
        
        logger.info(f"Extracted H2H data for {team_a} vs {team_b}")
        return extracted_h2h
        
    except Exception:
        logger.exception("Error fetching live H2H data with Tavily")
        return None


def get_head_to_head(team_a: str, team_b: str) -> str:
    """
    Get head-to-head history between two teams using Tavily search.
    
    Args:
        team_a: First team name
        team_b: Second team name
    
    Returns:
        String describing recent head-to-head results, or unavailable message
    """
    if not settings.tavily_api_key:
        return f"Head-to-Head: {team_a} vs {team_b}\n    Data unavailable (Tavily API key not configured)"
    
    logger.info(f"Fetching live H2H data for {team_a} vs {team_b}")
    try:
        live_data = run_async(get_head_to_head_live(team_a, team_b))
        if live_data:
            logger.info(f"Successfully fetched live H2H data for {team_a} vs {team_b}")
            return live_data
        else:
            return f"Head-to-Head: {team_a} vs {team_b}\n    Data currently unavailable from search results"
    except Exception:
        logger.exception("Error fetching live H2H data")
        return f"Head-to-Head: {team_a} vs {team_b}\n    Error retrieving data"
