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
from app.services.tavily_client import get_tavily_client
from app.models.analysis import AnalysisDetail, AnalysisResponse
from app.config.settings import settings
from app.utils.logger import get_logger

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
    form_a: str,
    form_b: str,
    h2h: str,
    league_a: str,
    league_b: str,
    stats_a: str,
    stats_b: str
) -> AnalysisDetail:
    """
    Synthesize tool outputs into structured analysis using LLM.
    
    Uses Ollama (development) or OpenAI (production) to generate intelligent insights.
    Falls back to rule-based synthesis if LLM is unavailable.
    """
    # Try LLM-powered synthesis
    llm_available = settings.use_ollama or settings.openai_api_key
   
    
    if llm_available:
        try:
            if settings.use_ollama:
                logger.info(f"Using Ollama ({settings.ollama_model}) for analysis synthesis")
                llm = Ollama(
                    model=settings.ollama_model,
                    base_url=settings.ollama_base_url,
                    temperature=0.7
                )
            else:
                logger.info("Using OpenAI LLM for analysis synthesis")
                llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.7,
                    api_key=settings.openai_api_key
                )
            
            # Construct comprehensive prompt
            prompt = f"""You are a professional football analyst. Analyze the following match data and provide structured insights.

Match: {team_a} vs {team_b}

RECENT FORM:
{team_a}:
{form_a}

{team_b}:
{form_b}

HEAD-TO-HEAD RECORD:
{h2h}

LEAGUE POSITIONS:
{league_a}

{league_b}

SEASON STATISTICS:
{team_a}:
{stats_a}

{team_b}:
{stats_b}

Based on this data, provide:
1. A brief summary (2-3 sentences)
2. 3-4 key insights analyzing form, league position, and statistics
3. A final verdict on the expected outcome (2-3 sentences)

Be specific, analytical, and reference the actual data. Focus on tactical and statistical observations."""

            # Get LLM response
            if settings.use_ollama:
                # Ollama returns string directly
                content = llm.invoke(prompt)
            else:
                # OpenAI returns message object
                response = llm.invoke(prompt)
                content = response.content
            
            # Parse LLM response (simple split-based parsing)
            lines = content.strip().split('\n')
            
            # Extract sections (this is a simple heuristic parser)
            summary_text = ""
            insights_text = ""
            verdict_text = ""
            
            current_section = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect section headers
                if "summary" in line.lower() or line.startswith("1."):
                    current_section = "summary"
                    continue
                elif "insight" in line.lower() or line.startswith("2."):
                    current_section = "insights"
                    continue
                elif "verdict" in line.lower() or "outcome" in line.lower() or line.startswith("3."):
                    current_section = "verdict"
                    continue
                
                # Append to appropriate section
                if current_section == "summary":
                    summary_text += line + " "
                elif current_section == "insights":
                    insights_text += line + " "
                elif current_section == "verdict":
                    verdict_text += line + " "
            
            # Fallback: if parsing failed, use simple split
            if not summary_text or not insights_text or not verdict_text:
                parts = content.split('\n\n')
                summary_text = parts[0] if len(parts) > 0 else f"Match Analysis: {team_a} vs {team_b}"
                insights_text = parts[1] if len(parts) > 1 else content
                verdict_text = parts[-1] if len(parts) > 2 else "Expected to be a competitive match."
            
            # Clean up
            summary_text = summary_text.strip() or f"Match Analysis: {team_a} vs {team_b}"
            insights_text = insights_text.strip() or content
            verdict_text = verdict_text.strip() or "This should be an interesting match."
            
            # Combine form data for display
            form = f"{team_a}:\n{form_a}\n\n{team_b}:\n{form_b}"
            league_position = f"{league_a}\n\n{league_b}"
            
            logger.info("Successfully generated LLM-powered analysis")
            
            return AnalysisDetail(
                summary=summary_text,
                form=form,
                head_to_head=h2h,
                league_position=league_position,
                insights=insights_text,
                final_verdict=verdict_text
            )
            
        except Exception:
            logger.exception("Error using LLM synthesis, falling back to rule-based")
    else:
        logger.info("OPENAI_API_KEY not set, using rule-based synthesis")
    
    # Fallback to rule-based synthesis
    summary = (
        f"Match Analysis: {team_a} vs {team_b}. "
        f"Based on current form, league position, head-to-head record, "
        f"and season statistics."
    )
    
    form = f"{team_a}:\n{form_a}\n\n{team_b}:\n{form_b}"
    head_to_head = h2h
    league_position = f"{league_a}\n\n{league_b}"
    
    # Generate insights based on the data
    insights = []
    
    if "WWW" in form_a and "LLL" in form_b:
        insights.append(f"{team_a} are in excellent form while {team_b} are struggling.")
    elif "WWW" in form_b and "LLL" in form_a:
        insights.append(f"{team_b} are in excellent form while {team_a} are struggling.")
    
    if "Position: 1" in league_a or "Position: 2" in league_a:
        insights.append(f"{team_a} are title contenders with strong league position.")
    if "Position: 1" in league_b or "Position: 2" in league_b:
        insights.append(f"{team_b} are title contenders with strong league position.")
    
    if "xG:" in stats_a and "xG:" in stats_b:
        insights.append("Both teams show strong attacking metrics this season.")
    
    insights_text = " ".join(insights) if insights else (
        f"Both {team_a} and {team_b} have shown competitive performances this season."
    )
    
    team_a_wins = form_a.count("(W)")
    team_b_wins = form_b.count("(W)")
    
    if team_a_wins > team_b_wins + 1:
        verdict = f"{team_a} enter this match with momentum and better recent form."
    elif team_b_wins > team_a_wins + 1:
        verdict = f"{team_b} enter this match with momentum and better recent form."
    else:
        verdict = f"This is expected to be a closely contested match between {team_a} and {team_b}."
    
    return AnalysisDetail(
        summary=summary,
        form=form,
        head_to_head=head_to_head,
        league_position=league_position,
        insights=insights_text,
        final_verdict=verdict
    )


async def run_analysis(query: str) -> AnalysisResponse:
    """
    Main agent function: orchestrates tool calls and synthesizes analysis.
    
    This is the public interface for the football analysis agent.
    It's called by the service layer and returns a structured response.
    
    Args:
        query: Natural language query about a football match
    
    Returns:
        AnalysisResponse with comprehensive match analysis
    
    Architecture:
        1. Parse query to extract team names
        2. Call all relevant tools in parallel (form, h2h, league, stats)
        3. Synthesize tool outputs into structured analysis
        4. Return typed response
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
    
    # Step 2: Call all tools to gather data
    logger.info(f"Calling tools for {team_a} vs {team_b}")
    
    try:
        # Get form for both teams
        form_a = get_team_form(team_a)
        form_b = get_team_form(team_b)
        
        # Get head-to-head record
        h2h = get_head_to_head(team_a, team_b)
        
        # Get league positions
        league_a = get_league_position(team_a)
        league_b = get_league_position(team_b)
        
        # Get season statistics
        stats_a = get_team_statistics(team_a)
        stats_b = get_team_statistics(team_b)
        
        logger.info("All tools executed successfully")
        
        # Step 3: Synthesize the analysis
        analysis = synthesize_analysis(
            team_a, team_b,
            form_a, form_b, h2h,
            league_a, league_b,
            stats_a, stats_b
        )
        
        logger.info("Analysis synthesis complete")
        return AnalysisResponse(analysis=analysis)
        
    except Exception as e:
        logger.exception(f"Error during tool execution: {str(e)}")
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
