from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.site import Site
from gemini.api.sensor import Sensor
from gemini.api.season import Season
from gemini.api.cultivar import Cultivar
from gemini.api.dataset import Dataset
from gemini.api.trait import Trait
from gemini.api.model import Model
from gemini.api.procedure import Procedure
from gemini.api.script import Script
from gemini.api.sensor_platform import SensorPlatform

from gemini.db.models.experiments import ExperimentModel

from datetime import date


class Experiment(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "experiment_id"))

    experiment_name: str
    experiment_info: Optional[dict] = None
    experiment_start_date: Optional[date] = None
    experiment_end_date: Optional[date] = None


    @classmethod
    def create(
        cls,
        experiment_name: str,
        experiment_info: dict = {},
        experiment_start_date: date = date.today(),
        experiment_end_date: date = date.today(),
    ) -> "Experiment":
        try:
            db_instance = ExperimentModel.get_or_create(
                experiment_name=experiment_name,
                experiment_info=experiment_info,
                experiment_start_date=experiment_start_date,
                experiment_end_date=experiment_end_date,
            )
            experiment = cls.model_validate(db_instance)
            return experiment
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, experiment_name: str) -> "Experiment":
        try:
            db_instance = ExperimentModel.get_by_parameters(
                experiment_name=experiment_name,
            )
            experiment = cls.model_validate(db_instance)
            return experiment
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Experiment":
        try:
            db_instance = ExperimentModel.get(id)
            experiment = cls.model_validate(db_instance)
            return experiment
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["Experiment"]:
        try:
            experiments = ExperimentModel.all()
            experiments = [cls.model_validate(experiment) for experiment in experiments]
            return experiments
        except Exception as e:
            raise e

    @classmethod
    def search(cls, **search_parameters) -> List["Experiment"]:
        try:
            experiments = ExperimentModel.search(**search_parameters)
            experiments = [cls.model_validate(experiment) for experiment in experiments]
            return experiments if experiments else None
        except Exception as e:
            raise e
        
    def update(self, **kwargs) -> "Experiment":
        try:
            curent_id = self.id
            experiment = ExperimentModel.get(curent_id)
            experiment = ExperimentModel.update(experiment, **kwargs)
            experiment = self.model_validate(experiment)
            self.refresh()
            return experiment
        except Exception as e:
            raise e
        

    def refresh(self) -> "Experiment":
        try:
            db_instance = ExperimentModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            raise e
        

    def delete(self) -> bool:
        try:
            current_id = self.id
            experiment = ExperimentModel.get(current_id)
            ExperimentModel.delete(experiment)
            return True
        except Exception as e:
            return False
        

    def get_seasons(self) -> List[Season]:
        try:
            seasons = self.seasons
            seasons = [Season.model_validate(season) for season in seasons]
            return seasons
        except Exception as e:
            raise e

    def get_sites(self) -> List[Site]:
        try:
            sites = self.sites
            sites = [Site.model_validate(site) for site in sites]
            return sites
        except Exception as e:
            raise e
        
    def get_sensors(self) -> List[Sensor]:
        try:
            sensors = self.sensors
            sensors = [Sensor.model_validate(sensor) for sensor in sensors]
            return sensors
        except Exception as e:
            raise e
        
    def get_cultivars(self) -> List[Cultivar]:
        try:
            cultivars = self.cultivars
            cultivars = [Cultivar.model_validate(cultivar) for cultivar in cultivars]
            return cultivars
        except Exception as e:
            raise e
        
    def get_datasets(self) -> List[Dataset]:
        try:
            datasets = self.datasets
            datasets = [Dataset.model_validate(dataset) for dataset in datasets]
            return datasets
        except Exception as e:
            raise e
        
    def get_traits(self) -> List[Trait]:
        try:
            traits = self.traits
            traits = [Trait.model_validate(trait) for trait in traits]
            return traits
        except Exception as e:
            raise e
        

    def get_models(self) -> List[Model]:
        try:
            models = self.models
            models = [Model.model_validate(model) for model in models]
            return models
        except Exception as e:
            raise e
        

    def get_procedures(self) -> List[Procedure]:
        try:
            procedures = self.procedures
            procedures = [Procedure.model_validate(procedure) for procedure in procedures]
            return procedures
        except Exception as e:
            raise e
        

    def get_scripts(self) -> List[Script]:
        try:
            scripts = self.scripts
            scripts = [Script.model_validate(script) for script in scripts]
            return scripts
        except Exception as e:
            raise e
        

    def get_platforms(self) -> List[SensorPlatform]:
        try:
            sensor_platforms = self.sensor_platforms
            sensor_platforms = [SensorPlatform.model_validate(sensor_platform) for sensor_platform in sensor_platforms]
            return sensor_platforms
        except Exception as e:
            raise e