from typing import Any, Optional, List
from gemini.api.base import APIBase
from gemini.api.cultivar import Cultivar
from gemini.models import PlantModel
from gemini.logger import logger_service

class Plant(APIBase):

    db_model = PlantModel

    plot_id: Optional[str] = None
    plant_number: int
    plant_info: Optional[dict] = None

    cultivar: Optional[Cultivar] = None

    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.plant_number} from the database")
        return self.plant_info
    
    def set_info(self, plant_info: Optional[dict] = None) -> "Plant":
        self.update(plant_info=plant_info)
        logger_service.info("API", f"Set information about {self.plant_number} in the database")
        return self
    
    def add_info(self, plant_info: Optional[dict] = None) -> "Plant":
        current_info = self.get_info()
        updated_info = {**current_info, **plant_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.plant_number} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Plant":
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.plant_number} in the database")
        return self
    
    def get_cultivar(self) -> Cultivar:
        self.refresh()
        logger_service.info("API", f"Retrieved cultivar information for {self.plant_number} from the database")
        return self.cultivar
    
    # Todo: Custom Search Function
    # Todo: Plant based on Plot Parameters

