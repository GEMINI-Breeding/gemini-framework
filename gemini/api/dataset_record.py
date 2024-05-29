from typing import Optional, List, Any, Generator
from pydantic import Field, BaseModel, ConfigDict
from gemini.api.base import APIBase
from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.dataset import Dataset
from gemini.api.plot import Plot
from gemini.models import DatasetRecordModel, PlotModel, SiteModel, SeasonModel, ExperimentModel, DatasetModel
from gemini.logger import logger_service
from gemini.object_store import storage_service
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID
from rich.progress import track
import os

class DatasetRecord(APIBase):

    db_model = DatasetRecordModel

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id : Optional[UUID] = None
    dataset_name : Optional[str] = None
    dataset_data: Optional[dict] = None
    record_info: Optional[dict] = None

    @classmethod
    def create(cls, **kwargs):
        record = DatasetRecord.model_construct(
            _fields_set=DatasetRecord.model_fields_set,
            **kwargs
        )
        return record

    @classmethod
    def add(cls, records: List['DatasetRecord']) -> bool:
        try:
            records_to_insert = []
            dataset_id = DatasetModel.get_or_create(dataset_name=records[0].dataset_name).id
            for record in track(records, description=f"Adding {len(records)} records to the dataset"):
                record_to_insert = {}
                record_to_insert['timestamp'] = record.timestamp
                record_to_insert['collection_date'] = record.timestamp.date()
                record_to_insert['dataset_id'] = dataset_id
                record_to_insert['dataset_name'] = record.dataset_name
                record_to_insert['dataset_data'] = record.dataset_data
                record_to_insert['record_info'] = record.record_info
                records_to_insert.append(record_to_insert)
            DatasetRecordModel.insert_bulk('dataset_records_unique', records_to_insert)
            logger_service.info('API', f'Added {len(records)} records to the database')
            return True
        except Exception as e:
            logger_service.error('API', f'Error adding records to the database: {e}')
            return False
        
    @classmethod
    def get(cls, record_id: UUID) -> 'DatasetRecord':
        record = DatasetRecordModel.get_by_id(record_id)
        return record
    
    def set_info(self, record_info: Optional[dict] = None) -> 'DatasetRecord':
        self.update(record_info=record_info)
        logger_service.info('API', f'Set information about dataset record with id {self.id}')
        return self
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info('API', f'Retrieved information about dataset record with id {self.id}')
        return self.record_info
    
    def add_info(self, record_info: Optional[dict] = None) -> 'DatasetRecord':
        current_info = self.record_info
        updated_info = {**current_info, **record_info}
        self.set_info(updated_info)
        logger_service.info('API', f'Added information to dataset record with id {self.id}')
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> 'DatasetRecord':
        current_info = self.record_info
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info('API', f'Removed information from dataset record with id {self.id}')
        return self
    
    @classmethod
    def search(cls, **kwargs) -> Generator['DatasetRecord', None, None]:
        records = DatasetRecordModel.stream(**kwargs)
        for record in records:
            record = record.to_dict()
            record = cls.postprocess_record(record)
            record = cls.model_validate(record)
            yield record

    @classmethod
    def preprocess_record(cls, record: dict) -> dict:
        dataset_data = record.get("dataset_data")
        dataset_data_copy = dataset_data.copy()
        for key, value in dataset_data_copy.items():
            if key in ["file", "file_path"]:
                file_uri = cls._upload_file(value, record)
                dataset_data["file_uri"] = file_uri
                dataset_data.pop(key)

        record["dataset_data"] = dataset_data

        logger_service.info(
            "API",
            f"Preprocessed record with id {record.get('id')}",
        )
        return record
    
    @classmethod
    def postprocess_record(cls, record: dict) -> dict:
        record_copy = record.copy()
        dataset_data = record_copy.get("dataset_data")
        if not dataset_data:
            return
        file_uri = dataset_data.get("file_uri")
        if file_uri:
            downloaded_local_file_path = cls._download_file(record_copy)
            record_copy["dataset_data"]["file_path"] = downloaded_local_file_path
        logger_service.info(
            "API",
            f"Postprocessed record with id {record.get('id')}",
        )
        return record_copy
    
    @classmethod
    def generate_file_uri(cls, file_path: str, record: dict) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at {file_path}")

        file_name = os.path.basename(file_path)
        collection_date = record.get("collection_date").strftime("%Y-%m-%d")
        file_uri = f"dataset_data/{collection_date}/{record.get('dataset_name')}/{file_name}"
        return file_uri
    
    @classmethod
    def _upload_file(cls, absolute_file_path: str, record: dict) -> str:
        file_uri = cls.generate_file_uri(absolute_file_path, record)

        file_tags = {
            "dataset_name": record.get("dataset_name"),
            "collection_date": record.get("collection_date").strftime("%Y-%m-%d"),
            **record.get("record_info")
        }
        storage_service.upload_file(
            file_path=absolute_file_path,
            key=file_uri,
            tags=file_tags
        )

        logger_service.info(
            "API",
            f"Uploaded dataset data file for record with id {record.get('id')}",
        )

        return file_uri
    
    @classmethod
    def _download_file(cls, record: dict) -> str:
        dataset_data = record.get("dataset_data")
        file_uri = dataset_data.get("file_uri")
        if not file_uri:
            raise ValueError("No file URI found in dataset data")

        file_path = storage_service.download_file(file_uri)
        logger_service.info(
            "API",
            f"Downloaded dataset data file for record with id {record.get('id')}",
        )
        return file_path
    
    def download(self) -> str:
        self.refresh()
        file_uri = self.dataset_data.get("file_uri")
        if not file_uri:
            raise ValueError("No file URI found in dataset data")
        
        file_path = storage_service.download_file(file_uri)
        logger_service.info(
            "API",
            f"Downloaded dataset data file for record with id {self.id}",
        )
        return file_path        



    # @classmethod
    # def add(cls, records: List['DatasetRecordEntry']) -> bool:
    #     records_to_insert = []
    #     for record in track(records, description=f"Adding {len(records)} records to the dataset"):
    #         record_to_insert = {}
    #         record_to_insert['timestamp'] = record.timestamp
    #         record_to_insert['collection_date'] = record.timestamp.date()
    #         record_to_insert['dataset_id'] = DatasetModel.get_or_create(dataset_name=record.dataset_name).id
    #         record_to_insert['experiment_id'] = ExperimentModel.get_or_create(experiment_name=record.experiment_name).id
    #         record_to_insert['season_id'] = SeasonModel.get_or_create(season_name=record.season_name, experiment_id=record_to_insert['experiment_id']).id
    #         record_to_insert['site_id'] = SiteModel.get_or_create(site_name=record.site_name).id
    #         record_to_insert['plot_id'] = PlotModel.get_or_create(
    #             plot_number=record.plot_number,
    #             plot_row_number=record.plot_row_number,
    #             plot_column_number=record.plot_column_number,
    #             season_id=record_to_insert['season_id'],
    #             experiment_id=record_to_insert['experiment_id'],
    #             site_id=record_to_insert['site_id']
    #         ).id
    #         record_to_insert['dataset_data'] = record.dataset_data
    #         record_to_insert['record_info'] = record.record_info
    #         records_to_insert.append(record_to_insert)
    #     cls.db_model.insert_bulk('dataset_records_unique', records_to_insert)
    #     logger_service.info('API', f'Added {len(records)} records to the database')
    #     return True





