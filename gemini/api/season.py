from typing import Optional, List, Any, Union
from gemini.api.base import APIBase
from gemini.models import SeasonModel, ExperimentModel
from gemini.logger import logger_service
from datetime import datetime, date
from uuid import UUID


class Season(APIBase):

    db_model = SeasonModel

    season_name: str
    season_info: Optional[dict] = None
    season_start_date: Optional[date] = None
    season_end_date: Optional[date] = None
    experiment_id: Optional[Union[str, UUID]] = None

    @classmethod
    def get(cls, experiment_name: str, season_name: str) -> "Season":
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        db_instance = SeasonModel.get_by_parameters(experiment_id=db_experiment.id, season_name=season_name)
        logger_service.info("API", f"Retrieved season with name {season_name} from the database")
        return cls.model_validate(db_instance)

    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.season_name} from the database")
        return self.season_info
    
    def set_info(self, season_info: Optional[dict] = None) -> "Season":
        self.update(season_info=season_info)
        logger_service.info("API", f"Set information about {self.season_name} in the database")
        return self
    
    def add_info(self, season_info: Optional[dict] = None) -> "Season":
        current_info = self.get_info()
        updated_info = {**current_info, **season_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.season_name} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Season":
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.season_name} in the database")
        return self
        