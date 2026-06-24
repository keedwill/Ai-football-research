"""
tools/h2h_tool.py — Tool: get head-to-head history between two teams.

Returns the recent head-to-head record between two teams.
Currently uses mock data for popular Premier League matchups.
"""


def get_head_to_head(team_a: str, team_b: str) -> str:
    """
    Get head-to-head history between two teams.
    
    Args:
        team_a: First team name
        team_b: Second team name
    
    Returns:
        String describing recent head-to-head results
    """
    from ..utils.constants import MANCHESTER_UNITED, MANCHESTER_CITY
    
    # Normalize team names
    team_a = team_a.strip().title()
    team_b = team_b.strip().title()
    
    # Handle abbreviations
    abbreviations = {
        "Man United": MANCHESTER_UNITED,
        "Man Utd": MANCHESTER_UNITED,
        "United": MANCHESTER_UNITED,
        "Man City": MANCHESTER_CITY,
        "City": MANCHESTER_CITY,
        "Spurs": "Tottenham"
    }
    
    team_a = abbreviations.get(team_a, team_a)
    team_b = abbreviations.get(team_b, team_b)
    
    # Create a consistent key for the matchup (alphabetically sorted)
    teams = tuple(sorted([team_a, team_b]))
    
    # Mock head-to-head data
    mock_h2h = {
        ("Arsenal", "Chelsea"): [
            "Arsenal 5-0 Chelsea (Apr 2024)",
            "Chelsea 2-2 Arsenal (Oct 2023)",
            "Arsenal 3-1 Chelsea (May 2023)",
            "Chelsea 0-1 Arsenal (Nov 2022)",
            "Arsenal 2-4 Chelsea (Apr 2022)"
        ],
        ("Arsenal", "Liverpool"): [
            "Arsenal 2-2 Liverpool (Dec 2023)",
            "Liverpool 1-1 Arsenal (Apr 2023)",
            "Arsenal 3-2 Liverpool (Oct 2022)",
            "Liverpool 4-0 Arsenal (Feb 2022)",
            "Arsenal 0-2 Liverpool (Nov 2021)"
        ],
        ("Arsenal", "Manchester United"): [
            "Arsenal 3-1 Man United (Sep 2023)",
            "Man United 3-2 Arsenal (Jan 2023)",
            "Arsenal 3-2 Man United (Jan 2023)",
            "Man United 0-1 Arsenal (Sep 2022)",
            "Arsenal 1-3 Man United (Apr 2022)"
        ],
        ("Chelsea", "Liverpool"): [
            "Chelsea 0-0 Liverpool (Jan 2024)",
            "Liverpool 4-1 Chelsea (Jan 2024)",
            "Chelsea 1-1 Liverpool (Aug 2023)",
            "Liverpool 0-0 Chelsea (Apr 2023)",
            "Chelsea 0-1 Liverpool (Mar 2023)"
        ],
        ("Chelsea", "Manchester United"): [
            "Man United 2-1 Chelsea (Dec 2023)",
            "Chelsea 4-1 Man United (Apr 2023)",
            "Man United 1-1 Chelsea (Oct 2022)",
            "Chelsea 1-1 Man United (Apr 2022)",
            "Man United 1-1 Chelsea (Nov 2021)"
        ],
        ("Liverpool", "Manchester United"): [
            "Liverpool 0-0 Man United (Dec 2023)",
            "Man United 2-1 Liverpool (Aug 2023)",
            "Liverpool 7-0 Man United (Mar 2023)",
            "Man United 2-1 Liverpool (Aug 2022)",
            "Liverpool 4-0 Man United (Apr 2022)"
        ],
        ("Liverpool", "Manchester City"): [
            "Man City 1-1 Liverpool (Nov 2023)",
            "Liverpool 1-1 Man City (Oct 2023)",
            "Man City 4-1 Liverpool (Apr 2023)",
            "Liverpool 1-0 Man City (Oct 2022)",
            "Man City 2-2 Liverpool (Apr 2022)"
        ],
        ("Manchester City", "Manchester United"): [
            "Man United 1-3 Man City (Oct 2023)",
            "Man City 3-0 Man United (Jan 2023)",
            "Man United 2-1 Man City (Jan 2023)",
            "Man City 6-3 Man United (Oct 2022)",
            "Man United 2-1 Man City (Jan 2022)"
        ],
        ("Arsenal", "Tottenham"): [
            "Tottenham 2-3 Arsenal (Apr 2024)",
            "Arsenal 3-2 Tottenham (Sep 2023)",
            "Tottenham 0-2 Arsenal (Jan 2023)",
            "Arsenal 3-1 Tottenham (Oct 2022)",
            "Tottenham 3-0 Arsenal (May 2022)"
        ],
        ("Chelsea", "Tottenham"): [
            "Tottenham 1-4 Chelsea (Nov 2023)",
            "Chelsea 1-1 Tottenham (May 2023)",
            "Tottenham 2-0 Chelsea (Feb 2023)",
            "Chelsea 2-2 Tottenham (Aug 2022)",
            "Tottenham 1-0 Chelsea (Jan 2022)"
        ]
    }
    
    if teams in mock_h2h:
        results = "\n    ".join(mock_h2h[teams])
        return f"Head-to-Head: {team_a} vs {team_b} (Last 5 matches):\n    {results}"
    else:
        # Generic response for matchups not in mock data
        return f"Head-to-Head: {team_a} vs {team_b}\n    Recent meetings: 2-1-2 record (mock data not available)"
