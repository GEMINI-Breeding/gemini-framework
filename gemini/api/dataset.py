from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.enums import GEMINIDatasetType
from gemini.api.dataset_record import DatasetRecord
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import ExperimentDatasetsViewModel

from datetime import date, datetime

class Dataset(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "dataset_id"))

    collection_date: date
    dataset_name: str
    dataset_info: Optional[dict] = None
    dataset_type_id: int

    @classmethod
    def create(
        cls,
        collection_date: date,
        dataset_name: str,
        dataset_info: dict = {},
        dataset_type: GEMINIDatasetType = GEMINIDatasetType.Default,
        experiment_name: str = "Default",
    ) -> "Dataset":
        try:

            dataset_type_id = dataset_type.value
            db_instance = DatasetModel.get_or_create(
                collection_date=collection_date,
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type_id=dataset_type_id,
            )
            dataset = cls.model_validate(db_instance)

            experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
            if experiment:
                experiment.datasets.append(dataset)

            return dataset
        except Exception as e:
            raise e
        
    @classmethod
    def get(cls, dataset_name: str) -> "Dataset":
        try:
            db_instance = DatasetModel.get_by_parameters(
                dataset_name=dataset_name,
            )
            dataset = cls.model_validate(db_instance)
            return dataset
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Dataset":
        try:
            db_instance = DatasetModel.get(id)
            dataset = cls.model_validate(db_instance)
            return dataset
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["Dataset"]:
        try:
            datasets = DatasetModel.all()
            datasets = [cls.model_validate(dataset) for dataset in datasets]
            return datasets if datasets else None
        except Exception as e:
            raise e
        

    @classmethod
    def search(cls, **search_parameters) -> List["Dataset"]:
        try:
            datasets = ExperimentDatasetsViewModel.search(**search_parameters)
            datasets = [cls.model_validate(dataset) for dataset in datasets]
            return datasets if datasets else None
        except Exception as e:
            raise e
        
    def update(self, **update_parameters) -> "Dataset":
        try:
            current_id = self.id
            dataset = DatasetModel.get(current_id)
            dataset = DatasetModel.update(dataset, **update_parameters)
            dataset = self.model_validate(dataset)
            self.refresh()
            return dataset
        except Exception as e:
            raise e
        
    def delete(self) ->  bool:
        try:
            current_id = self.id
            dataset = DatasetModel.get(current_id)
            DatasetModel.delete(dataset)
            return True
        except Exception as e:
            raise e
        
    def refresh(self) -> "Dataset":
        try:
            db_instance = DatasetModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            raise e
        
    def add_record(
        self,
        record = DatasetRecord
    ) -> bool:
        try:
            if record.timestamp is None:
                record.timestamp = datetime.now()
            if record.collection_date is None:
                record.collection_date = record.timestamp.date()
            if record.dataset_name is None:
                record.dataset_name = self.dataset_name
            if record.record_info is None:
                record.record_info = {}

            record.dataset_id = self.id

            success = DatasetRecord.add([record])
            return success
        except Exception as e:
            return False


    def add_records(
            self,
            records: List[DatasetRecord]
    ) -> bool:
        try:
            for record in records:
                if record.timestamp is None:
                    record.timestamp = datetime.now()
                if record.collection_date is None:
                    record.collection_date = record.timestamp.date()
                if record.dataset_name is None:
                    record.dataset_name = self.dataset_name
                if record.record_info is None:
                    record.record_info = {}

                record.dataset_id = self.id
                
            success = DatasetRecord.add(records)
            return success
        except Exception as e:
            return False
        
    def get_records(
            self,
            collection_date: date = None,
            experiment_name: str = None,
            season_name: str = None,
            site_name: str = None,
            record_info: dict = None
    ) -> List[DatasetRecord]:
        try:
            record_info = record_info if record_info else {}
            record_info = {k: v for k, v in record_info.items() if v is not None}

            records = DatasetRecord.search(
                dataset_id=self.id,
                collection_date=collection_date,
                dataset_name=self.dataset_name,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                record_info=record_info
            )
            return records
        except Exception as e:
            raise e

