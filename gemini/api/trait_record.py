from typing import Optional, List, Any, Generator
from gemini.api.base import APIBase
from gemini.api.trait import Trait
from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.dataset import Dataset
from gemini.api.plot import Plot
from gemini.api.sensor import Sensor
from gemini.models import TraitRecordModel, TraitModel, DatasetModel
from gemini.logger import logger_service

from datetime import datetime, date
from uuid import UUID


class TraitRecord(APIBase):

    db_model = TraitRecordModel

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_name: Optional[str] = None
    trait_name: Optional[str] = None
    trait_value: Optional[float] = None
    record_info: Optional[dict] = None


    @classmethod
    def create(cls, **kwargs) -> 'TraitRecord':
        record = cls.model_construct(
            _fields_set=cls.model_fields_set,
            **kwargs
        )
        return record

    @classmethod
    def add(cls, records: List['TraitRecord']) -> bool:
        try:
            records_to_insert = []
            dataset_id = DatasetModel.get_by_parameters(dataset_name=records[0].dataset_name).id
            trait_id = TraitModel.get_or_create(trait_name=records[0].trait_name).id
            for record in records:
                record_to_add = {}
                record_to_add['timestamp'] = record.timestamp
                record_to_add['collection_date'] = record.collection_date
                record_to_add['dataset_id'] = dataset_id
                record_to_add['dataset_name'] = record.dataset_name
                record_to_add['trait_id'] = trait_id
                record_to_add['trait_value'] = record.trait_value
                record_to_add['record_info'] = record.record_info
                records_to_insert.append(record_to_add)
            cls.db_model.insert_bulk("trait_records_unique", records_to_insert)
            logger_service.info(
                "API",
                f"Added {len(records)} trait records to the database",
            )
            return True
        except Exception as e:
            logger_service.error(
                "API",
                f"Failed to add trait records to the database",
            )
            return False
        
    @classmethod
    def get(cls, record_id: UUID) -> 'TraitRecord':
        record = cls.db_model.get_by_id(record_id)
        return cls.model_validate(record)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Getting information of the record with id {self.id}",
        )
        return self.record_info

    def set_info(self, record_info: dict) -> 'TraitRecord':
        self.update(record_info=record_info)
        logger_service.info(
            "API",
            f"Set information of the record with id {self.id}",
        )
        return self
    
    def add_info(self, record_info: dict) -> 'TraitRecord':
        current_info = self.get_info()
        updated_info = {**current_info, **record_info}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Added information to the record with id {self.id}",
        )
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> 'TraitRecord':
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Removed information from the record with id {self.id}",
        )
        return self
    
    @classmethod
    def search(cls, **kwargs) -> Generator['TraitRecord', None, None]:
        searched_records = cls.db_model.stream(**kwargs)
        for record in searched_records:
            record = cls.model_validate(record)
            yield record


# from typing import Optional, List, Any, Generator
# from typing_extensions import Annotated
# from pydantic import BaseModel, Field, ValidationError, ValidationInfo, field_validator
# from gemini.api.base import APIBase
# from gemini.models.columnar.trait_records import TraitRecordModel
# from gemini.models.experiments import ExperimentModel
# from gemini.models.sensors import SensorModel
# from gemini.models.seasons import SeasonModel
# from gemini.models.sites import SiteModel
# from gemini.models.plots import PlotModel
# from gemini.models.traits import TraitModel
# from gemini.models.views.trait_records_view import TraitRecordsViewModel
# from gemini.logger import logger_service
# from gemini.object_store import storage_service
# from datetime import datetime
# from datetime import date


# import os
# import uuid

# from rich.progress import track


# class TraitRecord(APIBase):

#     db_model = TraitRecordModel

#     timestamp: Optional[datetime] = None
#     collection_date: Optional[date] = None
#     sensor_id: Optional[uuid.UUID] = None
#     experiment_id: Optional[uuid.UUID] = None
#     season_id: Optional[uuid.UUID] = None
#     site_id: Optional[uuid.UUID] = None
#     plot_id: Optional[uuid.UUID] = None
#     trait_id: Optional[uuid.UUID] = None
#     trait_value: Optional[float] = None
#     record_info: Optional[dict] = None

