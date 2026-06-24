"""
tools/form_tool.py — Tool: get recent team form.

Returns the last 5 match results for a given team.
Uses API-Football for live data, falls back to mock data if API unavailable.
"""

from app.services.football_api_client import get_football_api_client
from app.config.settings import settings
from app.utils.logger import get_logger
import asyncio

logger = get_logger(__name__)


async def get_team_form_live(team_name: str) -> str:
    """
    Get recent form using API-Football API.
    
    Args:
        team_name: Name of the team
    
    Returns:
        String describing recent form with actual match results
    """
    try:
        client = get_football_api_client()
        
        # Search for team
        team_id = await client.search_team(team_name)
        if not team_id:
            logger.warning(f"Could not find team ID for '{team_name}'")
            return None
        
        # Get recent fixtures
        fixtures = await client.get_team_fixtures(team_id, last=5)
        if not fixtures:
            return None
        
        form_pattern = ""
        results = []
        
        for fixture in fixtures:
            home = fixture["teams"]["home"]["name"]
            away = fixture["teams"]["away"]["name"]
            home_goals = fixture["goals"]["home"]
            away_goals = fixture["goals"]["away"]
            
            # Determine result from team's perspective
            if fixture["teams"]["home"]["id"] == team_id:
                # Team played at home
                if home_goals > away_goals:
                    form_pattern += "W"
                    result = f"{home} {home_goals}-{away_goals} {away} (W)"
                elif home_goals < away_goals:
                    form_pattern += "L"
                    result = f"{home} {home_goals}-{away_goals} {away} (L)"
                else:
                    form_pattern += "D"
                    result = f"{home} {home_goals}-{away_goals} {away} (D)"
            else:
                # Team played away
                if away_goals > home_goals:
                    form_pattern += "W"
                    result = f"{home} {home_goals}-{away_goals} {away} (W)"
                elif away_goals < home_goals:
                    form_pattern += "L"
                    result = f"{home} {home_goals}-{away_goals} {away} (L)"
                else:
                    form_pattern += "D"
                    result = f"{home} {home_goals}-{away_goals} {away} (D)"
            
            results.append(result)
        
        # Format output
        output = f"{team_name} Recent Form: {form_pattern}\n"
        for result in results:
            output += f"    {result}\n"
        
        return output.strip()
        
    except Exception:
        logger.exception("Error fetching live form data")
        return None


def get_team_form(team_name: str) -> str:
    """
    Get the last 5 match results for a team.
    
    Uses live API data if available, falls back to mock data.
    
    Args:
        team_name: Name of the team (e.g., "Arsenal", "Chelsea")
    
    Returns:
        String describing recent form (W/D/L pattern and match results)
    """
    # Try live data first if API key is configured
    if settings.football_api_key:
        logger.info(f"Attempting to fetch live form data for {team_name}")
        try:
            # Run async function in sync context
            live_data = asyncio.run(get_team_form_live(team_name))
            if live_data:
                logger.info(f"Successfully fetched live form data for {team_name}")
                return live_data
            else:
                logger.warning(f"Live data unavailable for {team_name}, using mock data")
        except Exception:
            logger.exception("Error fetching live data, falling back to mock data")
    else:
        logger.info("FOOTBALL_API_KEY not set, using mock data")
    
    # Fallback to mock data
    # Mock form data for popular Premier League teams
    mock_forms = {
        "Arsenal": {
            "form": "WWDWW",
            "results": [
                "Arsenal 2-0 Brighton (W)",
                "Wolves 1-2 Arsenal (W)",
                "Arsenal 2-2 Liverpool (D)",
                "West Ham 0-6 Arsenal (W)",
                "Arsenal 3-1 Crystal Palace (W)"
            ]
        },
        "Chelsea": {
            "form": "WLDLW",
            "results": [
                "Chelsea 2-1 Newcastle (W)",
                "Man United 2-1 Chelsea (L)",
                "Chelsea 1-1 Burnley (D)",
                "Aston Villa 1-0 Chelsea (L)",
                "Chelsea 3-2 Brighton (W)"
            ]
        },
        "Manchester United": {
            "form": "LWDWW",
            "results": [
                "Man United 2-1 Chelsea (W)",
                "Man United 3-0 Everton (W)",
                "Nottingham Forest 2-2 Man United (D)",
                "Tottenham 2-0 Man United (L)",
                "Man United 1-0 Wolves (L)"
            ]
        },
        "Liverpool": {
            "form": "WWWDW",
            "results": [
                "Liverpool 4-1 Brentford (W)",
                "Arsenal 2-2 Liverpool (D)",
                "Liverpool 2-0 Sheffield United (W)",
                "Bournemouth 0-3 Liverpool (W)",
                "Liverpool 5-1 West Ham (W)"
            ]
        },
        "Manchester City": {
            "form": "WWWWL",
            "results": [
                "Aston Villa 1-0 Man City (L)",
                "Man City 5-1 Luton (W)",
                "Man City 3-1 Newcastle (W)",
                "Brighton 1-4 Man City (W)",
                "Man City 2-0 Everton (W)"
            ]
        },
        "Tottenham": {
            "form": "WLWDW",
            "results": [
                "Tottenham 3-1 Burnley (W)",
                "Tottenham 2-2 Everton (D)",
                "Tottenham 2-0 Man United (W)",
                "Newcastle 4-0 Tottenham (L)",
                "Tottenham 2-1 Crystal Palace (W)"
            ]
        }
    }
    
    # Normalize team name (case-insensitive, handle variations)
    normalized_name = team_name.strip().title()
    
    # Check for common abbreviations
    abbreviations = {
        "Man United": "Manchester United",
        "Man Utd": "Manchester United",
        "United": "Manchester United",
        "Man City": "Manchester City",
        "City": "Manchester City",
        "Spurs": "Tottenham"
    }
    
    if normalized_name in abbreviations:
        normalized_name = abbreviations[normalized_name]
    
    if normalized_name in mock_forms:
        data = mock_forms[normalized_name]
        form = data["form"]
        results = "\n    ".join(data["results"])
        return f"{normalized_name} Recent Form: {form}\n    {results}"
    else:
        # Generic response for teams not in mock data
        return f"{team_name} Recent Form: WDWDL (mock data not available for this team)"
