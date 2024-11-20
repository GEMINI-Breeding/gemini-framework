from pydantic import BaseModel, ConfigDict
from python_on_whales import DockerClient
from python_on_whales import Container, Network

from pathlib import Path
from enum import Enum

from gemini.config.settings import GEMINISettings

class GEMINIPipelineStatus(Enum):
    BUILDING = "BUILDING"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"


class GEMINIContainerManager(BaseModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    pipeline_compose_file: str = Path(__file__).parent / "compose.yaml"
    pipeline_env_file: str = Path(__file__).parent / ".env.example"
    pipeline_settings: GEMINISettings = None
    pipeline_status: GEMINIPipelineStatus = GEMINIPipelineStatus.STOPPED

    docker_client: DockerClient = None

    # Containers
    db_container: Container = None
    logger_container: Container = None
    storage_container: Container = None

    def build_images(self) -> bool:
        try:
            # Build the images
            self.docker_client.compose.build()
            self.pipeline_status = GEMINIPipelineStatus.BUILDING
            return True
        except Exception as e:
            print(e)
            return False
        

    def start_containers(self) -> bool:
        try:
            # Start the containers
            self.docker_client.compose.up(detach=True)
            self.pipeline_status = GEMINIPipelineStatus.RUNNING
            return True
        except Exception as e:
            print(e)
            return False
        
    def stop_containers(self) -> bool:
        try:
            # Stop the containers
            self.docker_client.compose.down()
            self.pipeline_status = GEMINIPipelineStatus.STOPPED
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


    def get_pipeline_info(self) -> dict:
        return {
            "pipeline_status": self.pipeline_status,
            "containers": {
                "db": self.db_container,
                "logger": self.logger_container,
                "storage": self.storage_container
            },
            "images": {
                "db": self.pipeline_settings.GEMINI_DB_IMAGE_NAME,
                "logger": self.pipeline_settings.GEMINI_LOGGER_IMAGE_NAME,
                "storage": self.pipeline_settings.GEMINI_STORAGE_IMAGE_NAME
            },
            "networks": self.docker_client.network.list()
        }

    def setup(self) -> bool:
        try:

            # Check Pipeline Settings
            if not self.pipeline_settings:
                self.pipeline_settings = GEMINISettings.from_env_file(self.pipeline_env_file)

            # Get the docker client
            client = DockerClient(
                compose_files=[self.pipeline_compose_file]
            )
            self.docker_client = client

            # Build the images
            self.build_images()

            # Start the containers
            self.start_containers()

            # Get the containers
            self.scan_containers()

        except Exception as e:
            return False



if __name__ == "__main__":
    manager = GEMINIContainerManager()
    manager.setup()
    print(manager.get_pipeline_info())
