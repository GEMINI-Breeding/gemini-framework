from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, Type
from typing import TypeAlias
from dotenv import load_dotenv, find_dotenv

class GEMINISettings(BaseSettings):

    # Database Configuration
    GEMINI_DB_CONTAINER_NAME : Optional[str] = None
    GEMINI_DB_IMAGE_NAME : Optional[str] = None
    GEMINI_DB_USER : Optional[str] = None
    GEMINI_DB_PASSWORD : Optional[str] = None
    GEMINI_DB_HOSTNAME : Optional[str] = None
    GEMINI_DB_NAME : Optional[str] = None
    GEMINI_DB_PORT : Optional[int] = None

    # Logger Configuration
    GEMINI_LOGGER_CONTAINER_NAME : Optional[str] = None
    GEMINI_LOGGER_IMAGE_NAME : Optional[str] = None
    GEMINI_LOGGER_HOSTNAME : Optional[str] = None
    GEMINI_LOGGER_PORT : Optional[int] = None
    GEMINI_LOGGER_PASSWORD : Optional[str] = None

    # File Store Configuration
    GEMINI_STORAGE_CONTAINER_NAME : Optional[str] = None
    GEMINI_STORAGE_IMAGE_NAME : Optional[str] = None
    GEMINI_STORAGE_HOSTNAME : Optional[str] = None
    GEMINI_STORAGE_PORT : Optional[int] = None
    GEMINI_STORAGE_API_PORT : Optional[int] = None
    GEMINI_STORAGE_ROOT_USER : Optional[str] = None
    GEMINI_STORAGE_ROOT_PASSWORD : Optional[str] = None
    GEMINI_STORAGE_ACCESS_KEY : Optional[str] = None
    GEMINI_STORAGE_SECRET_KEY : Optional[str] = None
    GEMINI_STORAGE_BUCKET_NAME : Optional[str] = None

    @staticmethod
    def from_env_file(env_file_path: str) -> "GEMINISettings":
        if not env_file_path:
            env_file_path = find_dotenv()
        load_dotenv(env_file_path)
        return GEMINISettings()




