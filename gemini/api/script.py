from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.dataset import Dataset
from gemini.api.script_record import ScriptRecord
from gemini.db.models.scripts import ScriptModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import ExperimentScriptsViewModel

from datetime import date, datetime


class Script(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "script_id"))

    script_name: str
    script_url: Optional[str] = None
    script_extension: Optional[str] = None
    script_info: Optional[dict] = None


    @classmethod
    def create(
        cls,
        script_name: str,
        script_url: str,
        script_extension: str,
        script_info: dict = {},
        experiment_name: str = "Default"
    ):
        try:
            db_instance = ScriptModel.get_or_create(
                script_name=script_name,
                script_url=script_url,
                script_extension=script_extension,
                script_info=script_info,
            )
            script = cls.model_validate(db_instance)
            experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
            if experiment:
                experiment.scripts.append(script)
            return script
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, script_name: str, script_url: str) -> "Script":
        try:
            db_instance = ScriptModel.get_by_parameters(
                script_name=script_name,
                script_url=script_url,
            )
            script = cls.model_validate(db_instance)
            return script
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Script":
        try:
            db_instance = ScriptModel.get(id)
            script = cls.model_validate(db_instance)
            return script
        except Exception as e:
            raise e
        
    @classmethod
    def get_all(cls) -> List["Script"]:
        try:
            scripts = ScriptModel.all()
            scripts = [cls.model_validate(script) for script in scripts]
            return scripts if scripts else None
        except Exception as e:
            raise e
        

    @classmethod
    def search(cls, **search_parameters) -> List["Script"]:
        try:
            scripts = ExperimentScriptsViewModel.search(**search_parameters)
            scripts = [cls.model_validate(script) for script in scripts]
            return scripts if scripts else None
        except Exception as e:
            raise e
        

    def update(self, **update_parameters) -> "Script":
        try:
            current_id = self.id
            script = ScriptModel.get(current_id)
            script = ScriptModel.update(current_id, **update_parameters)
            script = self.model_validate(script)
            self.refresh()
            return script
        except Exception as e:
            raise e
        

    def delete(self) -> bool:
        try:
            current_id = self.id
            script = ScriptModel.get(current_id)
            ScriptModel.delete(script)
            return True
        except Exception as e:
            return False
        

    def refresh(self) -> "Script":
        try:
            db_instance = ScriptModel.get(self.id)
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
        record: ScriptRecord
    ) -> bool:
        try:
            if record.timestamp is None:
                record.timestamp = datetime.now()
            if record.collection_date is None:
                record.collection_date = record.timestamp.date()
            if record.dataset_name is None:
                record.dataset_name = self.dataset_name
            if record.script_name is None:
                record.script_name = self.script_name
            if record.record_info is None:
                record.record_info = {}

            record.script_id = self.id
            success = ScriptRecord.add([record])
            return success
        except Exception as e:
            return False
        

    def add_records(
        self,
        records: List[ScriptRecord]
    ) -> bool:
        try:
            for record in records:
                if record.timestamp is None:
                    record.timestamp = datetime.now()
                if record.collection_date is None:
                    record.collection_date = record.timestamp.date()
                if record.dataset_name is None:
                    record.dataset_name = self.dataset_name
                if record.script_name is None:
                    record.script_name = self.script_name
                if record.record_info is None:
                    record.record_info = {}

                record.script_id = self.id
            success = ScriptRecord.add(records)
            return success
        except Exception as e:
            return False
        

    def get_records(
            self,
            collection_date: date = None,
            experiment_name: str = None,
            season_name: str = None,
            site_name: str = None,
            plot_number: int = None,
            plot_row_number: int = None,
            plot_column_number: int = None,
            record_info: dict = None
    ) -> List[ScriptRecord]:
        try:
            record_info = record_info if record_info else {}
            record_info = {k: v for k, v in record_info.items() if v is not None}

            records = ScriptRecord.search(
                script_id=self.id,
                collection_date=collection_date,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                record_info=record_info
            )
            return records
        except Exception as e:
            raise e