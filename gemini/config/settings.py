"""
GEMINI Framework Settings Manager

This module handles loading and managing configuration settings from environment
variables and .env files.
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

from gemini.db.config import DatabaseConfig
from gemini.logger.config.logger_config import RedisLoggerConfig
from gemini.storage.config.storage_config import MinioStorageConfig


class Settings(BaseSettings):
    """
    Central configuration class for the GEMINI Framework.
    Loads settings from environment variables and/or .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    # Database settings
    GEMINI_DB_USER: str = "gemini"
    GEMINI_DB_PASSWORD: str = "gemini"
    GEMINI_DB_HOSTNAME: str = "gemini-db"
    GEMINI_DB_NAME: str = "gemini"
    GEMINI_DB_PORT: int = 5432

    # Logger settings
    GEMINI_LOGGER_HOSTNAME: str = "gemini-logger"
    GEMINI_LOGGER_PORT: int = 6379
    GEMINI_LOGGER_PASSWORD: str = "gemini"

    # Storage settings
    GEMINI_STORAGE_HOSTNAME: str = "gemini-storage"
    GEMINI_STORAGE_PORT: int = 9000
    GEMINI_STORAGE_API_PORT: int = 9001
    GEMINI_STORAGE_ROOT_USER: str = "gemini_root"
    GEMINI_STORAGE_ROOT_PASSWORD: str = "gemini_root"
    GEMINI_STORAGE_ACCESS_KEY: str = "gemini_storage_user"
    GEMINI_STORAGE_SECRET_KEY: str = "gemini_secret"
    GEMINI_STORAGE_BUCKET_NAME: str = "gemini"

    def get_database_config(self) -> DatabaseConfig:
        """Get database configuration."""
        return DatabaseConfig(
            database_url=f"postgresql://{self.GEMINI_DB_USER}:{self.GEMINI_DB_PASSWORD}@{self.GEMINI_DB_HOSTNAME}:{self.GEMINI_DB_PORT}/{self.GEMINI_DB_NAME}"
        )

    def get_logger_config(self) -> RedisLoggerConfig:
        """Get logger configuration."""
        return RedisLoggerConfig(
            provider="redis",
            host=self.GEMINI_LOGGER_HOSTNAME,
            port=self.GEMINI_LOGGER_PORT,
            password=self.GEMINI_LOGGER_PASSWORD,
            key_prefix="gemini:"
        )

    def get_storage_config(self) -> MinioStorageConfig:
        """Get storage configuration."""
        return MinioStorageConfig(
            provider="minio",
            endpoint=f"{self.GEMINI_STORAGE_HOSTNAME}:{self.GEMINI_STORAGE_PORT}",
            access_key=self.GEMINI_STORAGE_ACCESS_KEY,
            secret_key=self.GEMINI_STORAGE_SECRET_KEY,
            bucket_name=self.GEMINI_STORAGE_BUCKET_NAME,
            secure=False  # TODO: Make configurable if needed
        )