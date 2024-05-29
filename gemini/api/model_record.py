from typing import Optional, List, Any, Generator
from pydantic import Field, BaseModel, ConfigDict
from gemini.api.base import APIBase
from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.dataset import Dataset
from gemini.api.plot import Plot
from gemini.models import ModelRecordModel, DatasetModel, ModelModel
from gemini.logger import logger_service
from gemini.object_store import storage_service
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID
from rich.progress import track

import os

class ModelRecord(APIBase):

    db_model = ModelRecordModel

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[UUID] = None
    dataset_name: Optional[str] = None
    model_id: Optional[UUID] = None
    model_name: Optional[str] = None
    model_data: Optional[dict] = None
    record_info: Optional[dict] = None

    @classmethod
    def create(cls, **kwargs) -> 'ModelRecord':
        record = ModelRecord.model_construct(
            _fields_set=ModelRecord.model_fields_set,
            **kwargs
        )
        return record

    @classmethod
    def add(cls, records: List['ModelRecord']) -> bool:
        try:
            records_to_insert = []
            dataset_id = DatasetModel.get_or_create(name=records[0].dataset_name).id
            model_id = ModelModel.get_or_create(name=records[0].model_name).id
            for record in records:
                record_to_insert = {}
                record_to_insert['timestamp'] = record.timestamp
                record_to_insert['collection_date'] = record.collection_date
                record_to_insert['dataset_id'] = dataset_id
                record_to_insert['dataset_name'] = record.dataset_name
                record_to_insert['model_id'] = model_id
                record_to_insert['model_name'] = record.model_name
                record_to_insert['model_data'] = record.model_data
                record_to_insert['record_info'] = record.record_info
                records_to_insert.append(record_to_insert)
            ModelRecordModel.insert_bulk('model_records', records_to_insert)
            logger_service.info(
                "API",
                f"Added {len(records)} model records to the database",
            )
            return True
        except Exception as e:
            logger_service.error(
                "API",
                f"Failed to add model records to the database",
            )
            return False
        
    @classmethod
    def get(cls, record_id: UUID) -> 'ModelRecord':
        record = ModelRecordModel.get_by_id(record_id)
        return cls.model_validate(record)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Getting information of the record with id {self.id}",
        )
        return self.record_info
    
    def set_info(self, record_info: dict) -> 'ModelRecord':
        self.update(record_info=record_info)
        logger_service.info(
            "API",
            f"Set information of the record with id {self.id}",
        )
        return self
    
    def add_info(self, record_info: dict) -> 'ModelRecord':
        current_info = self.get_info()
        updated_info = {**current_info, **record_info}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Added information to the record with id {self.id}",
        )
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> 'ModelRecord':
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Removed information from the record with id {self.id}",
        )
        return self
        
    @classmethod
    def search(cls, **kwargs) -> Generator['ModelRecord', None, None]:
        records = ModelRecordModel.stream(**kwargs)
        for record in records:
            record = record.to_dict()
            record = cls.postprocess_record(record)
            record = cls.model_validate(record)
            yield record

    @classmethod
    def preprocess_record(cls, record: dict) -> dict:
        model_data = record.get("model_data")
        model_data_copy = model_data.copy()
        for key, value in model_data_copy.items():
            if key in ["file", "file_path"]:
                file_uri = cls._upload_file(value, record)
                model_data["file_uri"] = file_uri
                model_data.pop(key)

        record["model_data"] = model_data

        logger_service.info(
            "API",
            f"Preprocessed record with id {record.get('id')}",
        )
        
        return record
    
    @classmethod
    def postprocess_record(cls, record: dict) -> dict:
        record_copy = record.copy()
        model_data = record_copy.get("model_data")
        if not model_data:
            return
        
        file_uri = model_data.get("file_uri")
        if file_uri:
            downloaded_local_file_path = cls._download_file(record_copy)
            record_copy["model_data"]["local_file_path"] = downloaded_local_file_path

        logger_service.info(
            "API",
            f"Postprocessed record with id {record_copy.get('id')}",
        )
        return record_copy

    @classmethod
    def generate_file_uri(cls, absolute_file_path: str, record: dict) -> str:
        if not os.path.exists(absolute_file_path):
            raise FileNotFoundError(f"File not found at path {absolute_file_path}")

        file_name = os.path.basename(absolute_file_path)
        collection_date = record.get('collection_date').strftime('%Y-%m-%d')
        file_uri = f"model_data/{collection_date}/{record.get('model_name')}/{file_name}"
        return file_uri
    

    @classmethod
    def _upload_file(cls, absolute_file_path: str, record: dict) -> str:
        file_uri = cls.generate_file_uri(absolute_file_path, record)
        file_tag = {
            'model_name': record.get('model_name'),
            'dataset_name': record.get('dataset_name'),
            'collection_date': record.get('collection_date').strftime('%Y-%m-%d')
            **record.get('record_info')
        }
        storage_service.upload_file(file_path=absolute_file_path, key=file_uri, tags=file_tag)
        logger_service.info(
            "API",
            f"Uploaded model data file for record with id {record.get('id')}",
        )
        return file_uri
    
    @classmethod
    def _download_file(cls, record: dict) -> str:
        file_uri = record.get("model_data").get("file_uri")
        if not file_uri:
            raise ValueError("File URI not found in the record")
        
        file_path = storage_service.download_file(file_uri)
        logger_service.info(
            "API",
            f"Downloaded model data file for record with id {record.get('id')}",
        )
        return file_path
    
    def download(self) -> str:
        self.refresh()
        file_uri = self.model_data.get("file_uri")
        if not file_uri:
            raise ValueError("File URI not found in the record")
        
        file_path = storage_service.download_file(file_uri)
        logger_service.info(
            "API",
            f"Downloaded model data file for record with id {self.id}",
        )
        return file_path

