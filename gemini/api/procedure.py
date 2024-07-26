from typing import List, Optional, Any
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, ID
from gemini.api.dataset import Dataset
from gemini.api.procedure_run import ProcedureRun
from gemini.api.procedure_record import ProcedureRecord
from gemini.logger import logger_service
from gemini.models import ProcedureModel, DatasetModel, ExperimentModel
from gemini.models import ExperimentProceduresViewModel

from uuid import UUID
from datetime import datetime, date
from rich.progress import track


class Procedure(APIBase):
    
    db_model = ProcedureModel

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "procedure_id"))
    procedure_name: str
    procedure_info: Optional[dict] = None

    datasets: Optional[List[Dataset]] = None
    procedure_runs: Optional[List[ProcedureRun]] = None

    @classmethod
    def create(
        cls,
        procedure_name: str ='Default',
        procedure_info: dict = {}, 
        experiment_name: str = 'Default'
    ):
        db_instance = ProcedureModel.get_or_create(
            procedure_name=procedure_name,
            procedure_info=procedure_info
        )
        
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        if db_experiment and db_instance not in db_experiment.procedures:
            db_experiment.procedures.append(db_instance)
            db_experiment.save()
        
        
        instance = cls.model_validate(db_instance)
        
        logger_service.info(
            "API",
            f"Created a new instance of {cls.__name__} with id {instance.id}",
        )
    
        return instance
    
    @classmethod
    def get(cls, procedure_name: str) -> "Procedure":
        db_instance = ProcedureModel.get_by_parameters(procedure_name=procedure_name)
        logger_service.info("API", f"Retrieved procedure with name {procedure_name} from the database")
        return cls.model_validate(db_instance)
    
    @classmethod
    def get_by_experiment(cls, experiment_name: str) -> List["Procedure"]:
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        db_procedures = db_experiment.procedures
        logger_service.info("API", f"Retrieved procedures for experiment {experiment_name} from the database")
        return [cls.model_validate(db_procedure) for db_procedure in db_procedures]
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.procedure_name} from the database")
        return self.procedure_info
    
    def set_info(self, procedure_info: Optional[dict] = None) -> "Procedure":
        self.update(procedure_info=procedure_info)
        logger_service.info("API", f"Set information about {self.procedure_name} in the database")
        return self
    
    def add_info(self, procedure_info: Optional[dict] = None) -> "Procedure":
        current_info = self.get_info()
        updated_info = {**current_info, **procedure_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.procedure_name} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Procedure":
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove} 
        self.update(procedure_info=current_info)
        logger_service.info("API", f"Removed information from {self.procedure_name} in the database")
        return self
    
    @classmethod
    def search(
        cls,
        experiment_name: str = None,
        **search_parameters: Any
    ) -> List["Procedure"]:
        procedures = ExperimentProceduresViewModel.search(
            experiment_name=experiment_name,
            **search_parameters
        )
        procedures = [cls.model_validate(procedure) for procedure in procedures]
        logger_service.info("API", f"Retrieved {len(procedures)} procedures from the database")
        return procedures if procedures else None
    
    def get_datasets(self) -> List[Dataset]:
        self.refresh()
        logger_service.info("API", f"Retrieved datasets for {self.procedure_name} from the database")
        return self.datasets
    
    def get_procedure_runs(self) -> List[ProcedureRun]:
        self.refresh()
        logger_service.info("API", f"Retrieved procedure runs for {self.procedure_name} from the database")
        return self.procedure_runs

    
    # Todo: Add, remove, and get datasets from a procedure
    # Todo: Add, remove, and get procedure runs from a procedure
    # Todo: Add, remove, and get records from a procedure

    def add_record(
        self,
        procedure_data: dict,
        timestamp: datetime = None,
        collection_date: date = None,
        dataset_name: str = 'Default',
        experiment_name: str = 'Default',
        season_name: str = '2023',
        site_name: str = 'Default',
        plot_number: int = -1,
        plot_row_number: int = -1,
        plot_column_number: int = -1,
        record_info: dict = {}
    ) -> bool:
        
        if timestamp is None:
            timestamp = datetime.now()

        collection_date = timestamp.date() if collection_date is None else collection_date

        if dataset_name is None:
            dataset_name = f"{self.procedure_name}_{collection_date}"

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

        record  = ProcedureRecord.create(
            procedure_name=self.procedure_name,
            timestamp=timestamp,
            collection_date=collection_date,
            dataset_name=dataset_name,
            procedure_data=procedure_data,
            record_info=info
        )

        success = ProcedureRecord.add([record])
        logger_service.info("API", f"Added a record to {self.procedure_name} in the database")
        return success
    
    def add_records(
        self,
        procedure_data: List[dict],
        timestamps: List[datetime] = None,
        collection_date: date = None,
        dataset_name: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_numbers: List[int] = None,
        plot_row_numbers: List[int] = None,
        plot_column_numbers: List[int] = None,
        record_info: List[dict] = None
    ) -> bool:
        
        if timestamps is None:
            timestamps = [datetime.now() for _ in range(len(procedure_data))]

        if len(procedure_data) != len(timestamps):
            raise ValueError("The number of timestamps must match the number of sensor data records")
        
        collection_date = timestamps[0].date() if collection_date is None else collection_date

        if dataset_name is None:
            dataset_name = f"{self.procedure_name}_{collection_date}"

        db_procedure = ProcedureModel.get_by_parameters(procedure_name=self.procedure_name)
        db_dataset = DatasetModel.get_or_create(dataset_name=dataset_name)
        if db_dataset not in db_procedure.datasets:
            db_procedure.datasets.append(db_dataset)
            db_procedure.save()

        records = []

        for i in track(range(len(procedure_data)), description="Creating Records"):
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

            record = ProcedureRecord.create(
                procedure_name=self.procedure_name,
                timestamp=timestamps[i],
                collection_date=collection_date,
                dataset_name=dataset_name,
                procedure_data=procedure_data[i],
                record_info=info
            )

            records.append(record)

        success = ProcedureRecord.add(records)
        logger_service.info("API", f"Added {len(records)} records to {self.procedure_name} in the database")
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
    ) -> List[ProcedureRecord]:
        
        record_info = record_info if record_info else {}
        record_info.update({
            "experiment_name": experiment_name,
            "season_name": season_name,
            "site_name": site_name,
            "plot_number": plot_number,
            "plot_row_number": plot_row_number,
            "plot_column_number": plot_column_number
        })
        
        record_info = {key: value for key, value in record_info.items() if value is not None}
        
        records = ProcedureRecord.search(
            procedure_name=self.procedure_name,
            collection_date=collection_date,
            record_info=record_info
        )
        
        return records
        
