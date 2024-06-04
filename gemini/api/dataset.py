from typing import Optional, List, Any
from gemini.api.base import APIBase
from gemini.api.enums import GEMINIDatasetType
from gemini.api.dataset_type import DatasetType
from gemini.api.dataset_record import DatasetRecord
from gemini.models import DatasetModel, ExperimentModel, DatasetTypeModel
from gemini.logger import logger_service
from gemini.object_store import storage_service

from datetime import datetime, date
from rich.progress import track


class Dataset(APIBase):

    db_model = DatasetModel

    dataset_name: str
    dataset_info: Optional[dict] = None
    is_derived: Optional[bool] = False
    collection_date: Optional[date] = None

    dataset_type: Optional[DatasetType] = None


    @classmethod
    def create(
        cls,
        dataset_name: str,
        dataset_info: dict = None,
        is_derived: bool = False,
        collection_date: date = None,
        dataset_type: GEMINIDatasetType = GEMINIDatasetType.Default,
        experiment_name: str = None
    ):
        
        db_dataset_type = DatasetTypeModel.get_by_id(dataset_type.value)
        new_instance = cls.db_model.get_or_create(
            dataset_name=dataset_name,
            dataset_info=dataset_info,
            is_derived=is_derived,
            collection_date=collection_date,
            dataset_type=db_dataset_type
        )

        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        if db_experiment and new_instance not in db_experiment.datasets:
            db_experiment.datasets.append(new_instance)
            db_experiment.save()

        logger_service.info(
            "API",
            f"Created a new dataset with name {new_instance.dataset_name} in the database",
        )
        new_instance = cls.model_validate(new_instance)
        return new_instance
    
    @classmethod
    def get(cls, dataset_name: str) -> "Dataset":
        db_instance = cls.db_model.get_by_parameters(dataset_name=dataset_name)
        logger_service.info("API", f"Retrieved dataset with name {dataset_name} from the database")
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.dataset_name} from the database")
        return self.dataset_info
    
    def set_info(self, dataset_info: Optional[dict] = None) -> "Dataset":
        self.update(dataset_info=dataset_info)
        logger_service.info("API", f"Set information about {self.dataset_name} in the database")
        return self
    
    def add_info(self, dataset_info: dict) -> "Dataset":
        current_info = self.get_info()
        updated_info = {**current_info, **dataset_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information about {self.dataset_name} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "Dataset":
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(current_info)
        logger_service.info("API", f"Removed information from {self.dataset_name} in the database")
        return self
    
    # Todo: Add Records and Search Records methods
    def add_record(
            self,
            dataset_data: dict,
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
            dataset_name = self.dataset_name

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

        record = DatasetRecord.create(
            dataset_name=self.dataset_name,
            timestamp=timestamp,
            collection_date=collection_date,
            dataset_data=dataset_data,
            record_info=info
        )

        success = DatasetRecord.add([record])
        logger_service.info("API", f"Added a record to {self.dataset_name} in the database")
        return success
    

    def add_records(
            self,
            dataset_data: List[dict],
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
            timestamps = [datetime.now() for _ in range(len(dataset_data))]

        if len(dataset_data) != len(timestamps):
            raise ValueError("The number of timestamps must match the number of records")
        
        collection_date = timestamps[0].date() if collection_date is None else collection_date

        if dataset_name is None:
            dataset_name = self.dataset_name

        db_dataset = DatasetModel.get_or_create(dataset_name=dataset_name)
        
        records = []

        for i in track(range(len(dataset_data)), description="Creating Records"):
            info = {
                "experiment_name": experiment_name if experiment_name else None,
                "season_name": season_name if season_name else None,
                "site_name": site_name if site_name else None,
                "plot_number": plot_numbers[i] if plot_numbers else None,
                "plot_row_number": plot_row_numbers[i] if plot_row_numbers else None,
                "plot_column_number": plot_column_numbers[i] if plot_column_numbers else None
            }

            if record_info and record_info[i]:
                info.update(record_info[i])

            record = DatasetRecord.create(
                dataset_name=self.dataset_name,
                timestamp=timestamps[i],
                collection_date=collection_date,
                dataset_data=dataset_data[i],
                record_info=info
            )

            records.append(record)

        success = DatasetRecord.add(records)
        logger_service.info("API", f"Added {len(records)} records to {self.dataset_name} in the database")
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
    ) -> List[DatasetRecord]:
        
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

        records = DatasetRecord.search(
            dataset_name=self.dataset_name,
            collection_date=collection_date,
            record_info=record_info
        )
        return records
