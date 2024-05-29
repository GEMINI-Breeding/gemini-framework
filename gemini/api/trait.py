from typing import Any, Optional, List
from gemini.api.base import APIBase
from gemini.api.trait_level import TraitLevel
from gemini.api.dataset import Dataset
from gemini.api.enums import GEMINITraitLevel
from gemini.models import TraitModel, ExperimentModel, TraitLevelModel
from gemini.logger import logger_service


class Trait(APIBase):

    db_model = TraitModel

    trait_name: str
    trait_units: Optional[str] = None
    trait_level_id: Optional[int] = None
    trait_metrics: Optional[dict] = None

    trait_level: Optional[TraitLevel] = None
    datasets: Optional[List[Dataset]] = None


    @classmethod
    def create(
        cls,
        trait_name: str,
        trait_units: str = None,
        trait_level: GEMINITraitLevel = None,
        trait_metrics: dict = None,
        experiment_name: str = None,
    ):
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        db_trait_level = TraitLevelModel.get_by_parameters(trait_level_name=trait_level.name)
        db_instance = cls.db_model.get_or_create(
            trait_name=trait_name,
            trait_units=trait_units,
            trait_level_id=db_trait_level.id,
            trait_metrics=trait_metrics
        )

        if db_experiment and db_instance not in db_experiment.traits:
            db_experiment.traits.append(db_instance)
            db_experiment.save()

        instance = cls.model_validate(db_instance)
        logger_service.info(
            "API",
            f"Created a new trait with name {instance.trait_name} in the database",
        )
        return instance
    
    @classmethod
    def get_by_level(cls, trait_level: GEMINITraitLevel) -> List["Trait"]:
        db_trait_level = TraitLevelModel.get_by_parameters(trait_level_name=trait_level.name)
        db_traits = cls.db_model.search(trait_level_id=db_trait_level.id)
        traits = [cls.model_validate(trait) for trait in db_traits]
        logger_service.info(
            "API",
            f"Retrieved traits of level {trait_level.name} from the database",
        )
        return traits
    
    @classmethod
    def get(cls, trait_name: str) -> "Trait":
        db_instance = cls.db_model.get_by_parameters(trait_name=trait_name)
        logger_service.info(
            "API",
            f"Retrieved trait with name {trait_name} from the database",
        )
        return cls.model_validate(db_instance) if db_instance else None
    
    def get_level(self) -> TraitLevel:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved level of {self.trait_name} from the database",
        )
        return self.trait_level
    
    def set_level(self, trait_level: GEMINITraitLevel) -> "Trait":
        db_trait_level = TraitLevelModel.get_by_parameters(trait_level_name=trait_level.name)
        self.update(trait_level_id=db_trait_level.id)
        logger_service.info(
            "API",
            f"Set level of {self.trait_name} in the database",
        )
        return self
    
    def get_datasets(self) -> List[Dataset]:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved datasets of {self.trait_name} from the database",
        )
        return self.datasets
    
    # Todo: Data Handling
    # Todo: Add records, get records, etc.
    # Todo: Add datasets, get datasets, etc.


# from typing import Any, Optional, List
# from gemini.api.base import APIBase
# from gemini.api.trait_record import TraitRecord
# from gemini.api.enums import GEMINITraitLevel
# from gemini.models import TraitModel, ExperimentModel, TraitLevelModel
# from gemini.logger import logger_service

# import pandas as pd
# from datetime import datetime


# class Trait(APIBase):

#     db_model = TraitModel

#     trait_name: str
#     trait_units: Optional[str] = None
#     trait_level_id: Optional[int] = None
#     trait_metrics: Optional[dict] = None
#     trait_info: Optional[dict] = None

#     trait_level: Optional[dict] = None
#     experiments: Optional[List[dict]] = None
#     datasets: Optional[List[dict]] = None

#     @classmethod
#     def create(
#         cls,
#         trait_name: str,
#         trait_units: str = None,
#         trait_level: GEMINITraitLevel = None,
#         trait_metrics: dict = None,
#         trait_info: dict = None,
#         experiment_name: str = None,
#     ):
#         """
#         Create a new trait

#         Args:
#         trait_name (str): The name of the trait
#         trait_units (str, optional): The units of the trait. Defaults to None.
#         trait_level (GEMINITraitLevel, optional): The level of the trait. Defaults to None.
#         trait_metrics (dict, optional): Additional metrics for the trait. Defaults to None.
#         trait_info (dict, optional): Additional information about the trait. Defaults to None.

#         Returns:
#         Trait: The created trait
#         """

#         experiment = ExperimentModel.get_by_parameter(
#             "experiment_name", experiment_name
#         )