# from typing import Optional, List, Any
# from typing_extensions import Annotated
# from pydantic import BaseModel, Field, ValidationError, ValidationInfo, field_validator
# from pydantic import ConfigDict
# from gemini.api.base import APIBase
# from gemini.models.columnar.model_records import ModelRecordModel
# from gemini.models.experiments import ExperimentModel
# from gemini.models.seasons import SeasonModel
# from gemini.models.sites import SiteModel
# from gemini.models.plots import PlotModel
# from gemini.models.models import ModelModel
# from gemini.models.views.model_records_view import ModelRecordsViewModel
# from gemini.logger import logger_service
# from gemini.object_store import storage_service
# from datetime import datetime
# from datetime import date


# import os
# import uuid
# from rich.progress import track


# class ModelRecord(APIBase):

#     db_model = ModelRecordModel

#     model_config = ConfigDict(
#         arbitrary_types_allowed=True, from_attributes=True, protected_namespaces=()
#     )

#     timestamp: Optional[datetime] = None
#     collection_date: Optional[date] = None
#     experiment_id: Optional[uuid.UUID] = None
#     season_id: Optional[uuid.UUID] = None
#     site_id: Optional[uuid.UUID] = None
#     plot_id: Optional[uuid.UUID] = None
#     model_id: Optional[uuid.UUID] = None
#     model_data: Optional[dict] = None
#     record_info: Optional[dict] = None

#     model: Optional[dict] = None
#     experiment: Optional[dict] = None
#     season: Optional[dict] = None
#     site: Optional[dict] = None
#     plot: Optional[dict] = None
#     sensor: Optional[dict] = None

#     @classmethod
#     def create(
#         cls,
#         timestamp: datetime,
#         collection_date: date,
#         model_name: str,
#         model_data: dict,
#         record_info: dict = None,
#         experiment_name: str = None,
#         season_name: str = None,
#         site_name: str = None,
#         plot_number: int = None,
#         plot_row_number: int = None,
#         plot_column_number: int = None,
#     ):
#         model = ModelModel.get_by_parameter("model_name", model_name)
#         experiment = ExperimentModel.get_or_create(experiment_name=experiment_name)
#         season = SeasonModel.get_or_create(
#             season_name=season_name, experiment_id=experiment.id
#         )
#         site = SiteModel.get_or_create(site_name=site_name, experiment_id=experiment.id)

#         plot = PlotModel.get_or_create(
#             experiment_id=experiment.id,
#             season_id=season.id,
#             site_id=site.id,
#             plot_number=plot_number,
#             plot_row_number=plot_row_number,
#             plot_column_number=plot_column_number,
#         )

#         new_instance = cls.db_model.get_or_create(
#             timestamp=timestamp,
#             collection_date=collection_date,
#             model_id=model.id if model else None,
#             model_data=model_data,
#             record_info=record_info,
#             experiment_id=experiment.id if experiment else None,
#             season_id=season.id if season else None,
#             site_id=site.id if site else None,
#             plot_id=plot.id,
#         )

#         logger_service.info(
#             "API",
#             f"Created a new model record with id {new_instance.id} in the database",
#         )

