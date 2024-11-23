from typing import Any, ClassVar
from gemini.pipeline.container_manager import GEMINIContainerManager
from gemini.config.settings import GEMINISettings

from pydantic import BaseModel, ConfigDict, PrivateAttr

class GEMINIManager(BaseModel):


    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    _shared_state: ClassVar[dict] = PrivateAttr(default={})

    k: int = 0

    container_manager: GEMINIContainerManager = GEMINIContainerManager()
    settings: GEMINISettings = GEMINISettings()

    def model_post_init(self, __context: Any) -> None:
        self.__dict__ = self._shared_state
        if not self._shared_state:
            self._shared_state.update(self.__dict__)

    def apply_settings(self, settings: GEMINISettings) -> None:
        self.container_manager.apply_settings(settings)
        self.settings = settings

    def build_pipeline(self) -> bool:
        return self.container_manager.build_images()
    
    def start_pipeline(self) -> bool:
        return self.container_manager.start_containers()
    
    def stop_pipeline(self) -> bool:
        return self.container_manager.stop_containers()
    
    def clean_pipeline(self) -> bool:
        return self.container_manager.purge_containers()



if __name__ == "__main__":
    manager = GEMINIManager()
    manager.build_pipeline()