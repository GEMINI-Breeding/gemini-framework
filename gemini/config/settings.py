from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os
from enum import Enum
from typing import Any
from dotenv import load_dotenv, find_dotenv, dotenv_values

class GEMINISettingsType(str, Enum):
    META = "meta"
    DB = "db"
    LOGGER = "logger"
    STORAGE = "storage"
    REST_API = "rest_api"
    SCHEDULER_DB = "scheduler_db"
    SCHEDULER_SERVER = "scheduler_server"

class GEMINISettings(BaseSettings):

    # Meta
    GEMINI_DEBUG : bool = False
    GEMINI_LOCAL : bool = False
    GEMINI_DOMAIN : str = "localhost"

    # Database Configuration
    GEMINI_DB_CONTAINER_NAME : str = "gemini-db"
    GEMINI_DB_IMAGE_NAME : str = "gemini/db"
    GEMINI_DB_USER : str = "gemini"
    GEMINI_DB_PASSWORD : str = "gemini"
    GEMINI_DB_HOSTNAME : str = "gemini-db"
    GEMINI_DB_NAME : str = "gemini"
    GEMINI_DB_PORT : int = 5432

    # Logger Configuration
    GEMINI_LOGGER_CONTAINER_NAME : str = "gemini-logger"
    GEMINI_LOGGER_IMAGE_NAME : str = "gemini/logger"
    GEMINI_LOGGER_HOSTNAME : str = "gemini-logger"
    GEMINI_LOGGER_PORT : int = 6379
    GEMINI_LOGGER_PASSWORD : str = "gemini"

    # File Store Configuration
    GEMINI_STORAGE_CONTAINER_NAME : str = "gemini-storage"
    GEMINI_STORAGE_IMAGE_NAME : str = "gemini/storage"
    GEMINI_STORAGE_HOSTNAME : str = "gemini-storage"
    GEMINI_STORAGE_PORT : int = 9000
    GEMINI_STORAGE_API_PORT : int = 9001
    GEMINI_STORAGE_ROOT_USER : str = "gemini_root"
    GEMINI_STORAGE_ROOT_PASSWORD : str = "gemini_root"
    GEMINI_STORAGE_BUCKET_NAME : str = "gemini"
    GEMINI_STORAGE_ACCESS_KEY : str = "gemini_storage_user"
    GEMINI_STORAGE_SECRET_KEY : str = "gemini_secret"

    # REST API Configuration
    GEMINI_REST_API_CONTAINER_NAME : str = "gemini-rest-api"
    GEMINI_REST_API_IMAGE_NAME : str = "gemini/rest-api"
    GEMINI_REST_API_HOSTNAME : str = "gemini-rest-api"
    GEMINI_REST_API_PORT : int = 7777

    # Scheduler DB
    GEMINI_SCHEDULER_DB_CONTAINER_NAME : str = "gemini-scheduler-db"
    GEMINI_SCHEDULER_DB_IMAGE_NAME : str = "gemini/scheduler-db"
    GEMINI_SCHEDULER_DB_HOSTNAME : str = "gemini-scheduler-db"
    GEMINI_SCHEDULER_DB_USER: str = "gemini"  # User for scheduler DB
    GEMINI_SCHEDULER_DB_PASSWORD: str = "gemini"
    GEMINI_SCHEDULER_DB_NAME: str = "gemini_scheduler"  # Database name for scheduler
    GEMINI_SCHEDULER_DB_PORT: int = 6432  # Port for scheduler DB

    # Scheduler Server
    GEMINI_SCHEDULER_SERVER_CONTAINER_NAME : str = "gemini-scheduler-server"
    GEMINI_SCHEDULER_SERVER_IMAGE_NAME : str = "gemini/scheduler-server"
    GEMINI_SCHEDULER_SERVER_HOSTNAME : str = "gemini-scheduler-server"
    GEMINI_SCHEDULER_SERVER_PORT : int = 4200

    def model_post_init(self, __context: Any) -> None:
        is_local = self.GEMINI_LOCAL
        if is_local:
            os.environ["GEMINI_LOCAL"] = "True"
            os.environ["GEMINI_DB_HOSTNAME"] = "localhost"
            os.environ["GEMINI_LOGGER_HOSTNAME"] = "localhost"
            os.environ["GEMINI_STORAGE_HOSTNAME"] = "localhost"
            os.environ["GEMINI_SCHEDULER_DB_HOSTNAME"] = "localhost"
            os.environ["GEMINI_SCHEDULER_SERVER_HOSTNAME"] = "localhost"
        return super().model_post_init(__context)

    @staticmethod
    def from_env_file(self, input_env_file_path: str) -> "GEMINISettings":
        if not os.path.exists(input_env_file_path):
            raise FileNotFoundError(f"Environment file {input_env_file_path} not found.")
        config = dotenv_values(input_env_file_path)
        settings = GEMINISettings.model_validate(config)
        return settings
    
    def create_env_file(self, env_file_path: str) -> str:
        dict = self.model_dump()
        with open(env_file_path, 'w') as f:
            for key, value in dict.items():
                f.write(f"{key}={value}\n")
        return env_file_path
    
    @staticmethod
    def get_settings(settings_type: GEMINISettingsType = GEMINISettingsType.META) -> dict:
        
        current_settings = GEMINISettings()
        match settings_type:
            case GEMINISettingsType.META:
                return {
                    "GEMINI_DEBUG": current_settings.GEMINI_DEBUG,
                    "GEMINI_LOCAL": current_settings.GEMINI_LOCAL,
                    "GEMINI_DOMAIN": current_settings.GEMINI_DOMAIN
                }
            case GEMINISettingsType.DB:
                return {
                    "GEMINI_DB_CONTAINER_NAME": current_settings.GEMINI_DB_CONTAINER_NAME,
                    "GEMINI_DB_IMAGE_NAME": current_settings.GEMINI_DB_IMAGE_NAME,
                    "GEMINI_DB_USER": current_settings.GEMINI_DB_USER,
                    "GEMINI_DB_PASSWORD": current_settings.GEMINI_DB_PASSWORD,
                    "GEMINI_DB_HOSTNAME": current_settings.GEMINI_DB_HOSTNAME if not current_settings.GEMINI_LOCAL else "localhost",
                    "GEMINI_DB_NAME": current_settings.GEMINI_DB_NAME,
                    "GEMINI_DB_PORT": current_settings.GEMINI_DB_PORT
                }
            case GEMINISettingsType.LOGGER:
                return {
                    "GEMINI_LOGGER_CONTAINER_NAME": current_settings.GEMINI_LOGGER_CONTAINER_NAME,
                    "GEMINI_LOGGER_IMAGE_NAME": current_settings.GEMINI_LOGGER_IMAGE_NAME,
                    "GEMINI_LOGGER_HOSTNAME": current_settings.GEMINI_LOGGER_HOSTNAME if not current_settings.GEMINI_LOCAL else "localhost",
                    "GEMINI_LOGGER_PORT": current_settings.GEMINI_LOGGER_PORT,
                    "GEMINI_LOGGER_PASSWORD": current_settings.GEMINI_LOGGER_PASSWORD
                }
            case GEMINISettingsType.STORAGE:

                current_settings.GEMINI_STORAGE_HOSTNAME = current_settings.GEMINI_DOMAIN if not current_settings.GEMINI_LOCAL else "localhost"
                return {
                    "GEMINI_STORAGE_CONTAINER_NAME": current_settings.GEMINI_STORAGE_CONTAINER_NAME,
                    "GEMINI_STORAGE_IMAGE_NAME": current_settings.GEMINI_STORAGE_IMAGE_NAME,
                    "GEMINI_STORAGE_HOSTNAME": current_settings.GEMINI_STORAGE_HOSTNAME if not current_settings.GEMINI_LOCAL else "localhost",
                    "GEMINI_STORAGE_PORT": current_settings.GEMINI_STORAGE_PORT,
                    "GEMINI_STORAGE_API_PORT": current_settings.GEMINI_STORAGE_API_PORT,
                    "GEMINI_STORAGE_ROOT_USER": current_settings.GEMINI_STORAGE_ROOT_USER,
                    "GEMINI_STORAGE_ROOT_PASSWORD": current_settings.GEMINI_STORAGE_ROOT_PASSWORD,
                    "GEMINI_STORAGE_ACCESS_KEY": current_settings.GEMINI_STORAGE_ACCESS_KEY,
                    "GEMINI_STORAGE_SECRET_KEY": current_settings.GEMINI_STORAGE_SECRET_KEY,
                    "GEMINI_STORAGE_BUCKET_NAME": current_settings.GEMINI_STORAGE_BUCKET_NAME
                }
            case GEMINISettingsType.REST_API:
                return {
                    "GEMINI_REST_API_CONTAINER_NAME": current_settings.GEMINI_REST_API_CONTAINER_NAME,
                    "GEMINI_REST_API_IMAGE_NAME": current_settings.GEMINI_REST_API_IMAGE_NAME,
                    "GEMINI_REST_API_HOSTNAME": current_settings.GEMINI_REST_API_HOSTNAME if not current_settings.GEMINI_LOCAL else "localhost",
                    "GEMINI_REST_API_PORT": current_settings.GEMINI_REST_API_PORT
                }
            case GEMINISettingsType.SCHEDULER_DB:
                return {
                    "GEMINI_SCHEDULER_DB_CONTAINER_NAME": current_settings.GEMINI_SCHEDULER_DB_CONTAINER_NAME,
                    "GEMINI_SCHEDULER_DB_IMAGE_NAME": current_settings.GEMINI_SCHEDULER_DB_IMAGE_NAME,
                    "GEMINI_SCHEDULER_DB_HOSTNAME": current_settings.GEMINI_SCHEDULER_DB_HOSTNAME if not current_settings.GEMINI_LOCAL else "localhost",
                    "GEMINI_SCHEDULER_DB_USER": current_settings.GEMINI_SCHEDULER_DB_USER,
                    "GEMINI_SCHEDULER_DB_PASSWORD": current_settings.GEMINI_SCHEDULER_DB_PASSWORD,
                    "GEMINI_SCHEDULER_DB_NAME": current_settings.GEMINI_SCHEDULER_DB_NAME,
                    "GEMINI_SCHEDULER_DB_PORT": current_settings.GEMINI_SCHEDULER_DB_PORT
                }
            case GEMINISettingsType.SCHEDULER_SERVER:
                return {
                    "GEMINI_SCHEDULER_SERVER_CONTAINER_NAME": current_settings.GEMINI_SCHEDULER_SERVER_CONTAINER_NAME,
                    "GEMINI_SCHEDULER_SERVER_IMAGE_NAME": current_settings.GEMINI_SCHEDULER_SERVER_IMAGE_NAME,
                    "GEMINI_SCHEDULER_SERVER_HOSTNAME": current_settings.GEMINI_SCHEDULER_SERVER_HOSTNAME if not current_settings.GEMINI_LOCAL else "localhost",
                    "GEMINI_SCHEDULER_SERVER_PORT": current_settings.GEMINI_SCHEDULER_SERVER_PORT
                }
            case _:
                raise ValueError(f"Unknown settings type: {settings_type}")
            