#         new_instance = cls.db_model.get_or_create(
#             trait_name=trait_name,
#             trait_units=trait_units,
#             trait_level_id=(
#                 trait_level.value if trait_level else GEMINITraitLevel.Default.value
#             ),
#             trait_metrics=trait_metrics,
#             trait_info=trait_info,
#             experiment_id=experiment.id if experiment else None,
#         )
#         logger_service.info(
#             "API",
#             f"Created a new trait with name {new_instance.trait_name} in the database",
#         )
#         new_instance = cls.model_validate(new_instance)
#         return new_instance

#     @classmethod
#     def get_by_level(cls, trait_level: GEMINITraitLevel) -> List["Trait"]:
#         """
#         Get all the traits of a given level

#         Args:
#         trait_level (GEMINITraitLevel): The level of the trait

#         Returns:
#         List[Trait]: A list of all the traits of the given level
#         """
#         traits = cls.db_model.search(trait_level_id=trait_level.value)
#         traits = [cls.model_validate(trait) for trait in traits]
#         return traits

#     @classmethod
#     def get_by_name(cls, trait_name: str) -> "Trait":
#         """
#         Get a trait by name

#         Args:
#         trait_name (str): The name of the trait

#         Returns:
#         Trait: The trait with the given name
#         """
#         db_instance = cls.db_model.get_by_parameter("trait_name", trait_name)
#         logger_service.info(
#             "API",
#             f"Retrieved trait with name {trait_name} from the database",
#         )
#         return cls.model_validate(db_instance) if db_instance else None

#     def get_info(self) -> dict:
#         """
#         Get the information about a trait

#         Returns:
#         dict: The information about the trait
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved information about {self.trait_name} from the database",
#         )
#         return self.trait_info

#     def set_info(self, trait_info: Optional[dict] = None) -> "Trait":
#         """
#         Set the information about a trait

#         Args:
#         trait_info (Optional[dict], optional): The information to set. Defaults to None.

#         Returns:
#         Trait: The trait with the updated information
#         """
#         self.update(trait_info=trait_info)
#         logger_service.info(
#             "API",
#             f"Updated information about {self.trait_name} in the database",
#         )
#         return self

#     def add_info(self, trait_info: dict) -> "Trait":
#         """
#         Add information to a trait

#         Args:
#         trait_info (dict): The information to add

#         Returns:
#         Trait: The trait with the added information
#         """
#         current_info = self.get_info()
#         updated_info = {**current_info, **trait_info}
#         self.set_info(updated_info)
#         logger_service.info(
#             "API",
#             f"Added information to {self.trait_name} in the database",
#         )
#         return self

#     def remove_info(self, keys_to_remove: List[str]) -> "Trait":
#         """
#         Remove information from a trait

#         Args:
#         keys_to_remove (List[str]): The keys to remove

#         Returns:
#         Trait: The trait with the removed information
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
#             f"Removed information from {self.trait_name} in the database",
#         )
#         return self

#     def get_experiments(self) -> List[dict]:
#         """
#         Get the experiments associated with a trait

#         Returns:
#         List[Experiment]: A list of experiments associated with the trait
#         """
#         self.refresh()
#         experiments = self.experiments
#         logger_service.info(
#             "API",
#             f"Retrieved experiments associated with {self.trait_name} from the database",
#         )
#         return experiments

#     def get_datasets(self) -> List[dict]:
#         """
#         Get the datasets associated with a trait

#         Returns:
#         List[Dataset]: A list of datasets associated with the trait
#         """
#         self.refresh()
#         datasets = self.datasets
#         logger_service.info(
#             "API",
#             f"Retrieved datasets associated with {self.trait_name} from the database",
#         )
#         return datasets

#     def add_experiment(self, experiment_name: str) -> "Trait":
#         """
#         Add an experiment to a trait

#         Args:
#         experiment_name (str): The name of the experiment

#         Returns:
#         Trait: The trait with the added experiment
#         """
#         experiment = ExperimentModel.get_by_parameter(
#             "experiment_name", experiment_name
#         )
#         if experiment and experiment not in self.experiments:
#             self.experiments.append(experiment)
#             self.save()
#             logger_service.info(
#                 "API",
#                 f"Added experiment {experiment_name} to {self.trait_name} in the database",
#             )
#         return self

#     # Todo: Data Handling
#     def get_records(
#         self,
#         collection_date: datetime = None,
#         experiment: str = None,
#         season: str = None,
#         site: str = None,
#         sensor: str = None,
#         plot_number: int = None,
#         plot_row_number: int = None,
#         plot_column_number: int = None,
#         record_info: dict = None,
#         as_dataframe: bool = False,
#     ):
#         """
#         Get the records associated with a trait