# from typing import Optional, List, Any
# from typing_extensions import Annotated
# from pydantic import BaseModel, Field, ValidationError, ValidationInfo, field_validator
# from gemini.api.base import APIBase
# from gemini.models.columnar.dataset_records import DatasetRecordModel
# from gemini.models.experiments import ExperimentModel
# from gemini.models.datasets import DatasetModel
# from gemini.models.seasons import SeasonModel
# from gemini.models.sites import SiteModel
# from gemini.models.plots import PlotModel
# from gemini.models.views.dataset_records_view import DatasetRecordsViewModel
# from gemini.logger import logger_service
# from gemini.object_store import storage_service
# from datetime import datetime
# from datetime import date

# import os
# import uuid
# import pandas as pd
# from rich.progress import track


# class DatasetRecord(APIBase):

#     db_model = DatasetRecordModel

#     timestamp: Optional[datetime] = None
#     collection_date: Optional[date] = None
#     dataset_id: Optional[uuid.UUID] = None
#     experiment_id: Optional[uuid.UUID] = None
#     season_id: Optional[uuid.UUID] = None
#     site_id: Optional[uuid.UUID] = None
#     plot_id: Optional[uuid.UUID] = None
#     dataset_data: Optional[dict] = None
#     record_info: Optional[dict] = None

#     dataset: Optional[dict] = None
#     experiment: Optional[dict] = None
#     season: Optional[dict] = None
#     site: Optional[dict] = None
#     plot: Optional[dict] = None

#     @classmethod
#     def create(
#         cls,
#         timestamp: datetime,
#         collection_date: datetime,
#         dataset_name: str = None,
#         experiment_name: str = None,
#         season_name: str = None,
#         site_name: str = None,
#         plot_number: int = None,
#         plot_row_number: int = None,
#         plot_column_number: int = None,
#         dataset_data: dict = None,
#         record_info: dict = None,
#     ) -> "DatasetRecord":

#         dataset = DatasetModel.get_by_parameter("dataset_name", dataset_name)
#         experiment = ExperimentModel.get_or_create(experiment_name=experiment_name)
#         season = SeasonModel.get_or_create(
#             season_name=season_name, experiment_id=experiment.id
#         )
#         site = SiteModel.get_or_create(site_name=site_name)

