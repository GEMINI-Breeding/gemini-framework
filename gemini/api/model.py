from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.dataset import Dataset
from gemini.db.models.models import ModelModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import ExperimentModelsViewModel

class Model(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "model_id"))

    model_name: str
    model_url: Optional[str] = None
    model_info: Optional[dict] = None

    datasets: List[Dataset]


    @classmethod
    def create(
        cls,
        model_name: str,
        model_url: str,
        model_info: dict = {},
        experiment_name: str = "Default",
    ):
        try:
            db_instance = ModelModel.get_or_create(
                model_name=model_name,
                model_url=model_url,
                model_info=model_info,
            )
            model = cls.model_validate(db_instance)
            experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
            if experiment:
                experiment.models.append(model)
            return model
        except Exception as e:
            raise e
        
    @classmethod
    def get(cls, model_name: str, model_url: str) -> "Model":
        try:
            db_instance = ModelModel.get_by_parameters(
                model_name=model_name,
                model_url=model_url,
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
    def search(cls, **search_parameters) -> List["Model"]:
        try:
            models = ExperimentModelsViewModel.search(**search_parameters)
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