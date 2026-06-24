"""
config/settings.py — Application settings via pydantic-settings.

Values are read from environment variables or a .env file at startup.
Import the `settings` singleton wherever config is needed — never read
os.environ directly elsewhere in the codebase.
"""

from pydantic_settings import BaseSettings
from typing import Union
import os


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables or .env file.
    
    Design decision: All config lives here. Other modules import `settings`
    rather than reading os.environ directly. This makes testing easier and
    provides a single place to document all config values.
    
    For Render deployment:
    - Set environment variables in Render dashboard
    - ALLOWED_ORIGINS should be comma-separated: "https://your-app.onrender.com,https://www.yourapp.com"
    """
    
    # API Keys
    openai_api_key: str = ""
    football_api_key: str = ""
    
    # Application
    environment: str = "development"
    log_level: str = "INFO"
    
    # Server (used for documentation, actual port set via uvicorn CLI)
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS — in production, set to your actual frontend domain
    # Can be a comma-separated string or list
    allowed_origins: Union[str, list[str]] = "http://localhost:5173"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Singleton instance — import this in other modules
settings = Settings()