#         plot = PlotModel.get_or_create(
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#             season_id=season.id if season else None,
#             experiment_id=experiment.id if experiment else None,
#             site_id=site.id if site else None,
#         )

#         new_instance = cls.db_model.get_or_create(
#             timestamp=timestamp,
#             collection_date=collection_date,
#             dataset_id=dataset.id if dataset else None,
#             experiment_id=experiment.id if experiment else None,
#             season_id=season.id if season else None,
#             site_id=site.id if site else None,
#             plot_id=plot.id if plot else None,
#             dataset_data=dataset_data,
#             record_info=record_info,
#         )

#         logger_service.info(
#             "API",
#             f"Created a new dataset record with id {new_instance.id} in the database",
#         )

#         new_instance = cls.model_validate(new_instance)
#         new_instance = cls.process_record(new_instance)
#         return new_instance

#     @classmethod
#     def create_bulk(
#         cls,
#         timestamps: List[datetime],
#         collection_dates: List[date],
#         dataset_name: str,
#         experiment_name: str,
#         season_name: str,
#         site_name: str,
#         plot_numbers: List[int],
#         plot_row_numbers: List[int],
#         plot_column_numbers: List[int],
#         dataset_data: List[dict] = None,
#         record_info: List[dict] = None,
#     ):

#         dataset = DatasetModel.get_by_parameter("dataset_name", dataset_name)
#         experiment = ExperimentModel.get_or_create(experiment_name=experiment_name)
#         season = SeasonModel.get_or_create(
#             season_name=season_name, experiment_id=experiment.id
#         )
#         site = SiteModel.get_or_create(site_name=site_name)

#         records_to_add = []

#         for i in track(range(len(timestamps)), description="Creating records"):
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
#                 "dataset_id": dataset.id if dataset else None,
#                 "experiment_id": experiment.id if experiment else None,
#                 "season_id": season.id if season else None,
#                 "site_id": site.id if site else None,
#                 "plot_id": plot.id if plot else None,
#                 "dataset_data": dataset_data[i] if dataset_data else None,
#                 "record_info": record_info[i] if record_info else None,
#             }

#             records_to_add.append(record)

#         # Bulk insert the records
#         records = cls.db_model.insert_bulk("dataset_records_unique", records_to_add)

#         for record in track(records, description="Processing Dataset Records"):
#             dataset_data = record.dataset_data
#             if any(key in dataset_data for key in ["file", "file_path"]):
#                 record = cls.model_validate(record)
#                 record = cls.process_record(record)

#         logger_service.info(
#             "API",
#             f"Created {len(records)} new procedure records in the database",
#         )

#         return records

#     def get_info(self) -> dict:
#         """
#         Get the information about a dataset record

#         Returns:
#         dict: The information about the dataset record
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved information about dataset record with id {self.id}",
#         )
#         return self.record_info

#     def set_info(self, record_info: Optional[dict] = None) -> "DatasetRecord":
#         """
#         Set the information about a dataset record

#         Args:
#         record_info (dict, optional): The information about the dataset record. Defaults to None.

#         Returns:
#         DatasetRecord: The dataset record with the new information
#         """
#         self.update(record_info=record_info)
#         logger_service.info(
#             "API",
#             f"Set information about dataset record with id {self.id}",
#         )
#         return self

#     def add_info(self, record_info: Optional[dict] = None) -> "DatasetRecord":
#         """
#         Add information to a dataset record

#         Args:
#         record_info (dict, optional): The information to add. Defaults to None.

#         Returns:
#         DatasetRecord: The dataset record with the added information
#         """
#         current_info = self.record_info
#         updated_info = {**current_info, **record_info}
#         self.set_info(updated_info)
#         logger_service.info(
#             "API",
#             f"Added information to dataset record with id {self.id}",
#         )
#         return self

#     def remove_info(self, keys_to_remove: List[str]) -> "DatasetRecord":
#         """
#         Remove information from a dataset record

#         Args:
#         keys_to_remove (List[str]): The keys to remove
#         """
#         current_info = self.record_info
#         updated_info = {
#             key: value
#             for key, value in current_info.items()
#             if key not in keys_to_remove
#         }
#         self.set_info(updated_info)
#         logger_service.info(
#             "API",
#             f"Removed information from dataset record with id {self.id}",
#         )
#         return self

#     def get_dataset(self) -> dict:
#         """
#         Get the dataset associated with a dataset record

#         Returns:
#         dict: The information about the dataset
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved information about dataset with id {self.dataset_id} from the database",
#         )
#         return self.dataset

#     def get_experiment(self) -> dict:
#         """
#         Get the experiment associated with a dataset record

#         Returns:
#         dict: The information about the experiment
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved information about experiment with id {self.experiment_id} from the database",
#         )
#         return self.experiment