#     trait: Optional[dict] = None
#     experiment: Optional[dict] = None
#     season: Optional[dict] = None
#     site: Optional[dict] = None
#     plot: Optional[dict] = None
#     sensor: Optional[dict] = None

#     def create(
#         cls,
#         trait_name: str,
#         trait_value: float,
#         timestamp: datetime = None,
#         collection_date: date = None,
#         experiment_name: str = None,
#         season_name: str = None,
#         site_name: str = None,
#         plot_number: int = None,
#         plot_row_number: int = None,
#         plot_column_number: int = None,
#         sensor_name: str = None,
#         record_info: dict = None,
#     ):
#         """
#         Create a new trait record

#         Args:
#         trait_name (str): The name of the trait
#         trait_value (float): The value of the trait
#         experiment_name (str, optional): The name of the experiment. Defaults to None.
#         season_name (str, optional): The name of the season. Defaults to None.
#         site_name (str, optional): The name of the site. Defaults to None.
#         plot_number (int, optional): The number of the plot. Defaults to None.
#         plot_row_number (int, optional): The row number of the plot. Defaults to None.
#         plot_column_number (int, optional): The column number of the plot. Defaults to None.
#         sensor_name (str, optional): The name of the sensor. Defaults to None.
#         record_info (dict, optional): The information about the record. Defaults to None.

#         Returns:
#         TraitRecord: The created trait record
#         """

#         trait = TraitModel.get_by_parameter("trait_name", trait_name)
#         sensor = SensorModel.get_by_parameter("sensor_name", sensor_name)
#         experiment = ExperimentModel.get_or_create(experiment_name=experiment_name)
#         season = SeasonModel.get_or_create(
#             season_name=season_name, experiment_id=experiment.id
#         )
#         site = SiteModel.get_or_create(site_name=site_name)

#         plot = PlotModel.get_or_create(
#             experiment_id=experiment.id if experiment else None,
#             season_id=season.id if season else None,
#             site_id=site.id if site else None,
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#         )

#         new_instance = cls.db_model.get_or_create(
#             timestamp=timestamp,
#             collection_date=collection_date,
#             trait_id=trait.id,
#             trait_value=trait_value,
#             sensor_id=sensor.id if sensor else None,
#             experiment_id=experiment.id if experiment else None,
#             season_id=season.id if season else None,
#             site_id=site.id if site else None,
#             plot_id=plot.id if plot else None,
#             record_info=record_info,
#         )

#         new_instance.save()
#         logger_service.info(
#             "API",
#             f"Created a new trait record with id {new_instance.id} in the database",
#         )
#         new_instance = cls.model_validate(new_instance)
#         return new_instance

#     @classmethod
#     def create_bulk(
#         cls,
#         timestamps: List[datetime],
#         collection_dates: List[date],
#         trait_name: str,
#         sensor_name: str,
#         experiment_name: str = None,
#         season_name: str = None,
#         site_name: str = None,
#         plot_numbers: List[int] = None,
#         plot_row_numbers: List[int] = None,
#         plot_column_numbers: List[int] = None,
#         trait_values: List[float] = None,
#         record_infos: List[dict] = None,
#     ):

#         trait = TraitModel.get_by_parameter("trait_name", trait_name)
#         sensor = SensorModel.get_by_parameter("sensor_name", sensor_name)
#         experiment = ExperimentModel.get_or_create(experiment_name=experiment_name)
#         season = SeasonModel.get_or_create(
#             season_name=season_name, experiment_id=experiment.id
#         )
#         site = SiteModel.get_or_create(site_name=site_name)

#         records_to_add = []

#         for i in track(range(len(timestamps)), description="Adding Trait Records"):
#             plot = PlotModel.get_or_create(
#                 experiment_id=experiment.id if experiment else None,
#                 season_id=season.id if season else None,
#                 site_id=site.id if site else None,
#                 plot_number=plot_numbers[i] if plot_numbers else None,
#                 plot_row_number=plot_row_numbers[i] if plot_row_numbers else None,
#                 plot_column_number=(
#                     plot_column_numbers[i] if plot_column_numbers else None
#                 ),
#             )