#         new_instance = cls.model_validate(new_instance)
#         new_instance = cls.process_record(new_instance)
#         return new_instance

#     @classmethod
#     def create_bulk(
#         cls,
#         timestamps: List[datetime],
#         collection_dates: List[date],
#         model_name: str,
#         experiment_name: str,
#         season_name: str,
#         site_name: str,
#         plot_numbers: List[int],
#         plot_row_numbers: List[int],
#         plot_column_numbers: List[int],
#         model_data: List[dict] = None,
#         record_info: List[dict] = None,
#     ):

#         model = ModelModel.get_by_parameter("model_name", model_name)
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
#                 "model_id": model.id if model else None,
#                 "experiment_id": experiment.id if experiment else None,
#                 "season_id": season.id if season else None,
#                 "site_id": site.id if site else None,
#                 "plot_id": plot.id if plot else None,
#                 "model_data": model_data[i] if model_data else None,
#                 "record_info": record_info[i] if record_info else None,
#             }

#             records_to_add.append(record)

#         # Bulk insert the records
#         records = cls.db_model.insert_bulk("model_records_unique", records_to_add)

#         for record in track(records, description="Processing Model Records"):
#             model_data = record.model_data
#             if any(key in model_data for key in ["file", "file_path"]):
#                 record = cls.model_validate(record)
#                 record = cls.process_record(record)

#         logger_service.info(
#             "API",
#             f"Created {len(records)} new procedure records in the database",
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

#     def set_info(self, record_info: dict) -> "ModelRecord":
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

#     def add_info(self, record_info: dict) -> "ModelRecord":
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

#     def remove_info(self, keys_to_remove: List[str]) -> "ModelRecord":
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
#     ) -> "ModelRecord":
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

#     def process_record(self):
#         """
#         Process the record
#         """
#         self.refresh()
#         model_data = self.model_data
#         for key, value in model_data.items():
#             if key in ["file", "file_path"]:
#                 self.upload_model_data_file(value)

#         logger_service.info(
#             "API",
#             f"Processed record with id {self.id}",
#         )
#         return self

#     def generate_file_uri(self, absolute_file_path: str) -> str:
#         """
#         Generate a file URI for a file

#         Args:
#         absolute_file_path (str): The absolute file path

#         Returns:
#         str: The file URI
#         """
#         if not os.path.exists(absolute_file_path):
#             raise FileNotFoundError(f"File not found at path {absolute_file_path}")

#         file_name = os.path.basename(absolute_file_path)
#         collection_date = self.collection_date
#         file_uri = (
#             f"model_data/{self.collection_date}/{self.model.model_name}/{file_name}"
#         )
#         return file_uri

#     def upload_model_data_file(self, absolute_file_path: str) -> str:
#         """
#         Upload a file associated with the model data

#         Args:
#         absolute_file_path (str): The absolute file path

#         Returns:
#         str: The file URI
#         """
#         file_uri = self.generate_file_uri(absolute_file_path)
#         file_tags = {
#             "model_name": self.model.model_name if self.model else None,
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
#         self.update(model_data={"file_uri": file_uri})
#         logger_service.info(
#             "API",
#             f"Uploaded model data file for record with id {self.id}",
#         )

#     def download_file(self) -> str:
#         self.refresh()
#         model_data = self.model_data
#         file_uri = model_data.get("file_uri", None)
#         if not file_uri:
#             return None

#         file_path = storage_service.download_file(file_uri)
#         logger_service.info(
#             "API",
#             f"Downloaded model data file for record with id {self.id}",
#         )
#         return file_path

#     def get_file_url(self) -> str:
#         self.refresh()
#         model_data = self.model_data
#         file_uri = model_data.get("file_uri", None)
#         if not file_uri:
#             return None

#         file_url = storage_service.get_presigned_download_url(file_uri)
#         logger_service.info(
#             "API",
#             f"Got file URL for record with id {self.id}",
#         )
#         return file_url

#     @classmethod
#     def search(cls, **kwargs):
#         """
#         Search for model records in the database.

#         Args:
#         **kwargs: The search parameters

#         Returns:
#         List[ModelRecord]: A list of the model records that match the search parameters
#         """

#         searched_records = ModelRecordsViewModel.stream(**kwargs)
#         for record in searched_records:
#             record = cls.model_validate(record)
#             yield record

#         logger_service.info(
#             "API",
#             f"Retrieved {len(searched_records)} model records from the database",
#         )
