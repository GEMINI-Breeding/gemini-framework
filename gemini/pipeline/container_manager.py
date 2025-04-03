from typing import Any
from enum import Enum
from pydantic import BaseModel, ConfigDict
from python_on_whales import DockerClient
from python_on_whales import Container, Network

from pathlib import Path
from gemini.config.settings import GEMINISettings


class GEMINIContainerManager(BaseModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    pipeline_compose_file: str = Path(__file__).parent / "compose.yaml"
    pipeline_env_file: str = Path(__file__).parent / ".env.example"
    docker_client: DockerClient = None

    # Containers
    db_container: Container = None
    logger_container: Container = None
    storage_container: Container = None

    # Pipeline Settings
    pipeline_settings: GEMINISettings = GEMINISettings()

    def model_post_init(self, __context: Any) -> None:

        self.docker_client = DockerClient(
            compose_files=[self.pipeline_compose_file]
        )

        return super().model_post_init(__context)

    def apply_settings(self, settings: GEMINISettings) -> None:
        parent_folder = Path(__file__).parent
        settings.create_env_file(f"{parent_folder}/.env")
        

    def build_images(self) -> bool:
        try:
            # Build the images
            self.docker_client.compose.build(cache=False, pull=True)
            return True
        except Exception as e:
            print(e)
            return False
        
    def rebuild_images(self) -> bool:
        try:
            self.docker_client.compose.down(volumes=True)
            self.docker_client.compose.up(detach=True)
            return True
        except Exception as e:
            print(e)
            return False
        
    def start_containers(self) -> bool:
        try:
            # Start the containers
            self.docker_client.compose.up(detach=True)
            return True
        except Exception as e:
            print(e)
            return False
        
    def stop_containers(self) -> bool:
        try:
            # Stop the containers
            self.docker_client.compose.down()
            return True
        except Exception as e:
            print(e)
            return False
        
    def purge_containers(self) -> bool:
        try:
            # Purge the containers
            self.docker_client.compose.down(volumes=True, remove_orphans=True, remove_images="all")
            return True
        except Exception as e:
            print(e)
            return False
        
    def scan_containers(self) -> bool:
        try:
            # Get the containers
            containers = self.docker_client.container.list()
            for container in containers:
                if container.name == self.pipeline_settings.GEMINI_DB_CONTAINER_NAME:
                    self.db_container = container
                elif container.name == self.pipeline_settings.GEMINI_LOGGER_CONTAINER_NAME:
                    self.logger_container = container
                elif container.name == self.pipeline_settings.GEMINI_STORAGE_CONTAINER_NAME:
                    self.storage_container = container

            return True
        except Exception as e:
            print(e)
            return False
        

    def get_status(self) -> str:
        try:
            # Get the status
            running_containers = self.docker_client.compose.ps()
            if running_containers:
                return "Running"
            else:
                return "Stopped"
        except Exception as e:
            print(e)
            return "Error"

    def setup(self, pipeline_settings: GEMINISettings = None) -> bool:
        try:

            # Build the images
            self.build_images()

            # Start the containers
            self.start_containers()

            # Get the containers
            self.scan_containers()

        except Exception as e:
            return False
        
    def teardown(self) -> bool:
        try:
            # Stop the containers
            self.stop_containers()
            # Purge the containers
            self.purge_containers()
            return True
        except Exception as e:
            print(e)
            return False
        

    def stop(self) -> bool:
        try:
            # Stop the containers
            self.stop_containers()
            return True
        except Exception as e:
            print(e)
            return False

