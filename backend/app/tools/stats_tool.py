"""
tools/stats_tool.py — Tool: get season statistics for a team.

Returns comprehensive season statistics including goals, xG, and tactical data.
Uses Tavily AI search for live data exclusively.
"""

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from app.services.tavily_client import get_tavily_client
from app.config.settings import settings
from app.utils.logger import get_logger
from app.utils.async_helper import run_async

logger = get_logger(__name__)


async def get_team_statistics_live(team_name: str) -> str:
    """
    Get team statistics using Tavily AI search + GPT-4 extraction.
    
    Args:
        team_name: Name of the team
    
    Returns:
        String with detailed season statistics
    """
    try:
        client = get_tavily_client()
        
        # Search for team statistics
        search_results = await client.search_team_statistics(team_name)
        if not search_results:
            logger.warning(f"No Tavily results for '{team_name}' statistics")
            return None
        
        # Use GPT-4 to extract structured stats
        if not (settings.use_ollama or settings.openai_api_key):
            logger.warning("No LLM configured, cannot extract statistics")
            return None
        
        if settings.use_ollama:
            llm = Ollama(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url,
                temperature=0
            )
        else:
            llm = ChatOpenAI(model="gpt-4", temperature=0, api_key=settings.openai_api_key)
        
        prompt = f"""Extract season statistics for {team_name} from this text.

Format your response EXACTLY like this:
{team_name} Season Statistics ([number] games):
    Goals Scored: [number]
    Goals Conceded: [number]
    Goal Difference: [+/-number]
    Clean Sheets: [number]
    Home Record: [W]W-[D]D-[L]L
    Away Record: [W]W-[D]D-[L]L

Example:
Arsenal Season Statistics (30 games):
    Goals Scored: 71
    Goals Conceded: 28
    Goal Difference: +43
    Clean Sheets: 14
    Home Record: 13W-2D-0L
    Away Record: 9W-4D-2L

Text to extract from:
{search_results}

IMPORTANT INSTRUCTIONS:
- If you can find ANY statistics for {team_name}, extract them in the format above
- If you cannot find ANY statistics at all, respond with EXACTLY: "NO_DATA_FOUND"
- Do NOT provide explanations about missing data
- Do NOT say things like "The text provided does not contain..."
- Either provide statistics in the format above OR respond with exactly "NO_DATA_FOUND"""
        
        response = llm.invoke(prompt)
        extracted_stats = response.content if hasattr(response, 'content') else response
        
        # Check if GPT-4 couldn't extract data
        if "NO_DATA_FOUND" in extracted_stats or "does not contain" in extracted_stats.lower() or "cannot find" in extracted_stats.lower() or len(extracted_stats) < 50:
            logger.warning(f"GPT-4 could not extract statistics for {team_name}, response: {extracted_stats[:100]}")
            return None
        
        logger.info(f"Extracted statistics for {team_name}")
        return extracted_stats
        
    except Exception:
        logger.exception("Error fetching live statistics with Tavily")
        return None


def get_team_statistics(team_name: str) -> str:
    """
    Get comprehensive season statistics for a team using Tavily search.
    
    Args:
        team_name: Name of the team
    
    Returns:
        String with detailed season statistics, or unavailable message
    """
    if not settings.tavily_api_key:
        return f"{team_name} Season Statistics: Data unavailable (Tavily API key not configured)"
    
    logger.info(f"Fetching live statistics for {team_name}")
    try:
        live_data = run_async(get_team_statistics_live(team_name))
        if live_data:
            logger.info(f"Successfully fetched live statistics for {team_name}")
            return live_data
        else:
            return f"{team_name} Season Statistics: Data currently unavailable from search results"
    except Exception:
        logger.exception("Error fetching live statistics")
        return f"{team_name} Season Statistics: Error retrieving data"
