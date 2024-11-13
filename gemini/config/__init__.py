"""
GEMINI Framework Configuration Module

This module provides centralized configuration management for the GEMINI framework,
integrating configurations from all services (database, logger, storage).

Example usage:
    from gemini.config import settings
    
    # Get service configs
    db_config = settings.get_database_config()
    logger_config = settings.get_logger_config()
    storage_config = settings.get_storage_config()
"""

from gemini.config.settings import Settings

# Create singleton settings instance
settings = Settings()

# Export manager for CLI tool
from gemini.config.env import EnvManager

__all__ = ['settings', 'EnvManager']