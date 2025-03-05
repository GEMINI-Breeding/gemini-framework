from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.script_runs import ScriptRunModel
from gemini.db.models.scripts import ScriptModel


class ScriptRun(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "script_run_id"))

    script_id : UUID
    script_run_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        script_run_info: dict = {},
        script_name: str = None,
    ) -> "ScriptRun":
        try:
            db_script = ScriptModel.get_by_parameters(script_name=script_name)
            if not db_script:
                raise Exception(f"Script with name {script_name} does not exist.")
            db_instance = ScriptRunModel.get_or_create(
                script_run_info=script_run_info,
                script_id=db_script.id
            )
            script_run = cls.model_validate(db_instance)
            return script_run
        except Exception as e:
            raise e
        
    @classmethod
    def get(cls, script_run_info: dict, script_name: str = None) -> "ScriptRun":
        try:
            db_script = ScriptModel.get_by_parameters(script_name=script_name)
            if not db_script:
                raise Exception(f"Script with name {script_name} does not exist.")
            db_instance = ScriptRunModel.get_by_parameters(
                script_run_info=script_run_info,
                script_id=db_script.id
            )
            script_run = cls.model_validate(db_instance)
            return script_run if script_run else None
        except Exception as e:
            raise e
        
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "ScriptRun":
        try:
            db_instance = ScriptRunModel.get(id)
            script_run = cls.model_validate(db_instance)
            return script_run if script_run else None
        except Exception as e:
            raise e
        
    @classmethod
    def get_all(cls) -> List["ScriptRun"]:
        try:
            script_runs = ScriptRunModel.all()
            script_runs = [cls.model_validate(script_run) for script_run in script_runs]
            return script_runs if script_runs else None
        except Exception as e:
            raise e
        
    @classmethod
    def search(
        cls,
        script_run_info: dict = None,
        script_name: str = None
    ) -> List["ScriptRun"]:
        try:
            if not script_name and not script_run_info:
                raise Exception("Either script_name or script_run_info must be provided.")
            
            db_model = ScriptModel.get_by_parameters(script_name=script_name)
            if not db_model:
                raise Exception(f"Script with name {script_name} does not exist.")
            
            script_runs = ScriptRunModel.search(
                script_run_info=script_run_info,
                script_id=db_model.id
            )

            script_runs = [cls.model_validate(script_run) for script_run in script_runs]
            return script_runs if script_runs else None
        except Exception as e:
            raise e
        

    def update(
        self,
        script_run_info: dict = None
    ) -> "ScriptRun":
        try:
            if not script_run_info:
                raise Exception("script_run_info must be provided.")
            current_id = self.id
            script_run = ScriptRunModel.get(id=current_id)
            script_run = ScriptRunModel.update(
                script_run,
                script_run_info=script_run_info
            )
            script_run = self.model_validate(script_run)
            self.refresh()
            return script_run
        except Exception as e:
            raise e
        
    def delete(self) -> bool:
        try:
            current_id = self.id
            script_run = ScriptRunModel.get(current_id)
            ScriptRunModel.delete(script_run)
            return True
        except Exception as e:
            raise e
        
    def refresh(self) -> "ScriptRun":
        try:
            db_instance = ScriptRunModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e
                    