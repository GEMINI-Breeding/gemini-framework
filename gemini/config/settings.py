from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, Type
from typing import TypeAlias
from dotenv import load_dotenv, find_dotenv

class GEMINISettings(BaseSettings):

    # Database Configuration
    GEMINI_DB_CONTAINER_NAME : Optional[str] = "gemini-db"
    GEMINI_DB_IMAGE_NAME : Optional[str] = "gemini/db"
    GEMINI_DB_USER : Optional[str] = None
    GEMINI_DB_PASSWORD : Optional[str] = None
    GEMINI_DB_HOSTNAME : Optional[str] = "gemini-db"
    GEMINI_DB_NAME : Optional[str] = None
    GEMINI_DB_PORT : Optional[int] = 5432

    # Logger Configuration
    GEMINI_LOGGER_CONTAINER_NAME : Optional[str] = "gemini-logger"
    GEMINI_LOGGER_IMAGE_NAME : Optional[str] = "gemini/logger"
    GEMINI_LOGGER_HOSTNAME : Optional[str] = "gemini-logger"
    GEMINI_LOGGER_PORT : Optional[int] = 6379
    GEMINI_LOGGER_PASSWORD : Optional[str] = None

    # File Store Configuration
    GEMINI_STORAGE_CONTAINER_NAME : Optional[str] = "gemini-storage"
    GEMINI_STORAGE_IMAGE_NAME : Optional[str] = "gemini/storage"
    GEMINI_STORAGE_HOSTNAME : Optional[str] = "gemini-storage"
    GEMINI_STORAGE_PORT : Optional[int] = 9000
    GEMINI_STORAGE_API_PORT : Optional[int] = 9001
    GEMINI_STORAGE_ROOT_USER : Optional[str] = None
    GEMINI_STORAGE_ROOT_PASSWORD : Optional[str] = None
    GEMINI_STORAGE_ACCESS_KEY : Optional[str] = None
    GEMINI_STORAGE_SECRET_KEY : Optional[str] = None
    GEMINI_STORAGE_BUCKET_NAME : Optional[str] = "gemini"

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
    


    def get_database_config(self) -> dict:
        return {
            "container_name": self.GEMINI_DB_CONTAINER_NAME,
            "image_name": self.GEMINI_DB_IMAGE_NAME,
            "user": self.GEMINI_DB_USER,
            "password": self.GEMINI_DB_PASSWORD,
            "hostname": self.GEMINI_DB_HOSTNAME,
            "port": self.GEMINI_DB_PORT,
            "database": self.GEMINI_DB_NAME
        }
    
    def get_logger_config(self) -> dict:
        return {
            "container_name": self.GEMINI_LOGGER_CONTAINER_NAME,
            "image_name": self.GEMINI_LOGGER_IMAGE_NAME,
            "hostname": self.GEMINI_LOGGER_HOSTNAME,
            "port": self.GEMINI_LOGGER_PORT,
            "password": self.GEMINI_LOGGER_PASSWORD
        }
    
    def get_storage_config(self) -> dict:
        return {
            "container_name": self.GEMINI_STORAGE_CONTAINER_NAME,
            "image_name": self.GEMINI_STORAGE_IMAGE_NAME,
            "hostname": self.GEMINI_STORAGE_HOSTNAME,
            "port": self.GEMINI_STORAGE_PORT,
            "api_port": self.GEMINI_STORAGE_API_PORT,
            "root_user": self.GEMINI_STORAGE_ROOT_USER,
            "root_password": self.GEMINI_STORAGE_ROOT_PASSWORD,
            "access_key": self.GEMINI_STORAGE_ACCESS_KEY,
            "secret_key": self.GEMINI_STORAGE_SECRET_KEY,
            "bucket_name": self.GEMINI_STORAGE_BUCKET_NAME
        }

