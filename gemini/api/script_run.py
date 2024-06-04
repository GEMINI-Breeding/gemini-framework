from typing import Optional, List, Any, Union
from gemini.api.base import APIBase
from gemini.models import ScriptRunModel, ScriptModel
from gemini.logger import logger_service

from uuid import UUID

class ScriptRun(APIBase):

    db_model = ScriptRunModel

    script_id: Optional[Union[str, UUID]] = None
    script_run_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        script_name: str,
        script_run_info: dict = None,
    ):
        
        script = ScriptModel.get_by_parameters(script_name=script_name)
        db_instance = cls.db_model.get_or_create(
            script_id=script.id,
            script_run_info=script_run_info
        )
        instance = cls.model_validate(db_instance)
        logger_service.info(
            "API",
            f"Created a new instance of {cls.__name__} with id {instance.id}",
        )
        return instance
    
    @classmethod
    def get_script_runs(cls, script_name: str) -> List["ScriptRun"]:
        script = ScriptModel.get_by_parameters(script_name=script_name)
        db_instances = cls.db_model.get_by_parameters(script_id=script.id)
        instances = [cls.model_validate(db_instance) for db_instance in db_instances]
        logger_service.info("API", f"Retrieved script runs for script {script_name} from the database")
        return instances

    @classmethod
    def get(cls, script_run_id: str) -> "ScriptRun":
        db_instance = cls.db_model.get_by_id(script_run_id)
        logger_service.info("API", f"Retrieved script run with id {script_run_id} from the database")
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        self.model_validate(self)
        logger_service.info("API", f"Retrieved information about {self.id} from the database")
        return self.script_run_info
    
    def set_info(self, script_run_info: Optional[dict] = None) -> "ScriptRun":
        self.update(script_run_info=script_run_info)
        logger_service.info("API", f"Set information about {self.id} in the database")
        return self
    
    def add_info(self, script_run_info: Optional[dict] = None) -> "ScriptRun":
        current_info = self.get_info()
        updated_info = {**current_info, **script_run_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.id} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "ScriptRun":
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.id} in the database")
        return self
