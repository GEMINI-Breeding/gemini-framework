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
    pipeline_settings: GEMINISettings = None

    docker_client: DockerClient = None

    def build_images(self) -> bool:
        try:
            # Build the images
            self.docker_client.compose.build()


            return True
        except Exception as e:
            print(e)
            return False



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

        except Exception as e:
            return False



if __name__ == "__main__":
    manager = GEMINIContainerManager()
    manager.setup()
