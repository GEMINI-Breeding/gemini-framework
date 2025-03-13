from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.enums import GEMINIDatasetType
from gemini.api.dataset_type import DatasetType
from gemini.api.dataset_record import DatasetRecord
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.dataset_types import DatasetTypeModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.associations import ExperimentDatasetModel
from gemini.db.models.views.experiment_views import ExperimentDatasetsViewModel

from datetime import date

class Dataset(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "dataset_id"))

    collection_date: date
    dataset_name: str
    dataset_info: Optional[dict] = None
    dataset_type_id: int

    @classmethod
    def create(
        cls,
        dataset_name: str,
        dataset_info: dict = {},
        dataset_type: GEMINIDatasetType = GEMINIDatasetType.Default,
        collection_date: date = date.today(),
        experiment_name: str = None
    ) -> "Dataset":
        try:

            dataset_type_id = dataset_type.value
            db_instance = DatasetModel.get_or_create(
                collection_date=collection_date,
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type_id=dataset_type_id,
            )
            if experiment_name:
                db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
                if db_experiment:
                    ExperimentDatasetModel.get_or_create(experiment_id=db_experiment.id, dataset_id=db_instance.id)

            dataset = cls.model_validate(db_instance)
            return dataset
        except Exception as e:
            raise e
        
    @classmethod
    def get(cls, dataset_name: str, experiment_name: str = None) -> "Dataset":
        try:
            db_instance = ExperimentDatasetsViewModel.get_by_parameters(
                dataset_name=dataset_name,
                experiment_name=experiment_name
            )
            dataset = cls.model_validate(db_instance)
            return dataset if dataset else None
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Dataset":
        try:
            db_instance = DatasetModel.get(id)
            dataset = cls.model_validate(db_instance)
            return dataset if dataset else None
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
    def search(
        cls, 
        experiment_name: str = None,
        dataset_name: str = None,
        dataset_info: dict = None,
        dataset_type: GEMINIDatasetType = None,
        collection_date: date = None,
    ) -> List["Dataset"]:
        try:
            if not experiment_name and not dataset_name and not dataset_info and not dataset_type and not collection_date:
                raise ValueError("At least one parameter must be provided.")

            datasets = ExperimentDatasetsViewModel.search(
                experiment_name=experiment_name,
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type=dataset_type,
                collection_date=collection_date,
            )
            datasets = [cls.model_validate(dataset) for dataset in datasets]
            return datasets if datasets else None
        except Exception as e:
            raise e
        
    def update(
            self,
            dataset_name: str = None,
            dataset_info: dict = None,
            dataset_type: GEMINIDatasetType = None,
            collection_date: date = None 
    ) -> "Dataset":
        try:
            if not dataset_name and not dataset_info and not dataset_type and not collection_date:
                raise ValueError("At least one parameter must be provided.")

            current_id = self.id
            dataset = DatasetModel.get(current_id)
            dataset = DatasetModel.update(
                dataset,
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type_id=dataset_type.value if dataset_type else None,
                collection_date=collection_date
            )
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
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e
        
    def get_type(self) -> DatasetType:
        try:
            dataset = DatasetModel.get(self.id)
            dataset_type = DatasetTypeModel.get(dataset.dataset_type_id)
            dataset_type = DatasetType.model_validate(dataset_type)
            return dataset_type if dataset_type else None
        except Exception as e:
            raise e


    def add_record(
        self,
        record: DatasetRecord
    ) -> bool:
        try:
            record.dataset_id = self.id
            record.dataset_name = self.dataset_name
            record.timestamp = record.timestamp if record.timestamp else date.today()

            success = DatasetRecord.add([record])
            return success
        except Exception as e:
            raise e
        
    def add_records(
        self,
        records: List[DatasetRecord]
    ) -> bool:
        try:
            for record in records:
                record.dataset_id = self.id
                record.dataset_name = self.dataset_name
                record.timestamp = record.timestamp if record.timestamp else date.today()

            success = DatasetRecord.add(records)
            return success
        except Exception as e:
            raise e
        
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

  