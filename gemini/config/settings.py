from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Any, Optional, Type
from typing import TypeAlias
from dotenv import load_dotenv, find_dotenv
from enum import Enum
from gemini.db.config import DatabaseConfig
from gemini.storage.config import StorageConfig, MinioStorageConfig
from gemini.logger.config import LoggerConfig, RedisLoggerConfig



class GEMINISettings(BaseSettings):

    # Meta
    GEMINI_DEBUG : Optional[bool] = False
    GEMINI_LOCAL : Optional[bool] = False

    # Database Configuration
    GEMINI_DB_CONTAINER_NAME : Optional[str] = "gemini-db"
    GEMINI_DB_IMAGE_NAME : Optional[str] = "gemini/db"
    GEMINI_DB_USER : Optional[str] = "gemini"
    GEMINI_DB_PASSWORD : Optional[str] = "gemini"
    GEMINI_DB_HOSTNAME : Optional[str] = "gemini-db"
    GEMINI_DB_NAME : Optional[str] = "gemini"
    GEMINI_DB_PORT : Optional[int] = 5432

    # Logger Configuration
    GEMINI_LOGGER_CONTAINER_NAME : Optional[str] = "gemini-logger"
    GEMINI_LOGGER_IMAGE_NAME : Optional[str] = "gemini/logger"
    GEMINI_LOGGER_HOSTNAME : Optional[str] = "gemini-logger"
    GEMINI_LOGGER_PORT : Optional[int] = 6379
    GEMINI_LOGGER_PASSWORD : Optional[str] = "gemini"

    # File Store Configuration
    GEMINI_STORAGE_CONTAINER_NAME : Optional[str] = "gemini-storage"
    GEMINI_STORAGE_IMAGE_NAME : Optional[str] = "gemini/storage"
    GEMINI_STORAGE_HOSTNAME : Optional[str] = "gemini-storage"
    GEMINI_STORAGE_PORT : Optional[int] = 9000
    GEMINI_STORAGE_API_PORT : Optional[int] = 9001
    GEMINI_STORAGE_ROOT_USER : Optional[str] = "gemini_root"
    GEMINI_STORAGE_ROOT_PASSWORD : Optional[str] = "gemini_root"
    GEMINI_STORAGE_ACCESS_KEY : Optional[str] = "gemini_storage_user"
    GEMINI_STORAGE_SECRET_KEY : Optional[str] = "gemini_secret"
    GEMINI_STORAGE_BUCKET_NAME : Optional[str] = "gemini"


    # REST API Configuration
    GEMINI_REST_API_CONTAINER_NAME : Optional[str] = "gemini-rest-api"
    GEMINI_REST_API_IMAGE_NAME : Optional[str] = "gemini/rest-api"
    GEMINI_REST_API_HOSTNAME : Optional[str] = "gemini-rest-api"
    GEMINI_REST_API_PORT : Optional[int] = 7777

    def model_post_init(self, __context: Any) -> None:
        is_local = self.GEMINI_LOCAL
        if is_local:
            self.GEMINI_DB_HOSTNAME = "localhost"
            self.GEMINI_LOGGER_HOSTNAME = "localhost"
            self.GEMINI_STORAGE_HOSTNAME = "localhost"
        return super().model_post_init(__context)

    @staticmethod
    def from_env_file(env_file_path: str) -> "GEMINISettings":
        if not env_file_path:
            env_file_path = find_dotenv()
        load_dotenv(env_file_path)
        return GEMINISettings()


    def create_env_file(self, env_file_path: str) -> str:
        dict = self.model_dump()
        with open(env_file_path, 'w') as f:
            for key, value in dict.items():
                f.write(f"{key}={value}\n")
        return env_file_path
    


    def get_database_config(self) -> DatabaseConfig:

        database_url = f"postgresql://{self.GEMINI_DB_USER}:{self.GEMINI_DB_PASSWORD}@{self.GEMINI_DB_HOSTNAME}:{self.GEMINI_DB_PORT}/{self.GEMINI_DB_NAME}"
        config = DatabaseConfig(
            database_url=database_url
        )
        return config

        
    def get_logger_config(self) -> LoggerConfig:

        config = RedisLoggerConfig(
            host=self.GEMINI_LOGGER_HOSTNAME,
            port=self.GEMINI_LOGGER_PORT,
            db=0,
            password=self.GEMINI_LOGGER_PASSWORD
        )

        return config
    
    def get_storage_config(self) -> StorageConfig:

        config = MinioStorageConfig(
            endpoint=f"{self.GEMINI_STORAGE_HOSTNAME}:{self.GEMINI_STORAGE_PORT}",
            access_key=self.GEMINI_STORAGE_ACCESS_KEY,
            secret_key=self.GEMINI_STORAGE_SECRET_KEY,
            bucket_name=self.GEMINI_STORAGE_BUCKET_NAME,
            secure=False
        )

        return config