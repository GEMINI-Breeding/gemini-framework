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





# # GEMINI Database Configuration
# GEMINI_DB_CONTAINER_NAME=gemini-db
# GEMINI_DB_IMAGE_NAME=gemini/db
# GEMINI_DB_USER=gemini
# GEMINI_DB_PASSWORD=gemini
# GEMINI_DB_HOSTNAME=gemini-db
# GEMINI_DB_NAME=gemini
# GEMINI_DB_PORT=5432

# # GEMINI Logger Configuration
# GEMINI_LOGGER_CONTAINER_NAME=gemini-logger
# GEMINI_LOGGER_IMAGE_NAME=gemini/logger
# GEMINI_LOGGER_HOSTNAME=gemini-logger
# GEMINI_LOGGER_PORT=6379
# GEMINI_LOGGER_PASSWORD=gemini

# # GEMINI File Store
# GEMINI_STORAGE_CONTAINER_NAME=gemini-storage
# GEMINI_STORAGE_IMAGE_NAME=gemini/storage
# GEMINI_STORAGE_HOSTNAME=gemini-storage
# GEMINI_STORAGE_PORT=9000
# GEMINI_STORAGE_API_PORT=9001
# GEMINI_STORAGE_ROOT_USER=gemini_root
# GEMINI_STORAGE_ROOT_PASSWORD=gemini_root
# GEMINI_STORAGE_ACCESS_KEY=gemini_storage_user
# GEMINI_STORAGE_SECRET_KEY=gemini_secret
# GEMINI_STORAGE_BUCKET_NAME=gemini

