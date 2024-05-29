from pydantic import BaseModel
from gemini.api.base import APIBase
from gemini.models import ModelRunModel, ModelModel
from gemini.logger import logger_service
from typing import Optional, List, Any, Union
from uuid import UUID

class ModelRun(APIBase):

    db_model = ModelRunModel

    model_id : Union[UUID, str]
    model_run_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        model_name: str,
        model_run_info: dict = None
    ):
        
        db_model = ModelModel.get_by_parameters(model_name=model_name)
        db_instance = cls.db_model.get_or_create(
            model_id=db_model.id,
            model_run_info=model_run_info
        )
        instance = cls.model_validate(db_instance)
        logger_service.info(
            "API",
            f"Created a new instance of {cls.__name__} with id {instance.id}",
        )
        return instance

    @classmethod
    def get_model_runs(cls, model_name: str) -> List["ModelRun"]:
        db_model = ModelModel.get_by_parameters(model_name=model_name)
        db_instances = cls.db_model.get_by_parameters(model_id=db_model.id)
        instances = [cls.model_validate(db_instance) for db_instance in db_instances]
        logger_service.info("API", f"Retrieved model runs for model {model_name} from the database")
        return instances
    
    @classmethod
    def get(cls, model_run_id: str) -> "ModelRun":
        db_instance = cls.db_model.get_by_id(model_run_id)
        logger_service.info("API", f"Retrieved model run with id {model_run_id} from the database")
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.id} from the database")
        return self.model_run_info
    
    def set_info(self, model_run_info: Optional[dict] = None) -> "ModelRun":
        self.update(model_run_info=model_run_info)
        logger_service.info("API", f"Set information about {self.id} in the database")
        return self
    
    def add_info(self, model_run_info: Optional[dict] = None) -> "ModelRun":
        current_info = self.get_info()
        updated_info = {**current_info, **model_run_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information about {self.id} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "ModelRun":
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.id} in the database")
        return self




