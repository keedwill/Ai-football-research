"""
test_agent.py — Comprehensive test of the football analysis agent.

Tests the agent with various query formats and team combinations.
"""

import asyncio
from app.agents.football_agent import run_analysis, extract_teams


def test_team_extraction():
    """Test the team name extraction logic."""
    print("=" * 70)
    print("TEST 1: Team Name Extraction")
    print("=" * 70 + "\n")
    
    test_queries = [
        "Analyze Arsenal vs Chelsea",
        "Liverpool vs Man United",
        "Predict Manchester City v Tottenham",
        "Who will win Arsenal versus Chelsea?",
        "Compare Man United and Liverpool",
        "Arsenal - Chelsea analysis",
        "Match analysis Liverpool against Man City"
    ]
    
    for query in test_queries:
        team_a, team_b = extract_teams(query)
        print(f"Query: '{query}'")
        print(f"  → Extracted: {team_a} vs {team_b}\n")


async def test_full_analysis():
    """Test complete analysis with different matchups."""
    print("=" * 70)
    print("TEST 2: Full Match Analysis")
    print("=" * 70 + "\n")
    
    queries = [
        "Analyze Arsenal vs Chelsea",
        "Liverpool vs Manchester United",
        "Predict Man City v Tottenham"
    ]
    
    for query in queries:
        print(f"\n{'='*70}")
        print(f"QUERY: {query}")
        print('='*70)
        
        result = await run_analysis(query)
        analysis = result.analysis
        
        print(f"\nSUMMARY:\n{analysis.summary}\n")
        print(f"FORM:\n{analysis.form}\n")
        print(f"HEAD-TO-HEAD:\n{analysis.head_to_head}\n")
        print(f"LEAGUE POSITION:\n{analysis.league_position}\n")
        print(f"INSIGHTS:\n{analysis.insights}\n")
        print(f"VERDICT:\n{analysis.final_verdict}\n")


async def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n" + "=" * 70)
    print("TEST 3: Edge Cases")
    print("=" * 70 + "\n")
    
    edge_queries = [
        "What's the weather?",  # No team names
        "Just testing",         # Invalid format
        "Analyze Arsenal",      # Only one team
    ]
    
    for query in edge_queries:
        print(f"Query: '{query}'")
        result = await run_analysis(query)
        print(f"  → Summary: {result.analysis.summary[:80]}...")
        print(f"  → Form: {result.analysis.form[:80]}...\n")


async def main():
    print("\n" + "=" * 70)
    print(" FOOTBALL ANALYSIS AGENT - COMPREHENSIVE TEST SUITE")
    print("=" * 70 + "\n")
    
    # Test 1: Team extraction
    test_team_extraction()
    
    # Test 2: Full analysis
    await test_full_analysis()
    
    # Test 3: Edge cases
    await test_edge_cases()
    
    print("\n" + "=" * 70)
    print(" ALL AGENT TESTS COMPLETED ✓")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
