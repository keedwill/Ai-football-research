"""
tools/stats_tool.py — Tool: get season statistics for a team.

Returns comprehensive season statistics including goals, xG, and tactical data.
Currently uses mock data for popular Premier League teams.
"""


def get_team_statistics(team_name: str) -> str:
    """
    Get comprehensive season statistics for a team.
    
    Args:
        team_name: Name of the team
    
    Returns:
        String with detailed season statistics
    """
    from ..utils.constants import MANCHESTER_UNITED, MANCHESTER_CITY
    
    # Normalize team name
    normalized_name = team_name.strip().title()
    
    # Handle abbreviations
    abbreviations = {
        "Man United": MANCHESTER_UNITED,
        "Man Utd": MANCHESTER_UNITED,
        "United": MANCHESTER_UNITED,
        "Man City": MANCHESTER_CITY,
        "City": MANCHESTER_CITY,
        "Spurs": "Tottenham"
    }
    
    normalized_name = abbreviations.get(normalized_name, normalized_name)
    
    # Mock season statistics
    mock_stats = {
        "Arsenal": {
            "goals_scored": 71,
            "goals_conceded": 28,
            "xg_for": 68.4,
            "xg_against": 25.2,
            "shots_per_game": 17.2,
            "possession_avg": 61.3,
            "pass_accuracy": 87.5,
            "clean_sheets": 14,
            "home_record": "13W-2D-0L",
            "away_record": "9W-4D-2L"
        },
        "Chelsea": {
            "goals_scored": 52,
            "goals_conceded": 48,
            "xg_for": 54.8,
            "xg_against": 46.3,
            "shots_per_game": 14.8,
            "possession_avg": 56.7,
            "pass_accuracy": 85.2,
            "clean_sheets": 8,
            "home_record": "9W-3D-3L",
            "away_record": "5W-4D-6L"
        },
        "Manchester United": {
            "goals_scored": 48,
            "goals_conceded": 45,
            "xg_for": 52.1,
            "xg_against": 43.7,
            "shots_per_game": 13.5,
            "possession_avg": 54.2,
            "pass_accuracy": 83.8,
            "clean_sheets": 9,
            "home_record": "10W-2D-3L",
            "away_record": "6W-3D-6L"
        },
        "Liverpool": {
            "goals_scored": 75,
            "goals_conceded": 30,
            "xg_for": 72.6,
            "xg_against": 28.8,
            "shots_per_game": 18.4,
            "possession_avg": 63.1,
            "pass_accuracy": 88.2,
            "clean_sheets": 15,
            "home_record": "14W-1D-0L",
            "away_record": "10W-2D-3L"
        },
        "Manchester City": {
            "goals_scored": 72,
            "goals_conceded": 34,
            "xg_for": 70.8,
            "xg_against": 31.5,
            "shots_per_game": 17.9,
            "possession_avg": 65.4,
            "pass_accuracy": 89.7,
            "clean_sheets": 13,
            "home_record": "13W-1D-1L",
            "away_record": "9W-3D-3L"
        },
        "Tottenham": {
            "goals_scored": 61,
            "goals_conceded": 46,
            "xg_for": 58.3,
            "xg_against": 44.1,
            "shots_per_game": 15.6,
            "possession_avg": 52.8,
            "pass_accuracy": 82.4,
            "clean_sheets": 10,
            "home_record": "11W-2D-2L",
            "away_record": "7W-3D-5L"
        }
    }
    
    if normalized_name in mock_stats:
        stats = mock_stats[normalized_name]
        
        return (
            f"{normalized_name} Season Statistics (30 games):\n"
            f"    Goals Scored: {stats['goals_scored']}\n"
            f"    Goals Conceded: {stats['goals_conceded']}\n"
            f"    Goal Difference: +{stats['goals_scored'] - stats['goals_conceded']}\n"
            f"    Expected Goals (xG): {stats['xg_for']}\n"
            f"    Expected Goals Against (xGA): {stats['xg_against']}\n"
            f"    Shots per Game: {stats['shots_per_game']}\n"
            f"    Possession Average: {stats['possession_avg']}%\n"
            f"    Pass Accuracy: {stats['pass_accuracy']}%\n"
            f"    Clean Sheets: {stats['clean_sheets']}\n"
            f"    Home Record: {stats['home_record']}\n"
            f"    Away Record: {stats['away_record']}"
        )
    else:
        # Generic response for teams not in mock data
        return (
            f"{team_name} Season Statistics:\n"
            f"    Goals: 40 scored, 45 conceded\n"
            f"    (Detailed mock data not available)"
        )
