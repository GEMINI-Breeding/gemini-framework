from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.model_runs import ModelRunModel
from gemini.db.models.models import ModelModel
from gemini.db.models.views.run_views import ModelRunsViewModel

from datetime import date, datetime

class ModelRun(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "model_run_id"))

    model_id : UUID
    model_run_info: Optional[dict] = None

    @classmethod
    def exists(
        cls,
        model_name: str = None,
        model_run_info: dict = None,
    ) -> bool:
        try:
            exists = ModelRunsViewModel.exists(
                model_name=model_name,
                model_run_info=model_run_info
            )
            return exists
        except Exception as e:
            raise e
        
    def get_info(self) -> dict:
        try:
            current_id = self.id
            model_run = ModelRunModel.get(current_id)
            model_run_info = model_run.model_run_info
            if not model_run_info:
                raise Exception("ModelRun info is empty.")
            return model_run_info
        except Exception as e:
            raise e
        
    def set_info(self, model_run_info: dict) -> "ModelRun":
        try:
            current_id = self.id
            model_run = ModelRunModel.get(current_id)
            model_run = ModelRunModel.update(
                model_run,
                model_run_info=model_run_info,
            )
            model_run = self.model_validate(model_run)
            self.refresh()
            return model_run
        except Exception as e:
            raise e

    @classmethod
    def create(
        cls,
        model_run_info: dict = {},
        model_name: str = None,
    ) -> "ModelRun":
        try:
            db_model = ModelModel.get_by_parameters(model_name=model_name)
            if not db_model:
                raise Exception(f"Model with name {model_name} does not exist.")
            db_instance = ModelRunModel.get_or_create(
                model_run_info=model_run_info,
                model_id=db_model.id
            )
            model_run = cls.model_validate(db_instance)
            return model_run
        except Exception as e:
            raise e
        
    @classmethod
    def get(cls, model_run_info: dict, model_name: str = None) -> "ModelRun":
        try:
            db_model = ModelModel.get_by_parameters(model_name=model_name)
            if not db_model:
                raise Exception(f"Model with name {model_name} does not exist.")
            db_instance = ModelRunModel.get_by_parameters(
                model_run_info=model_run_info,
                model_id=db_model.id
            )
            model_run = cls.model_validate(db_instance) if db_instance else None
            return model_run
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "ModelRun":
        try:
            db_instance = ModelRunModel.get(id)
            model_run = cls.model_validate(db_instance) if db_instance else None
            return model_run
        except Exception as e:
            raise e
        
    @classmethod
    def get_all(cls) -> List["ModelRun"]:
        try:
            model_runs = ModelRunModel.all()
            model_runs = [cls.model_validate(model_run) for model_run in model_runs]
            return model_runs if model_runs else None
        except Exception as e:
            raise e
        
    @classmethod
    def search(
        cls,
        model_run_info: dict = None,
        model_name: str = None
    ) -> List["ModelRun"]:
        try:

            if not model_name and not model_run_info:
                raise Exception("At least one of model_name or model_run_info must be provided.")

            db_model = ModelModel.get_by_parameters(model_name=model_name)
            if not db_model:
                raise Exception(f"Model with name {model_name} does not exist.")
            model_runs = ModelRunModel.search(
                model_run_info=model_run_info,
                model_id=db_model.id
            )
            model_runs = [cls.model_validate(model_run) for model_run in model_runs]
            return model_runs if model_runs else None
        except Exception as e:
            raise e
        
    def update(self, model_run_info: dict = None) -> "ModelRun":
        try:
            if not model_run_info:
                raise Exception("Model info cannot be empty.")
            current_id = self.id
            model_run = ModelRunModel.get(current_id)
            model_run = ModelRunModel.update(
                model_run,
                model_run_info=model_run_info   
            )
            model_run = self.model_validate(model_run)
            self.refresh()
            return model_run
        except Exception as e:
            raise e
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            model_run = ModelRunModel.get(current_id)
            ModelRunModel.delete(model_run)
            return True
        except Exception as e:
            raise e
        
    def refresh(self) -> "ModelRun":
        try:
            db_instance = ModelRunModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e
