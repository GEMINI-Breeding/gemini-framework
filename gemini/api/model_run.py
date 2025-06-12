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

    model_id : Optional[ID] = None
    model_run_info: Optional[dict] = None

    def __str__(self):
        return f"ModelRun(id={self.id}, model_id={self.model_id}, model_run_info={self.model_run_info})"
    
    def __repr__(self):
        return f"ModelRun(id={self.id}, model_id={self.model_id}, model_run_info={self.model_run_info})"

    @classmethod
    def exists(
        cls,
        model_run_info: dict,
        model_name: str = None
    ) -> bool:
        try:
            exists = ModelRunsViewModel.exists(
                model_name=model_name,
                model_run_info=model_run_info
            )
            return exists
        except Exception as e:
            print(f"Error checking existence of model run: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        model_run_info: dict = {},
        model_name: str = None
    ) -> Optional["ModelRun"]:
        try:
            db_instance = ModelRunModel.get_or_create(
                model_run_info=model_run_info
            )
            model_run = cls.model_validate(db_instance)
            if model_name:
                model_run.associate_model(model_name=model_name)
            return model_run
        except Exception as e:
            print(f"Error creating model run: {e}")
            return None
        
    @classmethod
    def get(cls, model_run_info: dict, model_name: str = None) -> Optional["ModelRun"]:
        try:
            db_instance = ModelRunsViewModel.get_by_parameters(
                model_run_info=model_run_info,
                model_name=model_name
            )
            if not db_instance:
                print(f"Model run with info {model_run_info} and model name {model_name} not found.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting model run: {e}")
            return None
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["ModelRun"]:
        try:
            db_instance = ModelRunModel.get(id)
            if not db_instance:
                print(f"Model run with id {id} not found.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting model run by id: {e}")
            return None
        
    @classmethod
    def get_all(cls) -> Optional[List["ModelRun"]]:
        try:
            model_runs = ModelRunModel.all()
            if not model_runs or len(model_runs) == 0:
                print("No model runs found.")
                return None
            model_runs = [cls.model_validate(model_run) for model_run in model_runs]
            return model_runs
        except Exception as e:
            print(f"Error getting all model runs: {e}")
            return None
        
    @classmethod
    def search(
        cls,
        model_run_info: dict = None,
        model_name: str = None
    ) -> Optional[List["ModelRun"]]:
        try:
            if not any([model_name, model_run_info]):
                print("At least one of model_name or model_run_info must be provided.")
                return None
            model_runs = ModelRunsViewModel.search(
                model_run_info=model_run_info,
                model_name=model_name
            )
            if not model_runs or len(model_runs) == 0:
                print("No model runs found for the given search criteria.")
                return None
            model_runs = [cls.model_validate(model_run) for model_run in model_runs]
            return model_runs
        except Exception as e:
            print(f"Error searching model runs: {e}")
            return None
        
    def update(self, model_run_info: dict = None) -> Optional["ModelRun"]:
        try:
            if not model_run_info:
                print("Model run info cannot be empty.")
                return None
            current_id = self.id
            model_run = ModelRunModel.get(current_id)
            if not model_run:
                print(f"Model run with id {current_id} does not exist.")
                return None
            model_run = ModelRunModel.update(
                model_run,
                model_run_info=model_run_info   
            )
            instance = self.model_validate(model_run)
            self.refresh()
            return instance
        except Exception as e:
            print(f"Error updating model run: {e}")
            return None
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            model_run = ModelRunModel.get(current_id)
            if not model_run:
                print(f"Model run with id {current_id} does not exist.")
                return False
            ModelRunModel.delete(model_run)
            return True
        except Exception as e:
            print(f"Error deleting model run: {e}")
            return False
        
    def refresh(self) -> Optional["ModelRun"]:
        try:
            db_instance = ModelRunModel.get(self.id)
            if not db_instance:
                print(f"Model run with id {self.id} not found.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing model run: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            model_run = ModelRunModel.get(current_id)
            if not model_run:
                print(f"Model run with id {current_id} does not exist.")
                return None
            model_run_info = model_run.model_run_info
            if not model_run_info:
                print("ModelRun info is empty.")
                return None
            return model_run_info
        except Exception as e:
            print(f"Error getting model run info: {e}")
            return None

    def set_info(self, model_run_info: dict) -> Optional["ModelRun"]:
        try:
            current_id = self.id
            model_run = ModelRunModel.get(current_id)
            if not model_run:
                print(f"Model run with id {current_id} does not exist.")
                return None
            model_run = ModelRunModel.update(
                model_run,
                model_run_info=model_run_info,
            )
            instance = self.model_validate(model_run)
            self.refresh()
            return instance
        except Exception as e:
            print(f"Error setting model run info: {e}")
            return None

    def get_associated_model(self):
        try:
            from gemini.api.model import Model
            if self.model_id is None:
                print("Model run does not have an associated model.")
                return None
            model = Model.get_by_id(self.model_id)
            if not model:
                print(f"Model with id {self.model_id} does not exist.")
                return None
            return model
        except Exception as e:
            print(f"Error getting model for model run: {e}")
            return None

    def associate_model(self, model_name: str):
        try:
            from gemini.api.model import Model
            model = Model.get(model_name=model_name)
            if not model:
                print(f"Model with name {model_name} does not exist.")
                return None
            existing_association = ModelRunModel.get_by_parameters(
                model_id=model.id,
                id=self.id
            )
            if existing_association:
                print(f"Model run with id {self.id} is already associated with model {model_name}.")
                return None
            # Assign the model to the model run
            db_model_run = ModelRunModel.get(self.id)
            if not db_model_run:
                print(f"Model run with id {self.id} does not exist.")
                return None
            db_model_run = ModelRunModel.update_parameter(
                db_model_run,
                "model_id",
                model.id
            )
            self.refresh()
            return model
        except Exception as e:
            print(f"Error assigning model to model run: {e}")
            return None

    def belongs_to_model(self, model_name: str) -> bool:
        try:
            from gemini.api.model import Model
            model = Model.get(model_name=model_name)
            if not model:
                print(f"Model with name {model_name} does not exist.")
                return False
            association_exists = ModelRunModel.exists(
                id=self.id,
                model_id=model.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if model run belongs to model: {e}")
            return False

    def unassociate_model(self):
        try:
            from gemini.api.model import Model
            model_run = ModelRunModel.get(self.id)
            if not model_run:
                print(f"Model run with id {self.id} does not exist.")
                return None
            model = Model.get_by_id(model_run.model_id)
            model_run = ModelRunModel.update_parameter(
                model_run,
                "model_id",
                None
            )
            self.refresh()
            return model
        except Exception as e:
            print(f"Error unassigning model from model run: {e}")
            return None