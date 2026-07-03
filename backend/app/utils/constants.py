"""
utils/constants.py — Application-wide constants.

Centralized constants to avoid magic strings and improve maintainability.
"""

# Team name constants (to avoid duplication)
MANCHESTER_UNITED = "Manchester United"
MANCHESTER_CITY = "Manchester City"
TOTTENHAM = "Tottenham"
ARSENAL = "Arsenal"
CHELSEA = "Chelsea"
LIVERPOOL = "Liverpool"

# Team abbreviations mapping
TEAM_ABBREVIATIONS = {
    "Man United": MANCHESTER_UNITED,
    "Man Utd": MANCHESTER_UNITED,
    "United": MANCHESTER_UNITED,
    "Man City": MANCHESTER_CITY,
    "City": MANCHESTER_CITY,
    "Spurs": TOTTENHAM,
}

# API Configuration (legacy constants, may be removed in future)
PREMIER_LEAGUE_ID = 39
DEFAULT_SEASON = 2023

# Response messages
ERROR_TEAM_NOT_FOUND = "Unable to extract team names from query"
ERROR_NO_DATA = "No data available for the requested teams"
ERROR_API_UNAVAILABLE = "External API temporarily unavailable"

# Validation limits
MIN_QUERY_LENGTH = 3
MAX_QUERY_LENGTH = 200
MAX_TEAM_NAME_LENGTH = 50

# HTTP Timeouts (seconds)
API_REQUEST_TIMEOUT = 10.0
LLM_REQUEST_TIMEOUT = 30.0

# Logging formats
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