#         Args:
#         collection_date (datetime, optional): The collection date of the record. Defaults to None.
#         experiment (str, optional): The name of the experiment. Defaults to None.
#         season (str, optional): The name of the season. Defaults to None.
#         site (str, optional): The name of the site. Defaults to None.
#         sensor (str, optional): The name of the sensor. Defaults to None.
#         plot_number (int, optional): The plot number. Defaults to None.
#         plot_row_number (int, optional): The plot row number. Defaults to None.
#         plot_column_number (int, optional): The plot column number. Defaults to None.
#         record_info (dict, optional): The information of the record. Defaults to None.
#         as_dataframe (bool, optional): Whether to return the records as a dataframe. Defaults to False.

#         Returns:
#         List[TraitRecord]: The records associated with the trait
#         """

#         self.refresh()
#         searched_records = TraitRecord.search(
#             collection_date=collection_date,
#             experiment_name=experiment,
#             season_name=season,
#             site_name=site,
#             sensor_name=sensor,
#             trait_name=self.trait_name,
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#             record_info=record_info,
#         )
#         if as_dataframe:
#             searched_records = pd.DataFrame(searched_records)
#         logger_service.info(
#             "API",
#             f"Retrieved records associated with {self.trait_name} from the database",
#         )
#         return searched_records

#     def add_record(
#         self,
#         timestamp: datetime,
#         collection_date: datetime,
#         record_data: dict,
#         record_info: dict = None,
#         experiment: str = None,
#         season: str = None,
#         site: str = None,
#         sensor: str = None,
#         plot_number: int = None,
#         plot_row_number: int = None,
#         plot_column_number: int = None,
#     ) -> TraitRecord:
#         """
#         Add a record to a trait

#         Args:
#         timestamp (datetime): The timestamp of the record
#         collection_date (datetime): The collection date of the record
#         record_data (dict): The data of the record
#         record_info (dict, optional): The information about the record. Defaults to None.
#         experiment (str, optional): The name of the experiment. Defaults to None.
#         season (str, optional): The name of the season. Defaults to None.
#         site (str, optional): The name of the site. Defaults to None.
#         sensor (str, optional): The name of the sensor. Defaults to None.
#         plot_number (int, optional): The plot number. Defaults to None.
#         plot_row_number (int, optional): The plot row number. Defaults to None.
#         plot_column_number (int, optional): The plot column number. Defaults to None.

#         Returns:
#         TraitRecord: The record added to the trait
#         """
#         new_record = TraitRecord.create(
#             trait_name=self.trait_name,
#             timestamp=timestamp,
#             collection_date=collection_date,
#             trait_value=record_data,
#             record_info=record_info,
#             experiment_name=experiment,
#             season_name=season,
#             site_name=site,
#             sensor_name=sensor,
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#         )
#         logger_service.info(
#             "API",
#             f"Added record to {self.trait_name} in the database",
#         )
#         return new_record

#     def add_records(
#         self,
#         timestamps: List[datetime],
#         record_data: List[dict],
#         record_info: dict = None,
#         experiment_name: str = None,
#         season_name: str = None,
#         site_name: str = None,
#         sensor_name: str = None,
#         plot_numbers: List[int] = None,
#         plot_row_numbers: List[int] = None,
#         plot_column_numbers: List[int] = None,
#     ):
#         """
#         Add records to a trait

#         Args:
#         timestamps (List[datetime]): The timestamps of the records
#         record_data (List[dict]): The data of the records
#         record_info (dict, optional): The information about the records. Defaults to None.
#         experiment_name (str, optional): The name of the experiment. Defaults to None.
#         season_name (str, optional): The name of the season. Defaults to None.
#         site_name (str, optional): The name of the site. Defaults to None.
#         sensor_name (str, optional): The name of the sensor. Defaults to None.
#         plot_numbers (List[int], optional): The plot numbers. Defaults to None.
#         plot_row_numbers (List[int], optional): The plot row numbers. Defaults to None.
#         plot_column_numbers (List[int], optional): The plot column numbers. Defaults to None.
#         """

#         if len(timestamps) != len(record_data):
#             raise ValueError("The number of timestamps and record data do not match")

#         records = TraitRecord.create_bulk(
#             trait_name=self.trait_name,
#             timestamps=timestamps,
#             collection_dates=[timestamp.date() for timestamp in timestamps],
#             trait_values=record_data,
#             record_infos=[record_info] * len(timestamps),
#             experiment_name=experiment_name,
#             season_name=season_name,
#             site_name=site_name,
#             sensor_name=sensor_name,
#             plot_numbers=plot_numbers,
#             plot_row_numbers=plot_row_numbers,
#             plot_column_numbers=plot_column_numbers,
#         )

#         logger_service.info(
#             "API",
#             f"Added {len(records)} records to {self.trait_name} in the database",
#         )

#         return records
