"""
services/tavily_client.py — Tavily AI search client for live football data.

Tavily Documentation: https://docs.tavily.com/
Free tier: 1,000 searches/month

This service uses Tavily AI search to get real-time football data from the web.
"""

from tavily import TavilyClient
from typing import Optional, List, Dict
from datetime import datetime
from app.config.settings import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FootballTavilyClient:
    """Client for Tavily AI search focused on football data."""
    
    def __init__(self):
        self.api_key = settings.tavily_api_key
        self.client = None
        
        if self.api_key:
            self.client = TavilyClient(api_key=self.api_key)
        else:
            logger.warning("TAVILY_API_KEY not set - search will not work")
    
    async def search(self, query: str, max_results: int = 5) -> Optional[List[Dict]]:
        """
        Search the web for football data using Tavily.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
        
        Returns:
            List of search results with content and URLs
        """
        if not self.client:
            logger.warning("Tavily client not initialized - API key missing")
            return None
        
        try:
            logger.info(f"Tavily search: {query}")
            
            # Perform search
            response = self.client.search(
                query=query,
                search_depth="advanced",  # "basic" or "advanced" - advanced for better quality
                max_results=max_results,
            #    days=30,
                include_domains=[
                    "bbc.com",
                    "espn.com",
                    "skysports.com",
                    "goal.com",
                    "theguardian.com",
                    "sofascore.com",
                    "fotmob.com",
                    "premierleague.com",
                    "uefa.com",
                    "fifa.com"
                ],
                exclude_domains=["twitter.com", "facebook.com"]
            )
            
            # Extract results
            results = response.get("results", [])
            logger.info(f"Tavily returned {len(results)} results")
            
            return results
            
        except Exception as e:
            logger.exception(f"Error in Tavily search for '{query}'")
            return None
    
    async def search_team_form(self, team_name: str) -> Optional[str]:
        """
        Search for a team's recent form (club or national team).
        
        Args:
            team_name: Name of the team
        
        Returns:
            Search results text
        """
        current_year = datetime.now().year
        current_month = datetime.now().strftime("%B")
        # Improved search query with more specific terms for very recent matches
        query = f"{team_name} latest results last 5 matches  {current_year} recent fixtures scores"
        results = await self.search(query, max_results=7)
        
        if not results:
            return None
        
        # Combine content from all results
        content = "\n\n".join([
            f"Source: {r.get('title', 'Unknown')}\n{r.get('content', '')}"
            for r in results
        ])
        
        return content
    
    async def search_head_to_head(self, team_a: str, team_b: str) -> Optional[str]:
        """
        Search for head-to-head history between two teams (club or national).
        
        Args:
            team_a: First team name
            team_b: Second team name
        
        Returns:
            Search results text
        """
        current_year = datetime.now().year
        # Improved search query with more specific terms
        query = f"{team_a} vs {team_b} head to head h2h last meetings {current_year} recent matches results history"
        results = await self.search(query, max_results=6)
        
        if not results:
            return None
        
        content = "\n\n".join([
            f"Source: {r.get('title', 'Unknown')}\n{r.get('content', '')}"
            for r in results
        ])
        
        return content
    
    async def search_league_standings(self, team_name: str = None) -> Optional[str]:
        """
        Search for current league standings or tournament rankings.
        Works for club leagues and international tournaments/rankings.
        
        Args:
            team_name: Team name to search standings for (optional)
        
        Returns:
            Search results text
        """
        current_year = datetime.now().year
        
        if team_name:
            # Improved search for team-specific standings with current date context
            current_month = datetime.now().strftime("%B")
            query = f"{team_name} current league standings table position {current_year} latest"
        else:
            # Generic league search
            query = f"football league standings table {current_year}"
        
        results = await self.search(query, max_results=6)
        
        if not results:
            return None
        
        content = "\n\n".join([
            f"Source: {r.get('title', 'Unknown')}\n{r.get('content', '')}"
            for r in results
        ])
        
        return content
    
    async def search_team_statistics(self, team_name: str) -> Optional[str]:
        """
        Search for team season statistics (club or national team).
        
        Args:
            team_name: Name of the team
        
        Returns:
            Search results text
        """
        current_year = datetime.now().year
        current_month = datetime.now().strftime("%B")
        # Improved search query with more comprehensive terms including current context
        query = f"{team_name} {current_year}  statistics goals scored conceded record current season latest"
        results = await self.search(query, max_results=6)
        
        if not results:
            return None
        
        content = "\n\n".join([
            f"Source: {r.get('title', 'Unknown')}\n{r.get('content', '')}"
            for r in results
        ])
        
        return content
    
    async def search_comprehensive_match_analysis(self, team_a: str, team_b: str) -> Optional[str]:
        """
        Single comprehensive search for complete match analysis.
        Gets all data in one search: form, h2h, league positions, statistics.
        
        This replaces 7 separate searches with 1 efficient search.
        
        Args:
            team_a: First team name
            team_b: Second team name
        
        Returns:
            Combined search results with all match context
        """
        current_year = datetime.now().year
        current_month = datetime.now().strftime("%B")
        
        # Comprehensive query covering all aspects
        query = (
            f"{team_a} vs {team_b} {current_year} {current_month} "
            f"recent form last 5 matches results "
            f"head to head h2h history last meetings "
            f"league standings table position "
            f"season statistics goals xG performance "
            f"match preview analysis prediction"
        )
        
        # OPTIMIZED: Use fewer results for faster processing
        results = await self.search(query, max_results=8)
        
        if not results:
            return None
        
        # BALANCED: Limit content but allow enough for tables and stats
        max_content_per_result = 800  # Increased from 400 to capture more data
        
        content_parts = []
        for r in results:
            title = r.get('title', 'Unknown')
            raw_content = r.get('content', '')
            # Truncate long content
            truncated_content = raw_content[:max_content_per_result]
            if len(raw_content) > max_content_per_result:
                truncated_content += "..."
            
            content_parts.append(f"Source: {title}\n{truncated_content}")
        
        content = "\n\n".join(content_parts)
        
        # BALANCED: Higher limit to preserve important data
        max_total_chars = 8000  # Increased from 4000
        if len(content) > max_total_chars:
            content = content[:max_total_chars] + "\n\n[Content truncated for performance...]"
        
        logger.info(f"Comprehensive search returned {len(results)} results ({len(content)} chars) for {team_a} vs {team_b}")
        
        return content


# Singleton instance
_client = None


def get_tavily_client() -> FootballTavilyClient:
    """Get singleton FootballTavilyClient instance."""
    global _client
    if _client is None:
        _client = FootballTavilyClient()
    return _client
