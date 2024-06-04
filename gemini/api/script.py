from typing import Optional, List, Any
from gemini.api.base import APIBase
from gemini.api.script_run import ScriptRun
from gemini.api.script_record import ScriptRecord
from gemini.api.dataset import Dataset
from gemini.models import ScriptModel, ScriptRunModel, DatasetModel, ExperimentModel

from gemini.logger import logger_service

from uuid import UUID
from datetime import date, datetime
from rich.progress import track


class Script(APIBase):

    db_model = ScriptModel

    script_name: str
    script_url: Optional[str] = None
    script_extension: Optional[str] = None
    script_info: Optional[dict] = None

    datasets: Optional[List[Dataset]] = None
    script_runs: Optional[List[ScriptRun]] = None

    @classmethod
    def create(
        cls,
        script_name: str,
        script_url: str = None,
        script_extension: str = None,
        script_info: dict = None,
        experiment_name: str = None
    ):
        new_instance = cls.db_model.get_or_create(
            script_name=script_name,
            script_url=script_url,
            script_extension=script_extension,
            script_info=script_info,
        )
        logger_service.info(
            "API",
            f"Created a new script with name {new_instance.script_name} in the database",
        )
        
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        if db_experiment and new_instance not in db_experiment.scripts:
            db_experiment.scripts.append(new_instance)
            db_experiment.save()
        
        new_instance = cls.model_validate(new_instance)
        return new_instance
    
    @classmethod
    def get(cls, script_name: str) -> "Script":
        script = cls.db_model.get_by_name(script_name)
        script = cls.model_validate(script)
        logger_service.info(
            "API",
            f"Retrieved script with name {script_name} from the database",
        )
        return script
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved information about {self.script_name} from the database",
        )
        return self.script_info
    
    def set_info(self, script_info: Optional[dict] = None) -> "Script":
        self.update(script_info=script_info)
        logger_service.info(
            "API",
            f"Updated information about {self.script_name} in the database",
        )
        return self
    
    def add_info(self, script_info: Optional[dict] = None) -> "Script":
        current_info = self.get_info()
        updated_info = {**current_info, **script_info}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Added information to {self.script_name} in the database",
        )
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Script":
        current_info = self.get_info()
        for key in keys_to_remove:
            current_info.pop(key, None)
        self.set_info(current_info)
        logger_service.info(
            "API",
            f"Removed information from {self.script_name} in the database",
        )
        return self
    
    def get_datasets(self) -> List[Dataset]:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved datasets for {self.script_name} from the database",
        )
        return self.datasets
    
    def get_script_runs(self) -> List[ScriptRun]:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved script runs for {self.script_name} from the database",
        )
        return self.script_runs
    
    # Todo: Adding, removing, searching data generated by a script
    # Todo: Add and remove datasets
    # Todo: Add and remove script runs
    
    def add_record(
        self,
        script_data: dict,
        timestamp: datetime = None,
        collection_date: date = None,
        dataset_name: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        record_info: dict = None
    ) -> bool:
        
        if timestamp is None:
            timestamp = datetime.now()
            
        collection_date = timestamp.date() if collection_date is None else collection_date
        
        if dataset_name is None:
            dataset_name = f"{self.script_name}_{collection_date}"
            
        db_script = ScriptModel.get_by_parameters(script_name=self.script_name)
        db_dataset = DatasetModel.get_or_create(dataset_name=dataset_name)
        if db_dataset and db_dataset not in db_script.datasets:
            db_script.datasets.append(db_dataset)
            db_script.save()
            
        info = {
            "experiment_name": experiment_name,
            "season_name": season_name,
            "site_name": site_name,
            "plot_number": plot_number,
            "plot_row_number": plot_row_number,
            "plot_column_number": plot_column_number
        }
        
        if record_info:
            info.update(record_info)
            
        record = ScriptRecord.create(
            script_name=self.script_name,
            timestamp=timestamp,
            collection_date=collection_date,
            dataset_name=dataset_name,
            script_data=script_data,
            record_info=info
        )
        
        success = ScriptRecord.add([record])
        logger_service.info(
            "API",
            f"Added a record to {self.script_name} in the database",
        )
        
        return success
    
    
    def add_records(
        self,
        script_data: List[dict],
        timestamps: List[datetime] = None,
        collection_date : date = None,
        dataset_name: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_numbers: List[int] = None,
        plot_column_numbers: List[int] = None,
        plot_row_numbers: List[int] = None,
        record_info: List[dict] = None
    ) -> bool:
        
        if timestamps is None:
            timestamps = [datetime.now() for _ in range(len(script_data))]
            
        if len(timestamps) != len(script_data):
            raise ValueError("The number of timestamps must match the number of records")
        
        collection_date = timestamps[0].date() if collection_date is None else collection_date
        
        if dataset_name is None:
            dataset_name = f"{self.script_name}_{collection_date}"
            
        db_script = ScriptModel.get_by_parameters(script_name=self.script_name)
        db_dataset = DatasetModel.get_or_create(dataset_name=dataset_name)
        if db_dataset and db_dataset not in db_script.datasets:
            db_script.datasets.append(db_dataset)
            db_script.save()
            
        records = []
        
        for i in track(range(len(script_data)), description="Adding Script Records"):
            info = {
                "experiment_name": experiment_name,
                "season_name": season_name,
                "site_name": site_name,
                "plot_number": plot_numbers[i] if plot_numbers else None,
                "plot_row_number": plot_row_numbers[i] if plot_row_numbers else None,
                "plot_column_number": plot_column_numbers[i] if plot_column_numbers else None
            }
            
            if record_info and record_info[i]:
                info.update(record_info[i])
            
            record = ScriptRecord.create(
                script_name=self.script_name,
                timestamp=timestamps[i],
                collection_date=collection_date,
                dataset_name=dataset_name,
                script_data=script_data[i],
                record_info=info
            )
            
            records.append(record)
         
        success = ScriptRecord.add(records)
        logger_service.info(
            "API",
            f"Added records to {self.script_name} in the database",
        )
        
        return success
  
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
        
        record_info = record_info or {}
        record_info.update({
            "experiment_name": experiment_name,
            "season_name": season_name,
            "site_name": site_name,
            "plot_number": plot_number,
            "plot_row_number": plot_row_number,
            "plot_column_number": plot_column_number
        })
        
        record_info = {key: value for key, value in record_info.items() if value is not None}
        
        records = ScriptRecord.search(
            collection_date=collection_date,
            script_name=self.script_name,
            record_info=record_info
        )
        
        logger_service.info(
            "API",
            f"Retrieved records for {self.script_name} from the database",
        )
        
        return records
