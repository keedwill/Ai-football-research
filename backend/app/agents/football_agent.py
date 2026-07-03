"""
agents/football_agent.py — Football analysis orchestration agent.

This agent receives a natural-language query about a football match and
orchestrates calls to multiple tools to build a comprehensive analysis.

Supports both Ollama (development) and OpenAI (production) for intelligent synthesis.

OPTIMIZED: Uses single Tavily search instead of 7 separate searches.
"""

import re
from typing import Tuple, Optional
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.tavily_client import get_tavily_client
from app.models.analysis import AnalysisDetail, AnalysisResponse
from app.config.settings import settings
from app.utils.logger import get_logger
from app.utils.async_helper import run_async

logger = get_logger(__name__)


def extract_teams(query: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract team names from a natural language query.
    
    Args:
        query: Natural language query like "Analyze Arsenal vs Chelsea"
    
    Returns:
        Tuple of (team_a, team_b) or (None, None) if not found
    
    Examples:
        "Analyze Arsenal vs Chelsea" -> ("Arsenal", "Chelsea")
        "Man United vs Liverpool" -> ("Man United", "Liverpool")
        "Who will win Arsenal Chelsea?" -> ("Arsenal", "Chelsea")
    """
    # Remove common prefixes that interfere with extraction
    clean_query = query
    prefixes_to_remove = [
        r"^analyze\s+",
        r"^predict\s+",
        r"^compare\s+",
        r"^who\s+will\s+win\s+",
        r"^match\s+analysis\s+",
    ]
    
    for prefix in prefixes_to_remove:
        clean_query = re.sub(prefix, "", clean_query, flags=re.IGNORECASE)
    
    # Common patterns for match queries
    patterns = [
        r"^(\w+(?:\s+\w+)*?)\s+vs?\.?\s+(\w+(?:\s+\w+)*)$",     # "Arsenal vs Chelsea"
        r"^(\w+(?:\s+\w+)*?)\s+versus\s+(\w+(?:\s+\w+)*)$",     # "Arsenal versus Chelsea"
        r"^(\w+(?:\s+\w+)*?)\s+and\s+(\w+(?:\s+\w+)*)$",        # "Arsenal and Chelsea"
        r"^(\w+(?:\s+\w+)*?)\s+-\s+(\w+(?:\s+\w+)*)$",          # "Arsenal - Chelsea"
        r"^(\w+(?:\s+\w+)*?)\s+against\s+(\w+(?:\s+\w+)*)$",    # "Arsenal against Chelsea"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, clean_query.strip(), re.IGNORECASE)
        if match:
            team_a = match.group(1).strip()
            team_b = match.group(2).strip()
            logger.info(f"Extracted teams: {team_a} vs {team_b}")
            return team_a, team_b
    
    logger.warning(f"Could not extract team names from query: {query}")
    return None, None


def synthesize_analysis(
    team_a: str,
    team_b: str,
    search_data: str
) -> AnalysisDetail:
    """
    Synthesize comprehensive search data into structured analysis using LLM.
    
    OPTIMIZED: Takes single search result instead of 7 separate tool outputs.
    LLM extracts and structures all required sections from the raw data.
    
    Uses Ollama (development) or OpenAI (production) to generate intelligent insights.
    Falls back to rule-based synthesis if LLM is unavailable.
    
    Args:
        team_a: First team name
        team_b: Second team name
        search_data: Comprehensive Tavily search results
    
    Returns:
        AnalysisDetail with all structured sections
    """
    # Try LLM-powered synthesis
    llm_available = settings.google_api_key or settings.use_ollama or settings.openai_api_key
    
    if llm_available:
        try:
            # Priority: Gemini (FREE) > OpenAI (PAID) > Ollama (LOCAL)
            if settings.google_api_key:
                logger.info(f"Using Google Gemini ({settings.gemini_model}) for analysis synthesis")
                llm = ChatGoogleGenerativeAI(
                    model=settings.gemini_model,
                    temperature=0.3,
                    google_api_key=settings.google_api_key
                )
            elif settings.openai_api_key and not settings.use_ollama:
                logger.info("Using OpenAI LLM for analysis synthesis")
                llm = ChatOpenAI(
                    model="gpt-4o-mini",  # Faster and cheaper than gpt-3.5-turbo
                    temperature=0.3,  # Lower temp = faster inference
                    api_key=settings.openai_api_key
                )
            elif settings.use_ollama:
                logger.info(f"Using Ollama ({settings.ollama_model}) for analysis synthesis")
                llm = Ollama(
                    model=settings.ollama_model,
                    base_url=settings.ollama_base_url,
                    temperature=0.3,  # Lower temp = faster inference
                    num_ctx=2048,  # Limit context window for speed
                    num_predict=800,  # Limit response length for speed
                )
            else:
                logger.warning("No LLM configured properly")
                llm_available = False
            
            # OPTIMIZED: Shorter, more direct prompt for faster processing
            prompt = f"""Analyze this football match data and extract key information.

Match: {team_a} vs {team_b}

DATA:
{search_data}

Extract and format these sections:
- FORM: Recent results for both teams
- HEAD_TO_HEAD: Recent meetings between them
- LEAGUE_POSITION: Current standings for both
- SUMMARY: 2-3 sentence match overview
- INSIGHTS: 3 key analytical points
- VERDICT: Match prediction (2 sentences)

Use this EXACT format:

FORM:
[data]

HEAD_TO_HEAD:
[data]

LEAGUE_POSITION:
[data]

SUMMARY:
[data]

INSIGHTS:
[data]

VERDICT:
[data]"""

            # Get LLM response (handle different response formats)
            response = llm.invoke(prompt)
            if isinstance(response, str):
                # Ollama returns string directly
                content = response
            else:
                # OpenAI and Gemini return message objects
                content = response.content
            
            # Parse the structured response
            sections = {
                "form": "",
                "head_to_head": "",
                "league_position": "",
                "summary": "",
                "insights": "",
                "verdict": ""
            }
            
            current_section = None
            lines = content.strip().split('\n')
            
            for line in lines:
                line_upper = line.strip().upper()
                
                # Detect section headers
                if line_upper.startswith("FORM:"):
                    current_section = "form"
                    continue
                elif line_upper.startswith("HEAD_TO_HEAD:") or line_upper.startswith("HEAD-TO-HEAD:"):
                    current_section = "head_to_head"
                    continue
                elif line_upper.startswith("LEAGUE_POSITION:") or line_upper.startswith("LEAGUE POSITION:"):
                    current_section = "league_position"
                    continue
                elif line_upper.startswith("SUMMARY:"):
                    current_section = "summary"
                    continue
                elif line_upper.startswith("INSIGHTS:") or line_upper.startswith("KEY INSIGHTS:"):
                    current_section = "insights"
                    continue
                elif line_upper.startswith("VERDICT:") or line_upper.startswith("FINAL VERDICT:"):
                    current_section = "verdict"
                    continue
                
                # Append content to current section
                if current_section and line.strip():
                    sections[current_section] += line + "\n"
            
            # Clean up sections
            for key in sections:
                sections[key] = sections[key].strip()
            
            # Ensure we have minimum content
            if not sections["summary"]:
                sections["summary"] = f"Match Analysis: {team_a} vs {team_b}"
            if not sections["form"]:
                sections["form"] = f"Form data for {team_a} and {team_b} - see search results above."
            if not sections["head_to_head"]:
                sections["head_to_head"] = "Head-to-head data unavailable or limited."
            if not sections["league_position"]:
                sections["league_position"] = "League position data - see search results above."
            if not sections["insights"]:
                sections["insights"] = f"This match between {team_a} and {team_b} should be competitive."
            if not sections["verdict"]:
                sections["verdict"] = "Expected to be a closely contested match."
            
            logger.info("Successfully generated LLM-powered analysis from comprehensive search")
            
            return AnalysisDetail(
                summary=sections["summary"],
                form=sections["form"],
                head_to_head=sections["head_to_head"],
                league_position=sections["league_position"],
                insights=sections["insights"],
                final_verdict=sections["verdict"]
            )
            
        except Exception:
            logger.exception("Error using LLM synthesis, falling back to rule-based")
    else:
        logger.info("No LLM configured, using rule-based synthesis")
    
    # Fallback to simple rule-based synthesis
    summary = (
        f"Match Analysis: {team_a} vs {team_b}. "
        f"Analysis based on available live data from web sources."
    )
    
    # Simple extraction attempts from search data
    form = f"Recent form data for {team_a} and {team_b}:\n{search_data[:500]}..."
    head_to_head = "Head-to-head history available in search data above."
    league_position = f"League positions for {team_a} and {team_b} - refer to search data."
    
    insights = (
        f"Based on available data, both {team_a} and {team_b} are preparing for this match. "
        f"Form, league position, and head-to-head records will influence the outcome."
    )
    
    verdict = f"This match between {team_a} and {team_b} should be competitive based on current data."
    
    return AnalysisDetail(
        summary=summary,
        form=form,
        head_to_head=head_to_head,
        league_position=league_position,
        insights=insights,
        final_verdict=verdict
    )


async def run_analysis(query: str) -> AnalysisResponse:
    """
    Main agent function: orchestrates comprehensive search and analysis.
    
    This is the public interface for the football analysis agent.
    It's called by the service layer and returns a structured response.
    
    Args:
        query: Natural language query about a football match
    
    Returns:
        AnalysisResponse with comprehensive match analysis
    
    OPTIMIZED Architecture:
        1. Parse query to extract team names
        2. Single comprehensive Tavily search for all data
        3. LLM extracts and structures all sections from search results
        4. Return typed response
        
    Performance: 1 Tavily search instead of 7 (85% reduction in API calls)
    """
    logger.info(f"Football agent processing query: {query}")
    
    # Step 1: Extract team names from query
    team_a, team_b = extract_teams(query)
    
    if not team_a or not team_b:
        logger.warning("Could not extract teams from query, using default analysis")
        # Fallback for queries that don't match expected patterns
        return AnalysisResponse(
            analysis=AnalysisDetail(
                summary=f"Analysis requested: {query}",
                form="Unable to extract team names from query. Please use format: 'Analyze Team A vs Team B'",
                head_to_head="N/A",
                league_position="N/A",
                insights="Try rephrasing your query with clear team names separated by 'vs' or 'v'.",
                final_verdict="Please provide a clearer match query."
            )
        )
    
    # Step 2: Single comprehensive search for all data
    logger.info(f"Performing comprehensive search for {team_a} vs {team_b}")
    
    try:
        client = get_tavily_client()
        
        # ONE search instead of 7
        search_data = await client.search_comprehensive_match_analysis(team_a, team_b)
        
        if not search_data:
            logger.warning("No search data returned from Tavily")
            return AnalysisResponse(
                analysis=AnalysisDetail(
                    summary=f"Unable to find data for {team_a} vs {team_b}",
                    form="No data available from search",
                    head_to_head="No data available",
                    league_position="No data available",
                    insights="Unable to gather sufficient data for analysis.",
                    final_verdict="Insufficient data to make a prediction."
                )
            )
        
        logger.info("Comprehensive search completed successfully")
        
        # Step 3: Synthesize the analysis from comprehensive data
        analysis = synthesize_analysis(team_a, team_b, search_data)
        
        logger.info("Analysis synthesis complete")
        return AnalysisResponse(analysis=analysis)
        
    except Exception as e:
        logger.exception(f"Error during analysis: {str(e)}")
        # Return a graceful error response
        return AnalysisResponse(
            analysis=AnalysisDetail(
                summary=f"Error analyzing {team_a} vs {team_b}",
                form=f"Error: {str(e)}",
                head_to_head="N/A",
                league_position="N/A",
                insights="An error occurred while gathering match data.",
                final_verdict="Unable to complete analysis due to technical error."
            )
        )
