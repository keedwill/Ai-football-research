"""
utils/exceptions.py — Custom exception classes for better error handling.

Provides domain-specific exceptions with proper status codes and messages.
"""

from fastapi import HTTPException, status


class AIFootballException(Exception):
    """Base exception for all AI Football Research System errors."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class TeamNotFoundError(AIFootballException):
    """Raised when a team cannot be found or extracted from query."""
    
    def __init__(self, query: str):
        message = f"Could not identify teams in query: '{query}'. Please use format: 'Team A vs Team B'"
        super().__init__(message, status_code=400)


class DataFetchError(AIFootballException):
    """Raised when external API data fetch fails."""
    
    def __init__(self, source: str, details: str = ""):
        message = f"Failed to fetch data from {source}"
        if details:
            message += f": {details}"
        super().__init__(message, status_code=503)


class LLMError(AIFootballException):
    """Raised when LLM synthesis fails."""
    
    def __init__(self, details: str = ""):
        message = "LLM analysis generation failed"
        if details:
            message += f": {details}"
        super().__init__(message, status_code=500)


class InvalidQueryError(AIFootballException):
    """Raised when query validation fails."""
    
    def __init__(self, reason: str):
        message = f"Invalid query: {reason}"
        super().__init__(message, status_code=400)


class ConfigurationError(AIFootballException):
    """Raised when system configuration is invalid."""
    
    def __init__(self, setting: str):
        message = f"Configuration error: {setting} is not properly set"
        super().__init__(message, status_code=500)


def create_http_exception(exc: AIFootballException) -> HTTPException:
    """
    Convert custom exception to FastAPI HTTPException.
    
    Args:
        exc: Custom AIFootballException instance
    
    Returns:
        HTTPException suitable for FastAPI response
    """
    return HTTPException(
        status_code=exc.status_code,
        detail={
            "error": exc.__class__.__name__,
            "message": exc.message
        }
    )
