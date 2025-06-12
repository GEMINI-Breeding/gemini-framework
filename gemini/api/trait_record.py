from typing import Optional, List, Generator
from uuid import UUID
from tqdm import tqdm

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.api.plot import Plot
from gemini.db.models.traits import TraitModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.columnar.trait_records import TraitRecordModel
from gemini.db.models.views.trait_records_immv import TraitRecordsIMMVModel
from gemini.db.models.views.validation_views import ValidTraitDatasetCombinationsViewModel
from gemini.db.models.views.dataset_views import TraitDatasetsViewModel
from gemini.db.models.views.plot_view import PlotViewModel
from gemini.db.models.views.experiment_views import (
    ExperimentTraitsViewModel,
    ExperimentDatasetsViewModel,
    ExperimentSitesViewModel,
    ExperimentSeasonsViewModel,
)

from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.associations import TraitDatasetModel

from datetime import date, datetime

class TraitRecord(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "trait_record_id"))

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[ID] = None
    dataset_name: Optional[str] = None
    trait_id: Optional[ID] = None
    trait_name: Optional[str] = None
    trait_value: Optional[float] = None
    experiment_id: Optional[ID] = None
    experiment_name : Optional[str] = None
    season_id: Optional[ID] = None
    season_name: Optional[str] = None
    site_id: Optional[ID] = None
    site_name: Optional[str] = None
    plot_id: Optional[ID] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    record_info: Optional[dict] = None

    def __str__(self):
        return f"TraitRecord(id={self.id}, timestamp={self.timestamp}, trait_name={self.trait_name}, dataset_name={self.dataset_name}, experiment_name={self.experiment_name}, site_name={self.site_name}, season_name={self.season_name}, plot_number={self.plot_number}, plot_row_number={self.plot_row_number}, plot_column_number={self.plot_column_number})"

    def __repr__(self):
        return f"TraitRecord(id={self.id}, timestamp={self.timestamp}, trait_name={self.trait_name}, dataset_name={self.dataset_name}, experiment_name={self.experiment_name}, site_name={self.site_name}, season_name={self.season_name}, plot_number={self.plot_number}, plot_row_number={self.plot_row_number}, plot_column_number={self.plot_column_number})"
    
    @classmethod
    def exists(
        cls,
        timestamp: datetime,
        trait_name: str,
        dataset_name: str,
        experiment_name: str,
        site_name: str,
        season_name: str,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None
    ) -> bool:
        try:
            exists = TraitRecordModel.exists(
                timestamp=timestamp,
                trait_name=trait_name,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number
            )
            return exists
        except Exception as e:
            print(f"Error checking existence of TraitRecord: {e}")
            raise e
        
    @classmethod
    def create(
        cls,
        timestamp: datetime = datetime.now(),
        collection_date: date = None,
        dataset_name: str = None,
        trait_name: str = None,
        trait_value: float = None,
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        record_info: dict = {},
        insert_on_create: bool = True
    ) -> Optional["TraitRecord"]:
        try:
            if not any([experiment_name, site_name, season_name]):
                raise ValueError("At least one of experiment_name, site_name, or season_name must be provided.")
            if not trait_name:
                raise ValueError("Trait name is required.")
            if not dataset_name:
                raise ValueError("Dataset name is required.")
            if not all([plot_number, plot_row_number, plot_column_number]):
                raise ValueError("Plot information (number, row, column) is required if any is provided.")
            if not timestamp:
                timestamp = datetime.now()
            if not collection_date:
                collection_date = timestamp.date()
            if not trait_value:
                raise ValueError("Trait value is required.")
            trait_record = TraitRecord(
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_name=dataset_name,
                trait_name=trait_name,
                trait_value=trait_value,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                record_info=record_info
            )
            if insert_on_create:
                insert_success, inserted_record_ids = cls.insert([trait_record])
                if not insert_success:
                    print(f"Failed to insert TraitRecord: {trait_record}")
                    return None
                if not inserted_record_ids or len(inserted_record_ids) == 0:
                    print(f"No TraitRecord IDs returned after insertion.")
                    return None
                inserted_record_id = inserted_record_ids[0]
                trait_record = cls.get_by_id(inserted_record_id)
            return trait_record
        except Exception as e:
            print(f"Error creating TraitRecord: {e}")
            return None
        
    @classmethod
    def insert(cls, records: List["TraitRecord"]) -> tuple[bool, List[str]]:
        try:
            if not records or len(records) == 0:
                print(f"No records provided to insert.")
                return False, []
            records_to_insert = []
            for record in records:
                record_dict = record.model_dump()
                record_dict = {k: v for k, v in record_dict.items() if v is not None}
                records_to_insert.append(record_dict)
            print(f"Inserting {len(records_to_insert)} TraitRecords.")
            inserted_record_ids = TraitRecordModel.insert_bulk('trait_records_unique', records_to_insert)
            print(f"Inserted {len(inserted_record_ids)} TraitRecords.")
            return True, inserted_record_ids
        except Exception as e:
            print(f"Error inserting TraitRecords: {e}")
            return False, []
        
    @classmethod
    def get(
        cls,
        timestamp: datetime,
        trait_name: str,
        dataset_name: str,
        experiment_name: str,
        site_name: str,
        season_name: str,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None
    ) -> Optional["TraitRecord"]:
        try:
            if not timestamp:
                print("Timestamp is required to get TraitRecord.")
                return None
            if not trait_name:
                print("Trait name is required to get TraitRecord.")
                return None
            if not dataset_name:
                print("Dataset name is required to get TraitRecord.")
                return None
            if not experiment_name and not site_name and not season_name:
                print("At least one of experiment_name, site_name, or season_name is required to get TraitRecord.")
                return None
            if not all([plot_number, plot_row_number, plot_column_number]):
                print("Plot information (number, row, column) is required if any is provided.")
                return None
            trait_record = TraitRecordsIMMVModel.get_by_parameters(
                timestamp=timestamp,
                trait_name=trait_name,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number
            )
            if not trait_record:
                print("TraitRecord not found with the provided parameters.")
                return None
            trait_record = cls.model_validate(trait_record)
            return trait_record
        except Exception as e:
            print(f"Error getting TraitRecord: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["TraitRecord"]:
        try:
            db_instance = TraitRecordModel.get(id)
            if not db_instance:
                print(f"TraitRecord with ID {id} not found.")
                return None
            record = cls.model_validate(db_instance)
            return record
        except Exception as e:
            print(f"Error getting TraitRecord by ID {id}: {e}")
            return None
        
    @classmethod
    def get_all(cls, limit: int = 100) -> Optional[List["TraitRecord"]]:
        try:
            records = TraitRecordModel.all(limit=limit)
            if not records or len(records) == 0:
                print(f"No TraitRecords found")
                return None
            records = [cls.model_validate(instance) for instance in records]
            return records
        except Exception as e:
            print(f"Error getting all TraitRecords: {e}")
            return None

    @classmethod
    def search(
        cls,
        dataset_name: str = None,
        trait_name: str = None,
        trait_value: float = None,
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        collection_date: date = None,
        record_info: dict = None
    ) -> Generator["TraitRecord", None, None]:
        try:
            if not any([dataset_name, trait_name, trait_value, experiment_name, site_name, season_name, plot_number, plot_row_number, plot_column_number, collection_date, record_info]):
                print("At least one search parameter must be provided.")
                return
            records = TraitRecordsIMMVModel.stream(
                dataset_name=dataset_name,
                trait_name=trait_name,
                trait_value=trait_value,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                collection_date=collection_date,
                record_info=record_info
            )
            for record in records:
                record = cls.model_validate(record)
                yield record
        except Exception as e:
            print(f"Error searching TraitRecords: {e}")
            yield from []

    def update(
        self,
        trait_value: float = None,
        record_info: dict = None
    ) -> Optional["TraitRecord"]:
        try:
            if not any([trait_value, record_info]):
                print("At least one parameter must be provided to update TraitRecord.")
                return None
            current_id = self.id
            trait_record = TraitRecordModel.get(current_id)
            if not trait_record:
                print(f"TraitRecord with ID {current_id} not found.")
                return None
            trait_record = TraitRecordModel.update(
                trait_record,
                trait_value=trait_value,
                record_info=record_info
            )
            trait_record = self.model_validate(trait_record)
            self.refresh()
            return trait_record
        except Exception as e:
            print(f"Error updating TraitRecord: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            trait_record = TraitRecordModel.get(current_id)
            if not trait_record:
                print(f"TraitRecord with ID {current_id} not found.")
                return False
            TraitRecordModel.delete(trait_record)
            return True
        except Exception as e:
            print(f"Error deleting TraitRecord: {e}")
            return False
        
    def refresh(self) -> Optional["TraitRecord"]:
        try:
            db_instance = TraitRecordModel.get(self.id)
            if not db_instance:
                print(f"TraitRecord with ID {self.id} not found.")
                return None
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != 'id':
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing TraitRecord: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            trait_record = TraitRecordModel.get(current_id)
            if not trait_record:
                print(f"TraitRecord with ID {current_id} not found.")
                return None
            record_info = trait_record.record_info
            if not record_info:
                print(f"No record info found for TraitRecord with ID {current_id}.")
                return None
            return record_info
        except Exception as e:
            print(f"Error getting record info for TraitRecord: {e}")
            return None
        
    def set_info(self, record_info: dict) -> Optional["TraitRecord"]:
        try:
            current_id = self.id
            trait_record = TraitRecordModel.get(current_id)
            if not trait_record:
                print(f"TraitRecord with ID {current_id} not found.")
                return None
            TraitRecordModel.update(
                trait_record,
                record_info=record_info
            )
            trait_record = self.model_validate(trait_record)
            self.refresh()
            return trait_record
        except Exception as e:
            print(f"Error setting record info for TraitRecord: {e}")
            return None
