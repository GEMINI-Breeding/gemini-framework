from typing import Optional, List, Any
from gemini.api.base import APIBase
from gemini.api.season import Season
from gemini.api.sensor import Sensor
from gemini.api.trait import Trait
from gemini.api.resource import Resource
from gemini.api.site import Site
from gemini.api.cultivar import Cultivar
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



# from typing import Optional, List, Any, TYPE_CHECKING
# from pydantic import ConfigDict
# from gemini.api.base import APIBase
# from gemini.models import ExperimentModel, SeasonModel
# from gemini.logger import logger_service

# from datetime import datetime


# class Experiment(APIBase):

#     db_model = ExperimentModel

#     experiment_name: str
#     experiment_info: Optional[dict] = None
#     experiment_start_date: Optional[datetime] = None
#     experiment_end_date: Optional[datetime] = None

#     seasons: Optional[List[dict]] = None
#     sites: Optional[List[dict]] = None
#     sensors: Optional[List[dict]] = None
#     traits: Optional[List[dict]] = None
#     resources: Optional[List[dict]] = None
#     cultivars: Optional[List[dict]] = None
#     datasets: Optional[List[dict]] = None

#     model_config = ConfigDict(
#         arbitrary_types_allowed=True, from_attributes=True, protected_namespaces=()
#     )

#     @classmethod
#     def create(
#         cls,
#         experiment_name: str,
#         experiment_info: dict = None,
#         experiment_start_date: datetime = None,
#         experiment_end_date: datetime = None,
#     ) -> "Experiment":
#         """
#         Create a new experiment

#         Args:
#         experiment_name (str): The name of the experiment
#         experiment_info (dict, optional): The information about the experiment. Defaults to None.
#         experiment_start_date (datetime, optional): The start date of the experiment. Defaults to None.
#         experiment_end_date (datetime, optional): The end date of the experiment. Defaults to None.

#         Returns:
#         Experiment: The created experiment
#         """
#         new_instance = cls.db_model.get_or_create(
#             experiment_name=experiment_name,
#             experiment_info=experiment_info,
#             experiment_start_date=experiment_start_date,
#             experiment_end_date=experiment_end_date,
#         )

#         logger_service.info(
#             "API",
#             f"Created a new experiment with name {new_instance.experiment_name} in the database",
#         )

#         new_instance = cls.model_validate(new_instance)
#         return new_instance

#     @classmethod
#     def get_by_name(cls, experiment_name: str) -> "Experiment":
#         """
#         Get an experiment by name

#         Args:
#         experiment_name (str): The name of the experiment

#         Returns:
#         Experiment: The experiment with the given name
#         """
#         db_instance = cls.db_model.get_by_parameter("experiment_name", experiment_name)
#         logger_service.info(
#             "API",
#             f"Retrieved experiment with name {experiment_name} from the database",
#         )
#         return cls.model_validate(db_instance) if db_instance else None

#     def get_info(self) -> dict:
#         """
#         Returns:
#         dict: The information about the experiment
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved information about {self.experiment_name} from the database",
#         )
#         return self.experiment_info

#     def set_info(self, experiment_info: Optional[dict] = None) -> "Experiment":
#         """
#         Set the information about an experiment

#         Args:
#         experiment_info (Optional[dict], optional): The information to set. Defaults to None.

#         Returns:
#         Experiment: The experiment with the updated information
#         """
#         self.update(experiment_info=experiment_info)
#         logger_service.info(
#             "API",
#             f"Updated information about {self.experiment_name} in the database",
#         )
#         return self

#     def add_info(self, experiment_info: Optional[dict] = None) -> "Experiment":
#         """
#         Add information to an experiment

#         Args:
#         experiment_info (Optional[dict], optional): The information to add. Defaults to None.

#         Returns:
#         Experiment: The experiment with the added information
#         """
#         current_info = self.get_info()
#         updated_info = {**current_info, **experiment_info}
#         self.set_info(updated_info)
#         logger_service.info(
#             "API",
#             f"Added information to {self.experiment_name} in the database",
#         )
#         return self

#     def remove_info(self, keys_to_remove: List[str]) -> "Experiment":
#         """
#         Remove information from an experiment

#         Args:
#         keys_to_remove (List[str]): The keys to remove

#         Returns:
#         Experiment: The experiment with the removed information
#         """
#         current_info = self.get_info()
#         updated_info = {
#             key: value
#             for key, value in current_info.items()
#             if key not in keys_to_remove
#         }
#         self.set_info(updated_info)
#         logger_service.info(
#             "API",
#             f"Removed information from {self.experiment_name} in the database",
#         )
#         return self

#     def get_seasons(self) -> List[dict]:
#         """
#         Get all the seasons for an experiment

#         Returns:
#         List[Season]: A list of all the seasons for the experiment
#         """
#         self.refresh()
#         seasons = self.seasons
#         logger_service.info(
#             "API",
#             f"Retrieved {len(seasons)} seasons for {self.experiment_name} from the database",
#         )
#         return seasons

#     def add_season(
#         self,
#         season_name: str,
#         season_start_date: datetime = None,
#         season_end_date: datetime = None,
#         season_info: dict = None,
#     ) -> dict:

#         db_season = SeasonModel.get_or_create(
#             experiment_id=self.id,
#             season_name=season_name,
#             season_start_date=season_start_date,
#             season_end_date=season_end_date,
#             season_info=season_info,
#         )

#         logger_service.info(
#             "API",
#             f"Created a new season with name {db_season.season_name} in the database",
#         )
#         db_season = db_season.to_dict()
#         return db_season

#     def get_sites(self) -> List[dict]:
#         """
#         Get all the sites for an experiment

#         Returns:
#         List[Site]: A list of all the sites for the experiment
#         """
#         self.refresh()
#         sites = self.sites
#         logger_service.info(
#             "API",
#             f"Retrieved {len(sites)} sites for {self.experiment_name} from the database",
#         )
#         return sites

#     def get_sensors(self) -> List[dict]:
#         """
#         Get all the sensors for an experiment

#         Returns:
#         List[dict]: A list of all the sensors for the experiment
#         """
#         self.refresh()
#         sensors = self.sensors
#         logger_service.info(
#             "API",
#             f"Retrieved {len(sensors)} sensors for {self.experiment_name} from the database",
#         )
#         return sensors

#     def get_traits(self) -> List[dict]:
#         """
#         Get all the traits for an experiment

#         Returns:
#         List[dict]: A list of all the traits for the experiment
#         """
#         self.refresh()
#         traits = self.traits
#         logger_service.info(
#             "API",
#             f"Retrieved {len(traits)} traits for {self.experiment_name} from the database",
#         )
#         return traits

#     def get_resources(self) -> List[dict]:
#         """
#         Get all the resources for an experiment

#         Returns:
#         List[dict]: A list of all the resources for the experiment
#         """
#         self.refresh()
#         resources = self.resources
#         logger_service.info(
#             "API",
#             f"Retrieved {len(resources)} resources for {self.experiment_name} from the database",
#         )
#         return resources

#     def get_cultivars(self) -> List[dict]:
#         """
#         Get all the cultivars for an experiment

#         Returns:
#         List[dict]: A list of all the cultivars for the experiment
#         """
#         self.refresh()
#         cultivars = self.cultivars
#         logger_service.info(
#             "API",
#             f"Retrieved {len(cultivars)} cultivars for {self.experiment_name} from the database",
#         )
#         return cultivars
