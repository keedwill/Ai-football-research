"""
test_tools.py — Test script for football data tools.

Demonstrates all tool functions with mock data.
"""

from app.tools.form_tool import get_team_form
from app.tools.h2h_tool import get_head_to_head
from app.tools.league_tool import get_league_position
from app.tools.stats_tool import get_team_statistics


def test_form_tool():
    print("=" * 70)
    print("TEST 1: Team Form Tool")
    print("=" * 70)
    
    teams = ["Arsenal", "Chelsea", "Liverpool"]
    for team in teams:
        print(f"\n{get_team_form(team)}\n")


def test_h2h_tool():
    print("=" * 70)
    print("TEST 2: Head-to-Head Tool")
    print("=" * 70)
    
    matchups = [
        ("Arsenal", "Chelsea"),
        ("Liverpool", "Manchester United"),
        ("Manchester City", "Tottenham")
    ]
    
    for team_a, team_b in matchups:
        print(f"\n{get_head_to_head(team_a, team_b)}\n")


def test_league_tool():
    print("=" * 70)
    print("TEST 3: League Position Tool")
    print("=" * 70)
    
    teams = ["Liverpool", "Arsenal", "Manchester City", "Chelsea"]
    for team in teams:
        print(f"\n{get_league_position(team)}\n")


def test_stats_tool():
    print("=" * 70)
    print("TEST 4: Team Statistics Tool")
    print("=" * 70)
    
    teams = ["Arsenal", "Manchester United"]
    for team in teams:
        print(f"\n{get_team_statistics(team)}\n")


def test_abbreviations():
    print("=" * 70)
    print("TEST 5: Abbreviation Handling")
    print("=" * 70)
    
    print("\nTesting 'Man United' abbreviation:")
    print(get_league_position("Man United"))
    
    print("\nTesting 'City' abbreviation:")
    print(get_team_form("City"))
    
    print("\nTesting 'Spurs' abbreviation:")
    print(get_team_statistics("Spurs"))


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print(" FOOTBALL TOOLS TEST SUITE")
    print("=" * 70 + "\n")
    
    test_form_tool()
    test_h2h_tool()
    test_league_tool()
    test_stats_tool()
    test_abbreviations()
    
    print("\n" + "=" * 70)
    print(" ALL TESTS COMPLETED ✓")
    print("=" * 70 + "\n")
