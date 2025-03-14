from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.script_run import ScriptRun
from gemini.api.script_record import ScriptRecord
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.db.models.scripts import ScriptModel
from gemini.db.models.script_runs import ScriptRunModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import ExperimentScriptsViewModel
from gemini.db.models.associations import ExperimentScriptModel, ScriptDatasetModel
from gemini.db.models.views.dataset_views import ScriptDatasetsViewModel
from datetime import date


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
        script_url: str = None,
        script_extension: str = None,
        script_info: dict = {},
        experiment_name: str = None
    ):
        try:
            db_instance = ScriptModel.get_or_create(
                script_name=script_name,
                script_url=script_url,
                script_extension=script_extension,
                script_info=script_info,
            )
            if experiment_name:
                db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
                if db_experiment:
                    ExperimentScriptModel.get_or_create(experiment_id=db_experiment.id, script_id=db_instance.id)

            script = cls.model_validate(db_instance)
            return script if script else None
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, script_name: str, experiment_name: str = None) -> "Script":
        try:
            db_instance = ExperimentScriptsViewModel.get_by_parameters(
                script_name=script_name,
                experiment_name=experiment_name
            )
            script = cls.model_validate(db_instance) if db_instance else None
            return script
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Script":
        try:
            db_instance = ScriptModel.get(id)
            script = cls.model_validate(db_instance) if db_instance else None
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
    def search(
        cls,
        experiment_name: str = None,
        script_name: str = None,
        script_info: dict = None,
        script_url: str = None,
        script_extension: str = None
    ) -> List["Script"]:
        try:
            if not any([experiment_name, script_name, script_info, script_url, script_extension]):
                raise Exception("At least one search parameter must be provided.")

            scripts = ExperimentScriptsViewModel.search(
                experiment_name=experiment_name,
                script_name=script_name,
                script_info=script_info,
                script_url=script_url,
                script_extension=script_extension
            )
            scripts = [cls.model_validate(script) for script in scripts]
            return scripts if scripts else None
        except Exception as e:
            raise e
        

    def update(
        self,
        script_name: str = None, 
        script_url : str = None,
        script_extension : str = None,
        script_info : dict = None
    ) -> "Script":
        try:    
            if not any([script_url, script_extension, script_info, script_name]):                           
                raise Exception("At least one update parameter must be provided.")

            current_id = self.id
            script = ScriptModel.get(current_id)
            script = ScriptModel.update(
                script,
                script_name=script_name,
                script_url=script_url,
                script_extension=script_extension,
                script_info=script_info
            )
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
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e
        
    def get_datasets(self) -> List["Dataset"]:
        try:
            script = ScriptModel.get(self.id)
            datasets = ScriptDatasetsViewModel.search(script_id=script.id)
            datasets = [Dataset.model_validate(dataset) for dataset in datasets]
            return datasets if datasets else None
        except Exception as e:
            raise e

    def create_dataset(
        self,
        dataset_name: str,
        dataset_info: dict = {},
        collection_date: date = None,
        experiment_name: str = None
    ) -> Dataset:
        try:
            dataset = Dataset.create(
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                collection_date=collection_date,
                experiment_name=experiment_name,
                dataset_type=GEMINIDatasetType.Procedure
            )
            ScriptDatasetModel.get_or_create(script_id=self.id, dataset_id=dataset.id)
            return dataset
        except Exception as e:
            raise e
        

    
    def get_runs(self) -> List[ScriptRun]:
        try:
            script = ScriptModel.get(self.id)
            script_runs = ScriptRunModel.search(script_id=script.id)
            script_runs = [ScriptRun.model_validate(script_run) for script_run in script_runs]
            return script_runs if script_runs else None
        except Exception as e:
            raise e
        

    def create_run(
        self,
        script_run_info: dict = None
    ) -> ScriptRun:
        try:
            run = ScriptRun.create(
                script_run_info=script_run_info,
                script_name=self.script_name
            )
            return run
        except Exception as e:
            raise e
                
    def add_record(
        self,
        record: ScriptRecord
    ) -> bool:
        try:
            record.script_id = self.id
            record.script_name = self.script_name
            record.dataset_name = f"{self.script_name} Dataset"
            record.timestamp = record.timestamp if record.timestamp else date.today()

            success = ScriptRecord.add([record])
            return success
        except Exception as e:
            raise e
        
    def add_records(
        self,
        records: List[ScriptRecord]
    ) -> bool:
        try:
            for record in records:
                record.script_id = self.id
                record.script_name = self.script_name
                record.dataset_name = f"{self.script_name} Dataset"
                record.timestamp = record.timestamp if record.timestamp else date.today()

            success = ScriptRecord.add(records)
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
    ) -> List[ScriptRecord]:
        try:
            record_info = record_info if record_info else {}
            record_info = {k: v for k, v in record_info.items() if v is not None}

            records = ScriptRecord.search(
                script_name=self.script_name,
                collection_date=collection_date,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                record_info=record_info
            )
            return records
        except Exception as e:
            raise e
        
