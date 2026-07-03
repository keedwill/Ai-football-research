"""  
tools/league_tool.py — Tool: get current league position for a team.

Returns the current league standing or FIFA ranking for any team.
Uses Tavily AI search for live data exclusively.
"""

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from app.services.tavily_client import get_tavily_client
from app.config.settings import settings
from app.utils.logger import get_logger
from app.utils.async_helper import run_async

logger = get_logger(__name__)


async def get_league_position_live(team_name: str) -> str:
    """
    Get league position using Tavily AI search + GPT-4 extraction.
    
    Args:
        team_name: Name of the team
    
    Returns:
        String describing league position and stats
    """
    try:
        client = get_tavily_client()
        
        # Search for team-specific standings
        search_results = await client.search_league_standings(team_name=team_name)
        if not search_results:
            logger.warning(f"No Tavily results for {team_name} standings")
            return None
        
        # Use GPT-4 to extract specific team's position
        if not (settings.use_ollama or settings.openai_api_key):
            logger.warning("No LLM configured, cannot extract league data")
            return None
        
        if settings.use_ollama:
            llm = Ollama(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url,
                temperature=0
            )
        else:
            llm = ChatOpenAI(model="gpt-4", temperature=0, api_key=settings.openai_api_key)
        
        prompt = f"""Extract the current league standing or ranking for {team_name} from this text.

For CLUB TEAMS, format like this:
{team_name} League Position:
    League: [League name]
    Position: [rank] ([context like Champions League zone/Relegation zone])
    Points: [points]
    Played: [games]
    Goal Difference: [+/-number]

For NATIONAL TEAMS, format like this:
{team_name} FIFA Ranking:
    FIFA Rank: [number]
    Continental Rank: [number if available]
    Recent Tournament: [info if available]

Examples:
Barcelona League Position:
    League: La Liga
    Position: 2nd (Champions League qualification)
    Points: 68
    Played: 30
    Goal Difference: +43

Brazil FIFA Ranking:
    FIFA Rank: 5
    Continental Rank: 1 (CONMEBOL)
    Recent Tournament: Copa America 2024 - Champions

Text to extract from:
{search_results}

IMPORTANT INSTRUCTIONS:
- If you can find ANY league standing or ranking data for {team_name}, extract it in the format above
- If you cannot find ANY data at all, respond with EXACTLY: "NO_DATA_FOUND"
- Do NOT provide explanations about missing data
- Do NOT say things like "The text provided does not contain..."
- Either provide data in the format above OR respond with exactly "NO_DATA_FOUND"

Extract the standing/ranking data for {team_name} specifically."""
        
        response = llm.invoke(prompt)
        extracted_position = response.content if hasattr(response, 'content') else response
        
        # Check if GPT-4 couldn't extract data
        if "NO_DATA_FOUND" in extracted_position or "does not contain" in extracted_position.lower() or "cannot find" in extracted_position.lower() or len(extracted_position) < 50:
            logger.warning(f"GPT-4 could not extract league position for {team_name}, response: {extracted_position[:100]}")
            return None
        
        logger.info(f"Extracted league position for {team_name}")
        return extracted_position
        
    except Exception:
        logger.exception("Error fetching live league data with Tavily")
        return None


def get_league_position(team_name: str) -> str:
    """
    Get the current league position for a team using Tavily search.
    
    Args:
        team_name: Name of the team
    
    Returns:
        String describing league position, or unavailable message
    """
    if not settings.tavily_api_key:
        return f"{team_name} League Position: Data unavailable (Tavily API key not configured)"
    
    logger.info(f"Fetching live league position for {team_name}")
    try:
        live_data = run_async(get_league_position_live(team_name))
        if live_data:
            logger.info(f"Successfully fetched live league position for {team_name}")
            return live_data
        else:
            return f"{team_name} League Position: Data currently unavailable from search results"
    except Exception:
        logger.exception("Error fetching live league data")
        return f"{team_name} League Position: Error retrieving data"
