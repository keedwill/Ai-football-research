"""
utils/logger.py — Centralised logging configuration.

Call `get_logger(__name__)` in any module to get a pre-configured logger
that writes structured output (level, timestamp, module name).
"""

import logging
import sys
from app.config.settings import settings


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger for the given module name.
    
    Design decision: All logging goes through this function. It ensures
    consistent formatting and makes it easy to add features like JSON
    structured logs or external log shipping later.
    
    Usage:
        logger = get_logger(__name__)
        logger.info("Processing request")
        logger.error("Failed to connect", exc_info=True)
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured (avoid duplicate handlers)
    if not logger.handlers:
        logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
        
        # Console handler with structured format
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Prevent propagation to root logger (avoids duplicate logs)
        logger.propagate = False
    
    return logger
