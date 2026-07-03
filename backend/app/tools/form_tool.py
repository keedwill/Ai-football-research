"""
tools/form_tool.py — Tool: get recent team form.

Returns the last 5 match results for any team (club or national).
Uses Tavily AI search for live data exclusively.
"""

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from app.services.tavily_client import get_tavily_client
from app.config.settings import settings
from app.utils.logger import get_logger
from app.utils.async_helper import run_async

logger = get_logger(__name__)


async def get_team_form_live(team_name: str) -> str:
    """
    Get recent form using Tavily AI search + GPT-4 extraction.
    
    Args:
        team_name: Name of the team
    
    Returns:
        String describing recent form with match results
    """
    try:
        client = get_tavily_client()
        
        # Search for team form
        search_results = await client.search_team_form(team_name)
        if not search_results:
            logger.warning(f"No Tavily results for '{team_name}' form")
            return None
        
        # Use GPT-4 to extract structured form data
        if not (settings.use_ollama or settings.openai_api_key):
            logger.warning("No LLM configured, cannot extract form data")
            return None
        
        if settings.use_ollama:
            llm = Ollama(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url,
                temperature=0
            )
        else:
            llm = ChatOpenAI(model="gpt-4", temperature=0, api_key=settings.openai_api_key)
        
        prompt = f"""Extract the last 5 match results for {team_name} from this text.

Format your response EXACTLY like this:
{team_name} Recent Form: [W/D/L pattern]
    [Match result 1]
    [Match result 2]
    [Match result 3]
    [Match result 4]
    [Match result 5]

Examples:
Arsenal Recent Form: WWDWL
    Arsenal 2-0 Brighton (W)
    Wolves 1-2 Arsenal (W)
    Arsenal 2-2 Liverpool (D)
    West Ham 0-6 Arsenal (W)
    Arsenal 1-3 Manchester City (L)

Brazil Recent Form: WWLWD
    Brazil 4-1 Peru (W)
    Colombia 0-1 Brazil (W)
    Brazil 0-1 Argentina (L)
    Uruguay 1-1 Brazil (D)
    Brazil 5-1 Bolivia (W)

Text to extract from:
{search_results}

IMPORTANT INSTRUCTIONS:
- If you can find ANY recent match results (even just 1-3 matches), extract them in the format above
- If you cannot find ANY match results at all, respond with EXACTLY: "NO_DATA_FOUND"
- Do NOT provide explanations about missing data
- Do NOT say things like "The text provided does not contain..."
- Either provide match results in the format above OR respond with exactly "NO_DATA_FOUND"""
        
        response = llm.invoke(prompt)
        extracted_form = response.content if hasattr(response, 'content') else response
        
        # Check if GPT-4 couldn't extract data
        if "NO_DATA_FOUND" in extracted_form or "does not contain" in extracted_form.lower() or "cannot find" in extracted_form.lower() or len(extracted_form) < 50:
            logger.warning(f"GPT-4 could not extract form data for {team_name}, response: {extracted_form[:100]}")
            return None
        
        logger.info(f"Extracted form data for {team_name}")
        return extracted_form
        
    except Exception:
        logger.exception("Error fetching live form data with Tavily")
        return None


def get_team_form(team_name: str) -> str:
    """
    Get the last 5 match results for a team using Tavily search.
    
    Args:
        team_name: Name of the team (e.g., "Arsenal", "Chelsea")
    
    Returns:
        String describing recent form, or unavailable message
    """
    if not settings.tavily_api_key:
        return f"{team_name} Recent Form: Data unavailable (Tavily API key not configured)"
    
    logger.info(f"Fetching live form data for {team_name}")
    try:
        live_data = run_async(get_team_form_live(team_name))
        if live_data:
            logger.info(f"Successfully fetched live form data for {team_name}")
            return live_data
        else:
            return f"{team_name} Recent Form: Data currently unavailable from search results"
    except Exception:
        logger.exception("Error fetching live form data")
        return f"{team_name} Recent Form: Error retrieving data"
