from typing import Any, Optional, List
from gemini.api.base import APIBase, ID
from gemini.api.trait_level import TraitLevel
from gemini.api.trait_record import TraitRecord
from gemini.api.dataset import Dataset
from gemini.api.enums import GEMINITraitLevel
from gemini.models import TraitModel, ExperimentModel, TraitLevelModel, DatasetModel
from gemini.models import ExperimentTraitsViewModel
from gemini.logger import logger_service

from datetime import datetime, date
from rich.progress import track


class Trait(APIBase):

    db_model = TraitModel

    trait_name: str
    trait_units: Optional[str] = None
    trait_level_id: Optional[int] = None
    trait_metrics: Optional[dict] = None

    trait_level: Optional[TraitLevel] = None
    datasets: Optional[List[Dataset]] = None


    @classmethod
    def create(
        cls,
        trait_name: str = 'Default',
        trait_units: str = 'Default',
        trait_level: GEMINITraitLevel = GEMINITraitLevel.Default,
        trait_metrics: dict = {},
        trait_info: dict = {},
        experiment_name: str = 'Default'
    ):
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        db_trait_level = TraitLevelModel.get_by_parameters(trait_level_name=trait_level.name)
        db_instance = cls.db_model.get_or_create(
            trait_name=trait_name,
            trait_units=trait_units,
            trait_level_id=db_trait_level.id,
            trait_metrics=trait_metrics,
            trait_info=trait_info
        )

        if db_experiment and db_instance not in db_experiment.traits:
            db_experiment.traits.append(db_instance)
            db_experiment.save()

        instance = cls.model_validate(db_instance)
        logger_service.info(
            "API",
            f"Created a new trait with name {instance.trait_name} in the database",
        )
        return instance
    
    @classmethod
    def get_by_level(cls, trait_level: GEMINITraitLevel) -> List["Trait"]:
        db_trait_level = TraitLevelModel.get_by_parameters(trait_level_name=trait_level.name)
        db_traits = cls.db_model.search(trait_level_id=db_trait_level.id)
        traits = [cls.model_validate(trait) for trait in db_traits]
        logger_service.info(
            "API",
            f"Retrieved traits of level {trait_level.name} from the database",
        )
        return traits
    
    @classmethod
    def get(cls, trait_name: str) -> "Trait":
        db_instance = cls.db_model.get_by_parameters(trait_name=trait_name)
        logger_service.info(
            "API",
            f"Retrieved trait with name {trait_name} from the database",
        )
        return cls.model_validate(db_instance) if db_instance else None
    
    @classmethod
    def get_by_experiment(cls, experiment_name: str) -> List["Trait"]:
        db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
        db_traits = db_experiment.traits
        traits = [cls.model_validate(db_trait) for db_trait in db_traits]
        logger_service.info(
            "API",
            f"Retrieved traits for experiment {experiment_name} from the database",
        )
        return traits
    
    @classmethod
    def search(
        cls,
        experiment_name: str = None,
        **search_parameters : Any
    ) -> List["Trait"]:
        traits = ExperimentTraitsViewModel.search(
            experiment_name=experiment_name,
            **search_parameters
        )
        traits = [cls.model_validate(trait) for trait in traits]
        logger_service.info(
            "API",
            f"Retrieved traits for experiment {experiment_name} from the database",
        )
        return traits

    
    def get_level(self) -> TraitLevel:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved level of {self.trait_name} from the database",
        )
        return self.trait_level
    
    def set_level(self, trait_level: GEMINITraitLevel) -> "Trait":
        db_trait_level = TraitLevelModel.get_by_parameters(trait_level_name=trait_level.name)
        self.update(trait_level_id=db_trait_level.id)
        logger_service.info(
            "API",
            f"Set level of {self.trait_name} in the database",
        )
        return self
    
    def get_datasets(self) -> List[Dataset]:
        self.refresh()
        logger_service.info(
            "API",
            f"Retrieved datasets of {self.trait_name} from the database",
        )
        return self.datasets
    
    # Todo: Data Handling
    # Todo: Add records, get records, etc.
    # Todo: Add datasets, get datasets, etc.
    def add_record(
            self,
            trait_value: Any,
            timestamp: datetime = None,
            collection_date: date = None,
            dataset_name: str = None,
            experiment_name: str = None,
            season_name: str = None,
            site_name: str = None,
            sensor_name: str = None,
            plot_number: int = None,
            plot_row_number: int = None,
            plot_column_number: int = None,
            record_info: dict = None
    ) -> TraitRecord:
        
        if timestamp is None:
            timestamp = datetime.now()

        collection_date = timestamp.date() if collection_date is None else collection_date

        if dataset_name is None:
            dataset_name = f"{self.trait_name}_{collection_date}"

        info = {
            "experiment_name": experiment_name,
            "season_name": season_name,
            "site_name": site_name,
            "sensor_name": sensor_name,
            "plot_number": plot_number,
            "plot_row_number": plot_row_number,
            "plot_column_number": plot_column_number
        }

        if record_info:
            info.update(record_info)

        record = TraitRecord.create(
            trait_name=self.trait_name,
            trait_value=trait_value,
            timestamp=timestamp,
            collection_date=collection_date,
            dataset_name=dataset_name,
            record_info=info
        )

        record_id = TraitRecord.add([record])
        if len(record_id) == 0 or not record_id:
            logger_service.error("API", "Failed to add record to the database")
            return None
        
        return TraitRecord.get(record_id[0])


    
    def add_records(
            self,
            trait_values: List[Any],
            timestamps: List[datetime] = None,
            collection_dates: date = None,
            dataset_name: str = None,
            experiment_name: str = None,
            season_name: str = None,
            site_name: str = None,
            sensor_name: str = None,
            plot_numbers: List[int] = None,
            plot_row_numbers: List[int] = None,
            plot_column_numbers: List[int] = None,
            record_info: List[dict] = None,
            stream_results: bool = False
    ) -> List[TraitRecord]:
        
        if timestamps is None:
            timestamps = [datetime.now() for _ in range(len(trait_values))]
        
        if len(trait_values) != len(timestamps):
            raise ValueError("The number of timestamps and trait values do not match")
        
        collection_date = timestamps[0].date() if collection_dates is None else collection_dates

        if dataset_name is None:
            dataset_name = f"{self.trait_name}_{collection_date}"

        db_trait = TraitModel.get_by_parameters(trait_name=self.trait_name)
    
        db_dataset = DatasetModel.get_or_create(dataset_name=dataset_name)
        if db_dataset not in db_trait.datasets:
            db_trait.datasets.append(db_dataset)
            db_trait.save()

        records = []
        
        for i in track(range(len(trait_values)), description="Adding Records"):
            info = {
                "experiment_name": experiment_name,
                "season_name": season_name,
                "site_name": site_name,
                "sensor_name": sensor_name,
                "plot_number": plot_numbers[i] if plot_numbers else None,
                "plot_row_number": plot_row_numbers[i] if plot_row_numbers else None,
                "plot_column_number": plot_column_numbers[i] if plot_column_numbers else None
            }

            if record_info and record_info[i]:
                info.update(record_info[i])

            record = TraitRecord.create(
                trait_name=self.trait_name,
                trait_value=trait_values[i],
                timestamp=timestamps[i],
                collection_date=collection_date,
                dataset_name=dataset_name,
                record_info=info
            )
            records.append(record)

        logger_service.info(
            "API",
            f"Adding records to {self.trait_name} in the database",
        )
        records = TraitRecord.add(records)
        if stream_results:
            return records
        return list(records)
    
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
    ) -> List[TraitRecord]:

        record_info = record_info if record_info else {}
        record_info.update({
            "experiment_name": experiment_name,
            "season_name": season_name,
            "site_name": site_name,
            "plot_number": plot_number,
            "plot_row_number": plot_row_number,
            "plot_column_number": plot_column_number
        })

        # Remove None values
        record_info = {k: v for k, v in record_info.items() if v is not None}

        records = TraitRecord.search(
            trait_name=self.trait_name,
            collection_date=collection_date,
            record_info=record_info
        )

        logger_service.info(
            "API",
            f"Retrieved records of {self.trait_name} from the database",
        )

        return records
        

         