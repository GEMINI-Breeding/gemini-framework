from typing import Optional, List, Any
from gemini.api.base import APIBase
from gemini.api.season import Season
from gemini.api.sensor import Sensor
from gemini.api.trait import Trait
from gemini.api.resource import Resource
from gemini.api.site import Site
from gemini.api.cultivar import Cultivar
from gemini.api.model import Model
from gemini.api.procedure import Procedure
from gemini.api.script import Script
from gemini.api.dataset import Dataset
from gemini.models import ExperimentModel, SeasonModel
from gemini.logger import logger_service

from datetime import datetime, date


class Experiment(APIBase):

    db_model = ExperimentModel

    experiment_name: str
    experiment_info: Optional[dict] = None
    experiment_start_date: Optional[date] = None
    experiment_end_date: Optional[date] = None

    seasons: Optional[List[Season]] = None
    sites: Optional[List[Site]] = None
    sensors: Optional[List[Sensor]] = None
    traits: Optional[List[Trait]] = None
    resources: Optional[List[Resource]] = None
    cultivars: Optional[List[Cultivar]] = None
    datasets: Optional[List[Dataset]] = None
    scripts: Optional[List[Script]] = None
    procedures: Optional[List[Procedure]] = None
    models: Optional[List[Model]] = None


    @classmethod
    def create(
        cls,
        experiment_name: str,
        experiment_info: dict = None,
        experiment_start_date: date = None,
        experiment_end_date: date = None,
    ) -> "Experiment":
        
        db_instance = cls.db_model.get_or_create(
            experiment_name=experiment_name,
            experiment_info=experiment_info,
            experiment_start_date=experiment_start_date,
            experiment_end_date=experiment_end_date,
        )

        logger_service.info(
            "API",
            f"Created a new experiment with name {db_instance.experiment_name} in the database",
        )

        return cls.model_validate(db_instance)
    

    @classmethod
    def get(cls, experiment_name: str) -> "Experiment":
        db_instance = cls.db_model.get_by_parameters(experiment_name=experiment_name)
        logger_service.info(
            "API",
            f"Retrieved experiment with name {experiment_name} from the database",
        )
        return cls.model_validate(db_instance) if db_instance else None
    

    def get_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved information about {self.experiment_name} from the database",
        )
        return self.experiment_info
    

    def set_info(self, experiment_info: Optional[dict] = None) -> "Experiment":
        self.update(experiment_info=experiment_info)
        logger_service.info(
            "API",
            f"Updated information about {self.experiment_name} in the database",
        )
        return self
    

    def add_info(self, experiment_info: Optional[dict] = None) -> "Experiment":
        current_info = self.get_info()
        updated_info = {**current_info, **experiment_info}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Added information to {self.experiment_name} in the database",
        )
        return self
    

    def remove_info(self, keys_to_remove: List[str]) -> "Experiment":
        current_info = self.get_info()
        updated_info = {
            key: value
            for key, value in current_info.items()
            if key not in keys_to_remove
        }
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Removed information from {self.experiment_name} in the database",
        )
        return self


