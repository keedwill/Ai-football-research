"""
tools/league_tool.py — Tool: get current league position for a team.

Returns the current Premier League standing for a team.
Currently uses mock data representing mid-season standings.
"""


def get_league_position(team_name: str) -> str:
    """
    Get the current league position for a team.
    
    Args:
        team_name: Name of the team
    
    Returns:
        String describing league position, points, and recent position
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
    
    # Mock league table (Premier League 2023/24 mid-season)
    mock_table = {
        "Liverpool": {"position": 1, "points": 70, "played": 30, "gd": "+45"},
        "Arsenal": {"position": 2, "points": 68, "played": 30, "gd": "+43"},
        "Manchester City": {"position": 3, "points": 67, "played": 30, "gd": "+38"},
        "Aston Villa": {"position": 4, "points": 60, "played": 30, "gd": "+22"},
        "Tottenham": {"position": 5, "points": 57, "played": 30, "gd": "+15"},
        "Manchester United": {"position": 6, "points": 51, "played": 30, "gd": "+3"},
        "West Ham": {"position": 7, "points": 48, "played": 30, "gd": "+6"},
        "Chelsea": {"position": 8, "points": 45, "played": 30, "gd": "+2"},
        "Newcastle": {"position": 9, "points": 44, "played": 30, "gd": "+12"},
        "Brighton": {"position": 10, "points": 42, "played": 30, "gd": "+5"},
        "Wolves": {"position": 11, "points": 40, "played": 30, "gd": "-3"},
        "Bournemouth": {"position": 12, "points": 39, "played": 30, "gd": "-8"},
        "Fulham": {"position": 13, "points": 36, "played": 30, "gd": "-5"},
        "Crystal Palace": {"position": 14, "points": 33, "played": 30, "gd": "-10"},
        "Brentford": {"position": 15, "points": 32, "played": 30, "gd": "-9"},
        "Everton": {"position": 16, "points": 29, "played": 30, "gd": "-12"},
        "Nottingham Forest": {"position": 17, "points": 26, "played": 30, "gd": "-15"},
        "Luton": {"position": 18, "points": 24, "played": 30, "gd": "-22"},
        "Burnley": {"position": 19, "points": 20, "played": 30, "gd": "-31"},
        "Sheffield United": {"position": 20, "points": 16, "played": 30, "gd": "-45"}
    }
    
    if normalized_name in mock_table:
        data = mock_table[normalized_name]
        position = data["position"]
        points = data["points"]
        played = data["played"]
        gd = data["gd"]
        
        # Add context about league position
        context = ""
        if position <= 4:
            context = " (Champions League qualification)"
        elif position == 5:
            context = " (Europa League qualification)"
        elif position >= 18:
            context = " (Relegation zone)"
        
        return (
            f"{normalized_name} League Position:\n"
            f"    Position: {position}/20{context}\n"
            f"    Points: {points}\n"
            f"    Played: {played}\n"
            f"    Goal Difference: {gd}"
        )
    else:
        # Generic response for teams not in mock data
        return f"{team_name} League Position: Mid-table (mock data not available)"
