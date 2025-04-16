from typing import Optional, List
from uuid import UUID
from tqdm import tqdm

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.dataset import Dataset
from gemini.api.trait_record import TraitRecord
from gemini.api.enums import GEMINITraitLevel, GEMINIDatasetType
from gemini.db.models.traits import TraitModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import ExperimentTraitsViewModel
from gemini.db.models.views.dataset_views import TraitDatasetsViewModel
from gemini.db.models.associations import ExperimentTraitModel, TraitDatasetModel
from datetime import date, datetime

class Trait(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "trait_id"))

    trait_name: str
    trait_units: str
    trait_level_id: Optional[int] = None
    trait_info: Optional[dict] = None
    trait_metrics: Optional[dict] = None

    @classmethod
    def exists(
        cls,
        trait_name: str
    ) -> bool:
        try:
            exists = TraitModel.exists(trait_name=trait_name)
            return exists
        except Exception as e:
            raise e
        
    def get_info(self) -> dict:
        try:
            current_id = self.id
            trait = TraitModel.get(current_id)
            trait_info = trait.trait_info
            if not trait_info:
                raise Exception("Trait info is empty.")
            return trait_info
        except Exception as e:
            raise e
        
    def set_info(self, trait_info: dict) -> "Trait":
        try:
            current_id = self.id
            trait = TraitModel.get(current_id)
            trait = TraitModel.update(
                trait,
                trait_info=trait_info
            )
            trait = self.model_validate(trait)
            self.refresh()
            return self
        except Exception as e:
            raise e

    @classmethod
    def create(
        cls,
        trait_name: str,
        trait_units: str = None,
        trait_level: GEMINITraitLevel = GEMINITraitLevel.Plot,
        trait_info: dict = {},
        trait_metrics: dict = {},
        experiment_name: str = None
    ) -> "Trait":
        try:
            trait_level_id = trait_level.value
            trait = TraitModel.get_or_create(
                trait_name=trait_name,
                trait_units=trait_units,
                trait_level_id=trait_level_id,
                trait_metrics=trait_metrics,
                trait_info=trait_info,
            )

            if experiment_name:
                db_experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
                if db_experiment:
                    ExperimentTraitModel.get_or_create(experiment_id=db_experiment.id, trait_id=trait.id)

            trait = cls.model_validate(trait)
            return trait
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, trait_name: str, experiment_name: str = None) -> "Trait":
        try:
            trait = TraitModel.get_by_parameters(
                trait_name=trait_name,
                experiment_name=experiment_name   
            )
            trait = cls.model_validate(trait)
            return trait if trait else None
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Trait":
        try:
            trait = TraitModel.get(id)
            trait = cls.model_validate(trait)
            return trait if trait else None
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["Trait"]:
        try:
            traits = TraitModel.all()
            traits = [cls.model_validate(trait) for trait in traits]
            return traits if traits else None
        except Exception as e:
            raise e
        

    @classmethod
    def search(
        cls, 
        experiment_name: str = None,
        trait_name: str = None,
        trait_units: str = None,
        trait_level: GEMINITraitLevel = None,
        trait_info: dict = None,
        trait_metrics: dict = None
    ) -> List["Trait"]:
        try:
            if not any([experiment_name, trait_name, trait_units, trait_level, trait_info, trait_metrics]):
                raise Exception("At least one search parameter must be provided.")
            
            traits = ExperimentTraitsViewModel.search(
                experiment_name=experiment_name,
                trait_name=trait_name,
                trait_units=trait_units,
                trait_level_id=trait_level.value if trait_level else None,
                trait_info=trait_info,
                trait_metrics=trait_metrics
            )
            traits = [cls.model_validate(trait) for trait in traits]
            return traits if traits else None
        except Exception as e:
            raise e
        

    def update(
            self,
            trait_name: str = None, 
            trait_units: str = None,
            trait_level: GEMINITraitLevel = None,
            trait_info: dict = None,
            trait_metrics: dict = None,
        ) -> "Trait":
        try:
            if not any([trait_units, trait_level, trait_info, trait_metrics, trait_name]):
                raise Exception("At least one update parameter must be provided.")

            current_id = self.id
            trait = TraitModel.get(current_id)
            trait = TraitModel.update(
                trait,
                trait_name=trait_name,
                trait_units=trait_units,
                trait_level_id=trait_level.value if trait_level else None,
                trait_info=trait_info,
                trait_metrics=trait_metrics
            )
            trait = self.model_validate(trait)
            self.refresh()
            return trait 
        except Exception as e:
            raise e
        

    def delete(self) -> bool:
        try:
            current_id = self.id
            trait = TraitModel.get(current_id)
            TraitModel.delete(trait)
            return True
        except Exception as e:
            return False
        

        
    def refresh(self) -> "Trait":
        try:
            db_instance = TraitModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e
        
    def get_datasets(self) -> List[Dataset]:
        try:
            trait = TraitModel.get(self.id)
            datasets = TraitDatasetsViewModel.search(trait_id=trait.id)
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
                dataset_type=GEMINIDatasetType.Trait,
                collection_date=collection_date,
                experiment_name=experiment_name
            )
            TraitDatasetModel.get_or_create(trait_id=self.id, dataset_id=dataset.id)
            return dataset
        except Exception as e:
            raise e
        
    def has_dataset(self, dataset_name: str) -> bool:
        try:
            exists = TraitDatasetsViewModel.exists(
                trait_id=self.id,
                dataset_name=dataset_name
            )
            return exists
        except Exception as e:
            raise e
        
    def assign_experiment():
        pass

    def belongs_to_experiment():
        pass

    def unassign_experiment():
        pass

    def get_experiments(self):
        try:
            from gemini.api.experiment import Experiment
            db_instance = TraitModel.get(self.id)
            experiments = ExperimentTraitsViewModel.search(trait_id=db_instance.id)
            experiments = [Experiment.model_validate(experiment) for experiment in experiments]
            return experiments if experiments else None
        except Exception as e:
            raise e


    def add_record(
        self,
        timestamp: date = None,
        collection_date: date = None,
        dataset_name: str = None,
        trait_value: float = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_number: int = -1,
        plot_row_number: int = -1,
        plot_column_number: int = -1,
        record_info: dict = {}
    ) -> tuple[bool, List[str]]:
        try:
            if not experiment_name or not season_name or not site_name:
                raise ValueError("Experiment name, season name, and site name must be provided.")
            
            timestamp = timestamp if timestamp else datetime.now()
            collection_date = collection_date if collection_date else timestamp.date()
            trait_name = self.trait_name
            trait_id = self.id

            if not dataset_name:
                dataset_name = trait_name.lower().replace(" ", "_")
                dataset_name = dataset_name + f"_{collection_date}"
                dataset_name = dataset_name + f"_{experiment_name}_{season_name}_{site_name}"


            trait_record = TraitRecord(
                trait_id=trait_id,
                trait_name=trait_name,
                trait_value=trait_value,
                dataset_name=dataset_name,
                timestamp=timestamp,
                collection_date=collection_date,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                record_info=record_info
            )

            success, inserted_record_ids = TraitRecord.add([trait_record])
            return success, inserted_record_ids
        except Exception as e:
            return False, []
        
    def add_records(
        self,
        timestamps: List[datetime] = None,
        collection_date: date = None,
        trait_values: List[float] = [],
        dataset_name: str = None,
        experiment_name: str = None,
        season_name: str = None,
        site_name: str = None,
        plot_numbers: List[int] = None,
        plot_row_numbers: List[int] = None,
        plot_column_numbers: List[int] = None,
        record_info: List[dict] = []
    ) -> tuple[bool, List[str]]:
        try:
            if not experiment_name or not season_name or not site_name:
                raise ValueError("Experiment name, season name, and site name must be provided.")
            
            if len(timestamps) == 0:
                raise ValueError("At least one timestamp must be provided.")
            
            if not dataset_name:
                dataset_name = self.trait_name.lower().replace(" ", "_")
                dataset_name = dataset_name + f"_{collection_date}"
                dataset_name = dataset_name + f"_{experiment_name}_{season_name}_{site_name}"

            collection_date = collection_date if collection_date else timestamps[0].date()
            trait_records = []
            timestamps_length = len(timestamps)

            for i in tqdm(range(timestamps_length), desc="Adding Records for Trait: " + self.trait_name):
                trait_record = TraitRecord(
                    trait_id=self.id,
                    trait_name=self.trait_name,
                    trait_value=trait_values[i],
                    dataset_name=dataset_name if dataset_name else f"{self.trait_name} Dataset",
                    timestamp=timestamps[i],
                    collection_date=collection_date,
                    experiment_name=experiment_name,
                    season_name=season_name,
                    site_name=site_name,
                    plot_number=plot_numbers[i] if plot_numbers else None,
                    plot_row_number=plot_row_numbers[i] if plot_row_numbers else None,
                    plot_column_number=plot_column_numbers[i] if plot_column_numbers else None,
                    record_info=record_info[i] if record_info else {}
                )
                trait_records.append(trait_record)

            success, inserted_record_ids = TraitRecord.add(trait_records)
            return success, inserted_record_ids
        except Exception as e:
            return False, []
        
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
        try:
            record_info = record_info if record_info else {}
            record_info = {k: v for k, v in record_info.items() if v is not None}

            records = TraitRecord.search(
                trait_name=self.trait_name,
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