#     def get_season(self) -> dict:
#         """
#         Get the season associated with a dataset record

#         Returns:
#         dict: The information about the season
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved information about season with id {self.season_id} from the database",
#         )
#         return self.season

#     def get_site(self) -> dict:
#         """
#         Get the site associated with a dataset record

#         Returns:
#         dict: The information about the site
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved information about site with id {self.site_id} from the database",
#         )
#         return self.site

#     def get_plot(self) -> dict:
#         """
#         Get the plot associated with a dataset record

#         Returns:
#         dict: The information about the plot
#         """
#         self.refresh()
#         logger_service.info(
#             "API",
#             f"Retrieved information about plot with id {self.plot_id} from the database",
#         )
#         return self.plot

#     def set_plot(
#         self, plot_number: int, plot_row_number: int, plot_column_number: int
#     ) -> "DatasetRecord":
#         """
#         Set the plot associated with a dataset record

#         Args:
#         plot_number (int): The number of the plot
#         plot_row_number (int): The row number of the plot
#         plot_column_number (int): The column number of the plot

#         Returns:
#         DatasetRecord: The dataset record with the updated plot
#         """
#         plot = PlotModel.get_by_parameters(
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#         )
#         self.update(plot_id=plot.id)
#         logger_service.info(
#             "API",
#             f"Set plot for dataset record with id {self.id}",
#         )
#         return self

#     def process_record(self) -> "DatasetRecord":
#         """
#         Process the dataset record
#         """
#         self.refresh()
#         dataset_data = self.dataset_data
#         for key, value in dataset_data.items():
#             if key in ["file", "file_path"]:
#                 self.upload_dataset_data_file(value)
#         logger_service.info(
#             "API",
#             f"Processed dataset record with id {self.id}",
#         )
#         return self

#     def generate_file_uri(self, file_path: str) -> str:
#         """
#         Generate a file URI

#         Args:
#         file_path (str): The path to the file

#         Returns:
#         str: The file URI
#         """
#         if not os.path.exists(file_path):
#             raise FileNotFoundError(f"File not found at {file_path}")

#         file_name = os.path.basename(file_path)
#         file_uri = f"dataset_data/{self.collection_date}/{self.dataset.dataset_name}/{file_name}"
#         return file_uri

#     def upload_dataset_data_file(self, absolute_file_path: str) -> str:
#         """
#         Upload a dataset data file

#         Args:
#         absolute_file_path (str): The absolute path to the file

#         Returns:
#         str: The file URI
#         """
#         file_uri = self.generate_file_uri(absolute_file_path)
#         file_tags = {
#             "dataset_name": self.dataset.dataset_name if self.dataset else None,
#             "experiment_name": (
#                 self.experiment.experiment_name if self.experiment else None
#             ),
#             "season_name": self.season.season_name if self.season else None,
#             "site_name": self.site.site_name if self.site else None,
#             "plot_number": self.plot.plot_number if self.plot else None,
#             "plot_row_number": self.plot.plot_row_number if self.plot else None,
#             "plot_column_number": self.plot.plot_column_number if self.plot else None,
#             "collection_date": datetime.strftime(self.collection_date, "%Y-%m-%d"),
#         }
#         storage_service.upload_file(
#             file_path=absolute_file_path, key=file_uri, tags=file_tags
#         )
#         self.update(dataset_data={"file_uri": file_uri})
#         logger_service.info(
#             "API",
#             f"Uploaded dataset data file for dataset record with id {self.id}",
#         )
#         return file_uri

#     def download_file(self) -> str:
#         self.refresh()
#         dataset_data = self.dataset_data
#         file_uri = dataset_data.get("file_uri")
#         if not file_uri:
#             return None

#         file_path = storage_service.download_file(file_uri)
#         logger_service.info(
#             "API",
#             f"Downloaded dataset data file for dataset record with id {self.id}",
#         )
#         return file_path

#     def get_file_url(self) -> str:
#         self.refresh()
#         dataset_data = self.dataset_data
#         file_uri = dataset_data.get("file_uri")
#         if not file_uri:
#             return None

#         file_url = storage_service.get_presigned_download_url(file_uri)
#         logger_service.info(
#             "API",
#             f"Retrieved file URL for dataset record with id {self.id}",
#         )
#         return file_url

#     @classmethod
#     def search(cls, **kwargs):
#         """
#         Search for dataset records in the database

#         Args:
#         **kwargs: The search parameters

#         Returns:
#         List[DatasetRecord]: The dataset records that match the search parameters
#         """
#         searched_records = DatasetRecordsViewModel.stream(**kwargs)
#         for record in searched_records:
#             record = cls.model_validate(record)
#             yield record

#         logger_service.info(
#             "API",
#             f"Retrieved dataset records from the database",
#         )