#             record = {
#                 "timestamp": timestamps[i],
#                 "collection_date": collection_dates[i],
#                 "trait_id": trait.id,
#                 "trait_value": trait_values[i] if trait_values else None,
#                 "sensor_id": sensor.id if sensor else None,
#                 "experiment_id": experiment.id if experiment else None,
#                 "season_id": season.id if season else None,
#                 "site_id": site.id if site else None,
#                 "plot_id": plot.id if plot else None,
#                 "record_info": record_infos[i] if record_infos else None,
#             }

#             records_to_add.append(record)

#         records = cls.db_model.insert_bulk("trait_records_unique", records_to_add)

#         logger_service.info(
#             "API",
#             f"Created {len(records)} new trait records in the database",
#         )

#         return records

#     def get_info(self) -> dict:
#         """
#         Get the information of the record

#         Returns:
#         dict: Information of the record
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Getting information of the record with id {self.id}",
#         )
#         return self.record_info

#     def set_info(self, record_info: dict) -> "TraitRecord":
#         """
#         Set the information of the record

#         Args:
#         record_info (dict): The information to set
#         """
#         self.update(record_info=record_info)
#         logger_service.info(
#             "API",
#             f"Set information of the record with id {self.id}",
#         )
#         return self

#     def add_info(self, record_info: dict) -> "TraitRecord":
#         """
#         Add information to the record

#         Args:
#         record_info (dict): The information to add
#         """
#         current_info = self.get_info()
#         current_info.update(record_info)
#         self.set_info(current_info)
#         logger_service.info(
#             "API",
#             f"Added information to the record with id {self.id}",
#         )
#         return self

#     def remove_info(self, keys_to_remove: List[str]) -> "TraitRecord":
#         """
#         Remove information from the record

#         Args:
#         keys_to_remove (List[str]): The keys to remove
#         """
#         current_info = self.get_info()
#         for key in keys_to_remove:
#             current_info.pop(key, None)
#         self.set_info(current_info)
#         logger_service.info(
#             "API",
#             f"Removed information from the record with id {self.id}",
#         )
#         return self

#     def get_model(self) -> dict:
#         """
#         Get the model of the record

#         Returns:
#         dict: The model of the record
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Getting model of the record with id {self.id}",
#         )
#         return self.model

#     def get_experiment(self) -> dict:
#         """
#         Get the experiment of the record

#         Returns:
#         dict: The experiment of the record
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Getting experiment of the record with id {self.id}",
#         )
#         return self.experiment

#     def get_season(self) -> dict:
#         """
#         Get the season of the record

#         Returns:
#         dict: The season of the record
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Getting season of the record with id {self.id}",
#         )
#         return self.season

#     def get_site(self) -> dict:
#         """
#         Get the site of the record

#         Returns:
#         dict: The site of the record
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Getting site of the record with id {self.id}",
#         )
#         return self.site

#     def get_sensor(self) -> dict:
#         """
#         Get the sensor of the record

#         Returns:
#         dict: The sensor of the record
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Getting sensor of the record with id {self.id}",
#         )
#         return self.sensor

#     def get_plot(self) -> dict:
#         """
#         Get the plot of the record

#         Returns:
#         dict: The plot of the record
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Getting plot of the record with id {self.id}",
#         )
#         return self.plot

#     def set_plot(
#         self, plot_number: int, plot_row_number: int, plot_column_number: int
#     ) -> "TraitRecord":
#         """
#         Set the plot of the record

#         Args:
#         plot_number (int): The plot number
#         plot_row_number (int): The row number of the plot
#         plot_column_number (int): The column number of the plot
#         """
#         plot = PlotModel.get_or_create(
#             experiment_id=self.experiment_id,
#             season_id=self.season_id,
#             site_id=self.site_id,
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#         )
#         self.update(plot_id=plot.id)
#         logger_service.info(
#             "API",
#             f"Set plot of the record with id {self.id}",
#         )
#         return self

#     @classmethod
#     def search(cls, **kwargs) -> Generator["TraitRecord", None, None]:
#         """
#         Search for trait records in the database

#         Args:
#         **kwargs: The search parameters

#         Returns:
#         List[TraitRecord]: The trait records that match the search parameters
#         """

#         searched_records = TraitRecordsViewModel.stream(**kwargs)
#         for record in searched_records:
#             record = record.to_dict()
#             yield record
