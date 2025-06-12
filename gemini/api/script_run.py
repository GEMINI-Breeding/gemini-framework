from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.script_runs import ScriptRunModel
from gemini.db.models.scripts import ScriptModel
from gemini.db.models.views.run_views import ScriptRunsViewModel


class ScriptRun(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "script_run_id"))

    script_id : Optional[ID] 
    script_run_info: Optional[dict] = None

    def __str__(self):
        return f"ScriptRun(id={self.id}, script_id={self.script_id}, script_run_info={self.script_run_info})"

    def __repr__(self):
        return f"ScriptRun(id={self.id}, script_id={self.script_id}, script_run_info={self.script_run_info})"

    @classmethod
    def exists(
        cls,
        script_run_info: dict,
        script_name: str = None
    ) -> bool:
        try:
            exists = ScriptRunsViewModel.exists(
                script_name=script_name,
                script_run_info=script_run_info
            )
            return exists
        except Exception as e:
            print(f"Error checking existence of script run: {e}")
            return False

    @classmethod
    def create(
        cls,
        script_run_info: dict = {},
        script_name: str = None
    ) -> Optional["ScriptRun"]:
        try:
            db_instance = ScriptRunModel.get_or_create(
                script_run_info=script_run_info,
            )
            script_run = cls.model_validate(db_instance)
            if script_name:
                script_run.associate_script(script_name)
            return script_run
        except Exception as e:
            print(f"Error creating script run: {e}")
            return None

    @classmethod
    def get(cls, script_run_info: dict, script_name: str = None) -> Optional["ScriptRun"]:
        try:
            db_script = ScriptModel.get_by_parameters(script_name=script_name)
            if not db_script:
                print(f"Script with name {script_name} does not exist.")
                return None
            db_instance = ScriptRunsViewModel.get_by_parameters(
                script_run_info=script_run_info,
                script_name=script_name
            )
            if not db_instance:
                print(f"Script run with info {script_run_info} and script name {script_name} not found.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting script run: {e}")
            return None

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["ScriptRun"]:
        try:
            db_instance = ScriptRunModel.get(id)
            if not db_instance:
                print(f"Script run with id {id} not found.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting script run by id: {e}")
            return None

    @classmethod
    def get_all(cls) -> Optional[List["ScriptRun"]]:
        try:
            script_runs = ScriptRunModel.all()
            if not script_runs or len(script_runs) == 0:
                print("No script runs found.")
                return None
            script_runs = [cls.model_validate(script_run) for script_run in script_runs]
            return script_runs
        except Exception as e:
            print(f"Error getting all script runs: {e}")
            return None

    @classmethod
    def search(
        cls,
        script_run_info: dict = None,
        script_name: str = None
    ) -> Optional[List["ScriptRun"]]:
        try:
            if not any([script_name, script_run_info]):
                print("At least one of script_name or script_run_info must be provided.")
                return None
            script_runs = ScriptRunsViewModel.search(
                script_run_info=script_run_info,
                script_name=script_name
            )
            if not script_runs or len(script_runs) == 0:
                print("No script runs found for the given search criteria.")
                return None
            script_runs = [cls.model_validate(script_run) for script_run in script_runs]
            return script_runs
        except Exception as e:
            print(f"Error searching script runs: {e}")
            return None

    def update(self, script_run_info: dict = None) -> Optional["ScriptRun"]:
        try:
            if not script_run_info:
                print("Model run info cannot be empty.")
                return None
            current_id = self.id
            script_run = ScriptRunModel.get(current_id)
            if not script_run:
                print(f"Script run with id {current_id} does not exist.")
                return None
            script_run = ScriptRunModel.update(
                script_run,
                script_run_info=script_run_info
            )
            instance = self.model_validate(script_run)
            self.refresh()
            return instance
        except Exception as e:
            print(f"Error updating script run: {e}")
            return None

    def delete(self) -> bool:
        try:
            current_id = self.id
            script_run = ScriptRunModel.get(current_id)
            if not script_run:
                print(f"Script run with id {current_id} does not exist.")
                return False
            ScriptRunModel.delete(script_run)
            return True
        except Exception as e:
            print(f"Error deleting script run: {e}")
            return False

    def refresh(self) -> Optional["ScriptRun"]:
        try:
            db_instance = ScriptRunModel.get(self.id)
            if not db_instance:
                print(f"Script run with id {self.id} not found.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and getattr(self, key) != value:
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing script run: {e}")
            return None

    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            script_run = ScriptRunModel.get(current_id)
            if not script_run:
                print(f"Script run with id {current_id} does not exist.")
                return None
            script_run_info = script_run.script_run_info
            if not script_run_info:
                print("ScriptRun info is empty.")
                return {}
            return script_run_info
        except Exception as e:
            print(f"Error getting script run info: {e}")
            return None

    def set_info(self, script_run_info: dict) -> Optional["ScriptRun"]:
        try:
            current_id = self.id
            script_run = ScriptRunModel.get(current_id)
            if not script_run:
                print(f"Script run with id {current_id} does not exist.")
                return None
            script_run = ScriptRunModel.update(
                script_run,
                script_run_info=script_run_info,
            )
            self.script_run_info = script_run.script_run_info
            return self
        except Exception as e:
            print(f"Error setting script run info: {e}")
            return None
        
    def get_associated_script(self):
        try:
            from gemini.api.script import Script
            current_id = self.script_id
            script_run_model = ScriptRunsViewModel.get_by_parameters(
                script_id=current_id
            )
            script_id = script_run_model.script_id
            if not script_id:
                print(f"No script found for script run with id {self.id}.")
                return None
            script = Script.get_by_id(script_id)
            if not script:
                print(f"Script with id {script_id} does not exist.")
                return None
            return script
        except Exception as e:
            print(f"Error getting script for script run: {e}")
            return None

    def associate_script(self, script_name: str):
        try:
            from gemini.api.script import Script
            script = Script.get(script_name=script_name)
            if not script:
                print(f"Script with name {script_name} does not exist.")
                return None
            existing_association = ScriptRunModel.get_by_parameters(
                id=script.id,
                script_run_id=self.id
            )
            if existing_association:
                print(f"Script run with id {self.id} is already associated with script {script_name}.")
                return self
            db_script_run = ScriptRunModel.get(self.id)
            db_script_run = ScriptRunModel.update_parameter(
                db_script_run,
                "script_id",
                script.id
            )
            self.refresh()
            return script
        except Exception as e:
            print(f"Error assigning script to script run: {e}")
            return None

    def unassociate_script(self):
        try:
            from gemini.api.script import Script
            script_run = ScriptRunModel.get(self.id)
            if not script_run:
                print(f"Script run with id {self.id} does not exist.")
                return None
            script = Script.get_by_id(script_run.script_id)
            script_run = ScriptRunModel.update_parameter(
                script_run,
                "script_id",
                None
            )
            self.refresh()
            return script
        except Exception as e:
            print(f"Error unassigning script from script run: {e}")
            return None

    def belongs_to_script(self, script_name: str) -> bool:
        try:
            from gemini.api.script import Script
            script = Script.get(script_name=script_name)
            if not script:
                print(f"Script with name {script_name} does not exist.")
                return False
            assignment_exists = ScriptRunModel.exists(
                script_run_id=self.id,
                script_id=script.id
            )
            return assignment_exists
        except Exception as e:
            print(f"Error checking if script run belongs to script: {e}")
            return False

    