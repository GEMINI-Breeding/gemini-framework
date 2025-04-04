from pydantic import BaseModel, ConfigDict, PrivateAttr
from pathlib import Path
from python_on_whales import DockerClient
from python_on_whales import Container

from gemini.logger.interfaces import logger_provider
from gemini.logger.providers.redis_logger import RedisLogger

from gemini.storage.interfaces import storage_provider
from gemini.storage.providers.minio_storage import MinioStorageProvider

from gemini.config.settings import GEMINISettings

from enum import Enum
from typing import Any, ClassVar

class GEMINIComponent(str, Enum):
    LOGGER = "logger"
    STORAGE = "storage"
    DB = "db"

class GEMINIManager:

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    _shared_state: ClassVar[dict] = PrivateAttr(default={})

    compose_file: str = Path(__file__).parent / "pipeline" / "docker-compose.yaml"
    env_file: str = Path(__file__).parent / "pipeline" / ".env"
    docker_client: DockerClient = DockerClient(
        compose_files=[compose_file]
    )

    # Pipeline Settings
    pipeline_settings: GEMINISettings = GEMINISettings()

    def model_post_init(self, __context: Any) -> None:
        return super().model_post_init(__context)
    
    def save_settings(self, settings: GEMINISettings) -> None:
        self.pipeline_settings = settings
        settings.create_env_file(self.env_file)
        print(f"Settings saved to {self.env_file}")

    def build(self) -> bool:
        try:
            self.docker_client.compose.build(cache=False)
            return True
        except Exception as e:
            print(e)
            return False
        
    def rebuild(self) -> bool:
        try:
            self.docker_client.compose.down(volumes=True)
            self.docker_client.compose.build()
            self.docker_client.compose.up(detach=True)
            return True
        except Exception as e:
            print(e)
            return False

    def start(self) -> bool:
        try:
            self.docker_client.compose.up(detach=True)
            return True
        except Exception as e:
            print(e)
            return False
        
    def clean(self) -> bool:
        try:
            self.docker_client.compose.down(volumes=True, remove_orphans=True)
            return True
        except Exception as e:
            print(e)
            return False
        
    def stop(self) -> bool:
        try:
            self.docker_client.compose.stop()
            return True
        except Exception as e:
            print(e)
            return False
        
    def set_domain(self, domain: str) -> None:
        self.pipeline_settings.GEMINI_DOMAIN = domain
        self.save_settings(self.pipeline_settings)
        print(f"Domain set to {domain}")

