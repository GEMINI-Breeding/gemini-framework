from typing import List, Optional, Any
from gemini.api.base import APIBase
from gemini.api.dataset import Dataset
from gemini.api.model_run import ModelRun
from gemini.api.model_record import ModelRecord
from gemini.models import ModelModel, DatasetModel, ExperimentModel
from gemini.models import ExperimentModelsViewModel
from gemini.logger import logger_service
from typing import List, Optional, Any

from uuid import UUID
from datetime import datetime, date
from rich.progress import track

class Model(APIBase):

    db_model = ModelModel

    model_name: str
    model_url: Optional[str] = None
    model_info: Optional[dict] = None

    datasets: Optional[List[Dataset]] = None
    model_runs: Optional[List[ModelRun]] = None

    @classmethod
    def create(
        cls,
        model_name: str ='Default',
        model_url: str = 'Default',
        model_info: dict = {},
        experiment_name: str = 'Default'
    ):
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        db_instance = ModelModel.get_or_create(
            model_name=model_name,
            model_url=model_url,
            model_info=model_info
        )
        if db_experiment and db_instance not in db_experiment.models:
            db_experiment.models.append(db_instance)
            db_experiment.save()
        instance = cls.model_validate(db_instance)
        logger_service.info(
            "API",
            f"Created a new instance of {cls.__name__} with id {instance.id}",
        )
        return instance
    
    @classmethod
    def get(cls, model_name: str) -> "Model":
        db_instance = ModelModel.get_by_parameters(model_name=model_name)
        logger_service.info("API", f"Retrieved model with name {model_name} from the database")
        return cls.model_validate(db_instance)
    
    @classmethod
    def get_by_experiment(cls, experiment_name: str) -> List["Model"]:
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        db_models = db_experiment.models
        logger_service.info("API", f"Retrieved models for experiment {experiment_name} from the database")
        return [cls.model_validate(db_model) for db_model in db_models]
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.model_name} from the database")
        return self.model_info
    
    def set_info(self, model_info: Optional[dict] = None) -> "Model":
        self.update(model_info=model_info)
        logger_service.info("API", f"Set information about {self.model_name} in the database")
        return self
    
    def add_info(self, model_info: Optional[dict] = None) -> "Model":
        current_info = self.get_info()
        updated_info = {**current_info, **model_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.model_name} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Model":
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.model_name} in the database")
        return self
    
    @classmethod
    def search(
        cls,
        experiment_name: str = None,
        **search_parameters: Any
    ) -> List["Model"]:
        models = ExperimentModelsViewModel.search(
            experiment_name=experiment_name,
            **search_parameters
        )
        logger_service.info("API", f"Retrieved {len(models)} models from the database")
        return [cls.model_validate(model) for model in models]
    
    
    def get_datasets(self) -> List[Dataset]:
        self.refresh()
        logger_service.info("API", f"Retrieved datasets for model {self.model_name} from the database")
        return self.datasets
    
    def get_model_runs(self) -> List[ModelRun]:
        self.refresh()
        logger_service.info("API", f"Retrieved model runs for model {self.model_name} from the database")
        return self.model_runs

    def add_record(
            self,
            model_data: dict,
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
            dataset_name = f"{self.model_name}_{collection_date}"

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

        record = ModelRecord.create(
            timestamp=timestamp,
            collection_date=collection_date,
            dataset_name=dataset_name,
            model_name=self.model_name,
            model_data=model_data,
            record_info=info
        )

        success = ModelRecord.add([record])
        logger_service.info("API", f"Added a record to {self.model_name} in the database")
        return success
    

    def add_records(
            self,
            model_data: List[dict],
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
            timestamps = [datetime.now() for _ in range(len(model_data))]

        if len(timestamps) != len(model_data):
            raise ValueError("Number of timestamps must match number of model data")
        
        collection_date = timestamps[0].date() if collection_date is None else collection_date

        if dataset_name is None:
            dataset_name = f"{self.model_name}_{collection_date}"

        db_model = ModelModel.get_by_parameters(model_name=self.model_name)
        db_dataset = DatasetModel.get_or_create(dataset_name=dataset_name)
        if db_dataset not in db_model.datasets:
            db_model.datasets.append(db_dataset)
            db_model.save()

        records = []

        for i in track(range(len(model_data)), description="Creating Records"):
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

            record = ModelRecord.create(
                model_name=self.model_name,
                dataset_name=dataset_name,
                timestamp=timestamps[i],
                collection_date=collection_date,
                model_data=model_data[i],
                record_info=info
            )

            records.append(record)

        success = ModelRecord.add(records)
        logger_service.info("API", f"Added {len(records)} records to {self.model_name} in the database")
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
    ) -> List[ModelRecord]:
        
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

        records = ModelRecord.search(
            model_name=self.model_name,
            collection_date=collection_date,
            record_info=record_info
        )

        return records