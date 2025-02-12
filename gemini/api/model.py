from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.dataset import Dataset
from gemini.api.model_record import ModelRecord
from gemini.db.models.models import ModelModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.associations import ExperimentModelModel
from gemini.db.models.views.experiment_views import ExperimentModelsViewModel

from datetime import date, datetime

class Model(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "model_id"))

    model_name: str
    model_url: Optional[str] = None
    model_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        model_name: str,
        model_url: str = None,
        model_info: dict = {},
        experiment_name: str = None,
    ):
        try:
            db_instance = ModelModel.get_or_create(
                model_name=model_name,
                model_url=model_url,
                model_info=model_info,
            )

            if experiment_name:
                db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
                if db_experiment:
                    ExperimentModelModel.get_or_create(experiment_id=db_experiment.id, model_id=db_instance.id)

            model = cls.model_validate(db_instance)
            return model
        except Exception as e:
            raise e
        
    @classmethod
    def get(cls, model_name: str, experiment_name: str = None) -> "Model":
        try:
            db_instance = ModelModel.get_by_parameters(
                model_name=model_name,
                experiment_name=experiment_name
            )
            model = cls.model_validate(db_instance)
            return model
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Model":
        try:
            db_instance = ModelModel.get(id)
            model = cls.model_validate(db_instance)
            return model
        except Exception as e:
            raise e
        
    
    @classmethod
    def get_all(cls) -> List["Model"]:
        try:
            models = ModelModel.all()
            return [cls.model_validate(model) for model in models]
        except Exception as e:
            raise e
        
    @classmethod
    def search(
        cls, 
        experiment_name: str = None,
        model_name: str = None,
        model_info: dict = None,
        model_url: str = None
    ) -> List["Model"]:
        try:
            models = ExperimentModelsViewModel.search(
                experiment_name=experiment_name,
                model_name=model_name,
                model_info=model_info,
                model_url=model_url
            )
            return [cls.model_validate(model) for model in models]
        except Exception as e:
            raise e
        
    
    def update(self, **update_parameters) -> "Model":
        try:
            current_id = self.id
            model = ModelModel.get(current_id)
            model = ModelModel.update(current_id, **update_parameters)
            model = self.model_validate(model)
            self.refresh()
            return model
        except Exception as e:
            raise e
        
    
    def delete(self) -> bool:
        try:
            current_id = self.id
            model = ModelModel.get(current_id)
            ModelModel.delete(model)
            return True
        except Exception as e:
            return False
        
    def refresh(self) -> "Model":
        try:
            db_instance = ModelModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            raise e
        

    def get_datasets(self) -> List[Dataset]:
        try:
            datasets = self.datasets
            return datasets
        except Exception as e:
            raise e
        

    def add_record(
        self,
        record: "ModelRecord"
    ) -> bool:
        try:
            if record.timestamp is None:
                record.timestamp = datetime.now()
            if record.collection_date is None:
                record.collection_date = record.timestamp.date()
            if record.dataset_name is None:
                record.dataset_name = f"{self.model_name} Dataset"
            if record.model_name is None:
                record.model_name = self.model_name
            if record.record_info is None:
                record.record_info = {}

            record.model_id = self.id

            success = ModelRecord.add([record])
            return success
        except Exception as e:
            return False
        
    def add_records(
        self,
        records: List["ModelRecord"]
    ) -> bool:
        try:
            for record in records:
                if record.timestamp is None:
                    record.timestamp = datetime.now()
                if record.collection_date is None:
                    record.collection_date = record.timestamp.date()
                if record.dataset_name is None:
                    record.dataset_name = f"{self.model_name} Dataset"
                if record.model_name is None:
                    record.model_name = self.model_name
                if record.record_info is None:
                    record.record_info = {}

                record.model_id = self.id

            success = ModelRecord.add(records)
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
    ) -> List["ModelRecord"]:
        try:
            record_info = record_info if record_info else {}
            record_info = {k: v for k, v in record_info.items() if v is not None}

            records = ModelRecord.search(
                model_id=self.id,
                collection_date=collection_date,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                record_info=record_info
            )
            return records
        except Exception as e:
            raise e
        
    
                
     

            