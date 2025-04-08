from enum import Enum
from pathlib import Path
from typing import Any
import subprocess, os

import docker
from docker import DockerClient
from pydantic import BaseModel, ConfigDict, PrivateAttr

from gemini.config.settings import GEMINISettings
from gemini.logger.interfaces import logger_provider
from gemini.logger.providers.redis_logger import RedisLogger
from gemini.storage.interfaces import storage_provider
from gemini.storage.providers.minio_storage import MinioStorageProvider

class GEMINIComponentType(str, Enum):
    META = "meta"
    DB = "db"
    LOGGER = "logger"
    STORAGE = "storage"
    REST_API = "rest_api"
    SCHEDULER_DB = "scheduler_db"
    SCHEDULER_SERVER = "scheduler_server"

class GEMINIContainerInfo(BaseModel):
    id: str
    image: str
    name: str
    ip_address: str


class GEMINIManager(BaseModel):
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

    env_file_path : str = Path(__file__).parent / "pipeline" / ".env"
    compose_file_path : str = Path(__file__).parent / "pipeline" / "docker-compose.yaml"
    docker_client: DockerClient = docker.from_env()

    # Pipeline Settings
    pipeline_settings: GEMINISettings = GEMINISettings()

    docker_containers: dict[str, GEMINIContainerInfo] = {}

    def model_post_init(self, __context: Any) -> None:
        self.scan_containers()
        return super().model_post_init(__context)
    
    def scan_containers(self) -> None:
        try:
            containers = self.docker_client.containers.list()
            for container in containers:
                container_info = container.attrs
                container_name = container_info["Name"].strip("/")
                container_image = container_info["Config"]["Image"]
                container_id = container_info["Id"]
                container_gemini_network = container_info["NetworkSettings"]["Networks"].get("gemini_network")
                container_ip = container_gemini_network["IPAddress"]

                self.docker_containers[container_name] = GEMINIContainerInfo(
                    id=container_id,
                    image=container_image,
                    name=container_name,
                    ip_address=container_ip
                )
        except Exception as e:
            print(f"Error scanning containers: {e}")

    def save_settings(self) -> None:
        # Delete current settings if they exist
        self.delete_settings()
        # Create a new settings file
        current_settings = self.get_settings()
        current_settings.create_env_file(self.env_file_path)
        self.pipeline_settings = current_settings
        print(f"Settings saved to {self.env_file_path}")


    def get_settings(self) -> GEMINISettings:
        current_settings = GEMINISettings()
        return current_settings
    
    def set_setting(self, setting_name: str, setting_value: Any) -> None:
        current_settings = GEMINISettings()
        if hasattr(current_settings, setting_name):
            current_settings.set_setting(setting_name, setting_value)
            self.save_settings()
        else:
            raise KeyError(f"Setting {setting_name} does not exist in GEMINISettings.")
        

    
    def delete_settings(self) -> None:
        try:
            os.remove(self.env_file_path)
            print(f"Settings file {self.env_file_path} deleted.")
        except Exception as e:
            print(f"Error deleting settings file: {e}")
    
    def build(self) -> bool:
        try:
            subprocess.run(
                ["docker", "compose", "-f", self.compose_file_path, "--env-file", self.env_file_path, "build"],
                check=True
            )
            return True
        except Exception as e:
            print(e)
            return False
        
    def rebuild(self) -> bool:
        try:
            subprocess.run(
                ["docker", "compose", "-f", self.compose_file_path, "--env-file", self.env_file_path, "down", "--remove-orphans"],
                check=True
            )
            subprocess.run(
                ["docker", "compose", "-f", self.compose_file_path, "--env-file", self.env_file_path, "build"],
                check=True
            )
            subprocess.run(
                ["docker", "compose", "-f", self.compose_file_path, "--env-file", self.env_file_path, "up", "--detach"],
                check=True
            )
            return True
        except Exception as e:
            print(e)
            return False
        
    def start(self) -> bool:
        try:
            subprocess.run(
                ["docker", "compose", "-f", self.compose_file_path, "--env-file", self.env_file_path, "up", "--detach"],
                check=True
            )
            return True
        except Exception as e:
            print(e)
            return False
        
    def clean(self) -> bool:
        try:
            subprocess.run(
                ["docker", "compose", "-f", self.compose_file_path, "--env-file", self.env_file_path, "down", "--volumes", "--remove-orphans"],
                check=True
            )
            return True
        except Exception as e:
            print(e)
            return False
        
    def stop(self) -> bool:
        try:
            subprocess.run(
                ["docker","compose", "-f", self.compose_file_path, "--env-file", self.env_file_path, "stop"],
                check=True
            )
            return True
        except Exception as e:
            print(e)
            return False


    def update(self) -> bool:
        try:
            # Get update.sh script
            update_script_path = Path(__file__).parent / "scripts" / "update.sh"
            subprocess.run(
                ["bash", str(update_script_path)],
                check=True
            )
            return True
        except Exception as e:
            print(e)
            return False



    def get_component_settings(self, component_type: GEMINIComponentType) -> dict:
        current_settings = self.get_settings()
        match component_type:
            case GEMINIComponentType.META:
                return {
                    "GEMINI_DEBUG": current_settings.GEMINI_DEBUG,
                    "GEMINI_LOCAL": current_settings.GEMINI_LOCAL,
                    "GEMINI_PUBLIC_DOMAIN": current_settings.GEMINI_PUBLIC_DOMAIN
                }
            case GEMINIComponentType.DB:
                return {
                    "GEMINI_DB_CONTAINER_NAME": current_settings.GEMINI_DB_CONTAINER_NAME,
                    "GEMINI_DB_IMAGE_NAME": current_settings.GEMINI_DB_IMAGE_NAME,
                    "GEMINI_DB_USER": current_settings.GEMINI_DB_USER,
                    "GEMINI_DB_PASSWORD": current_settings.GEMINI_DB_PASSWORD,
                    "GEMINI_DB_HOSTNAME": current_settings.GEMINI_DB_HOSTNAME if not current_settings.GEMINI_LOCAL else "localhost",
                    "GEMINI_DB_NAME": current_settings.GEMINI_DB_NAME,
                    "GEMINI_DB_PORT": current_settings.GEMINI_DB_PORT
                }
            case GEMINIComponentType.LOGGER:
                return {
                    "GEMINI_LOGGER_CONTAINER_NAME": current_settings.GEMINI_LOGGER_CONTAINER_NAME,
                    "GEMINI_LOGGER_IMAGE_NAME": current_settings.GEMINI_LOGGER_IMAGE_NAME,
                    "GEMINI_LOGGER_HOSTNAME": current_settings.GEMINI_LOGGER_HOSTNAME if not current_settings.GEMINI_LOCAL else "localhost",
                    "GEMINI_LOGGER_PORT": current_settings.GEMINI_LOGGER_PORT,
                    "GEMINI_LOGGER_PASSWORD": current_settings.GEMINI_LOGGER_PASSWORD
                }
            case GEMINIComponentType.STORAGE:
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
            case GEMINIComponentType.REST_API:
                return {
                    "GEMINI_REST_API_CONTAINER_NAME": current_settings.GEMINI_REST_API_CONTAINER_NAME,
                    "GEMINI_REST_API_IMAGE_NAME": current_settings.GEMINI_REST_API_IMAGE_NAME,
                    "GEMINI_REST_API_HOSTNAME": current_settings.GEMINI_REST_API_HOSTNAME if not current_settings.GEMINI_LOCAL else "localhost",
                    "GEMINI_REST_API_PORT": current_settings.GEMINI_REST_API_PORT
                }
            case GEMINIComponentType.SCHEDULER_DB:
                return {
                    "GEMINI_SCHEDULER_DB_CONTAINER_NAME": current_settings.GEMINI_SCHEDULER_DB_CONTAINER_NAME,
                    "GEMINI_SCHEDULER_DB_IMAGE_NAME": current_settings.GEMINI_SCHEDULER_DB_IMAGE_NAME,
                    "GEMINI_SCHEDULER_DB_HOSTNAME": current_settings.GEMINI_SCHEDULER_DB_HOSTNAME if not current_settings.GEMINI_LOCAL else "localhost",
                    "GEMINI_SCHEDULER_DB_USER": current_settings.GEMINI_SCHEDULER_DB_USER,
                    "GEMINI_SCHEDULER_DB_PASSWORD": current_settings.GEMINI_SCHEDULER_DB_PASSWORD,
                    "GEMINI_SCHEDULER_DB_NAME": current_settings.GEMINI_SCHEDULER_DB_NAME,
                    "GEMINI_SCHEDULER_DB_PORT": current_settings.GEMINI_SCHEDULER_DB_PORT
                }
            case GEMINIComponentType.SCHEDULER_SERVER:
                return {
                    "GEMINI_SCHEDULER_SERVER_CONTAINER_NAME": current_settings.GEMINI_SCHEDULER_SERVER_CONTAINER_NAME,
                    "GEMINI_SCHEDULER_SERVER_IMAGE_NAME": current_settings.GEMINI_SCHEDULER_SERVER_IMAGE_NAME,
                    "GEMINI_SCHEDULER_SERVER_HOSTNAME": current_settings.GEMINI_SCHEDULER_SERVER_HOSTNAME if not current_settings.GEMINI_LOCAL else "localhost",
                    "GEMINI_SCHEDULER_SERVER_PORT": current_settings.GEMINI_SCHEDULER_SERVER_PORT
                }
            case _:
                raise ValueError(f"Unknown settings type: {component_type}")
