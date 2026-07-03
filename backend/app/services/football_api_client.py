"""
services/football_api_client.py — API-Football client for live data.

API-Football Documentation: https://www.api-football.com/documentation-v3
Free tier: 100 requests/day

This service replaces mock data with real API calls to API-Football.
"""

import httpx
from typing import Optional, Dict, List
from app.config.settings import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FootballAPIClient:
    """Client for API-Football v3."""
    
    BASE_URL = "https://v3.football.api-football.com"
    
    def __init__(self):
        self.api_key = settings.football_api_key
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "v3.football.api-football.com"
        }
        
        if not self.api_key:
            logger.warning("FOOTBALL_API_KEY not set - API calls will fail")
    
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make authenticated request to API-Football.
        
        Args:
            endpoint: API endpoint (e.g., "/teams")
            params: Query parameters
        
        Returns:
            JSON response from API
        
        Raises:
            httpx.HTTPError: If request fails
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            logger.info(f"API-Football request: {endpoint} with params {params}")
            response = await client.get(url, headers=self.headers, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            # API-Football returns data in { "response": [...] } format
            return data.get("response", [])
    
    async def search_team(self, team_name: str, league_id: int = 39) -> Optional[int]:
        """
        Search for a team by name and get its ID.
        
        Args:
            team_name: Team name to search for
            league_id: League ID (39 = Premier League)
        
        Returns:
            Team ID if found, None otherwise
        """
        try:
            params = {"name": team_name, "league": league_id, "season": 2023}
            teams = await self._make_request("/teams", params)
            
            if teams:
                team_id = teams[0]["team"]["id"]
                logger.info(f"Found team '{team_name}' with ID {team_id}")
                return team_id
            
            logger.warning(f"Team '{team_name}' not found")
            return None
            
        except Exception as e:
            logger.exception(f"Error searching for team '{team_name}'")
            return None
    
    async def get_team_fixtures(self, team_id: int, last: int = 5) -> List[Dict]:
        """
        Get recent fixtures for a team.
        
        Args:
            team_id: API-Football team ID
            last: Number of recent matches to fetch
        
        Returns:
            List of fixture data
        """
        try:
            params = {"team": team_id, "last": last, "season": 2023}
            fixtures = await self._make_request("/fixtures", params)
            return fixtures
            
        except Exception as e:
            logger.exception(f"Error fetching fixtures for team {team_id}")
            return []
    
    async def get_h2h(self, team1_id: int, team2_id: int, last: int = 5) -> List[Dict]:
        """
        Get head-to-head matches between two teams.
        
        Args:
            team1_id: First team ID
            team2_id: Second team ID
            last: Number of recent H2H matches
        
        Returns:
            List of H2H fixture data
        """
        try:
            params = {"h2h": f"{team1_id}-{team2_id}", "last": last}
            h2h = await self._make_request("/fixtures/headtohead", params)
            return h2h
            
        except Exception as e:
            logger.exception(f"Error fetching H2H for {team1_id} vs {team2_id}")
            return []
    
    async def get_team_statistics(self, team_id: int, league_id: int = 39, season: int = 2023) -> Optional[Dict]:
        """
        Get season statistics for a team.
        
        Args:
            team_id: Team ID
            league_id: League ID (39 = Premier League)
            season: Season year
        
        Returns:
            Team statistics dict
        """
        try:
            params = {"team": team_id, "league": league_id, "season": season}
            stats = await self._make_request("/teams/statistics", params)
            
            # API-Football returns statistics in first element
            if stats and len(stats) > 0:
                return stats[0]
            
            return None
            
        except Exception as e:
            logger.exception(f"Error fetching statistics for team {team_id}")
            return None
    
    async def get_standings(self, league_id: int = 39, season: int = 2023) -> List[Dict]:
        """
        Get league standings.
        
        Args:
            league_id: League ID (39 = Premier League)
            season: Season year
        
        Returns:
            List of standings data
        """
        try:
            params = {"league": league_id, "season": season}
            standings = await self._make_request("/standings", params)
            
            # Extract the standings array from nested structure
            if standings and len(standings) > 0:
                return standings[0].get("league", {}).get("standings", [[]])[0]
            
            return []
            
        except Exception as e:
            logger.exception(f"Error fetching standings for league {league_id}")
            return []


# Singleton instance
_client = None


def get_football_api_client() -> FootballAPIClient:
    """Get singleton FootballAPIClient instance."""
    global _client
    if _client is None:
        _client = FootballAPIClient()
    return _client
