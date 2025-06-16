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

    def __str__(self):
        return f"Trait(name={self.trait_name}, id={self.id})"
    
    def __repr__(self):
        return f"Trait(trait_name={self.trait_name}, id={self.id})"
    
    @classmethod
    def exists(
        cls,
        trait_name: str
    ) -> bool:
        try:
            exists = TraitModel.exists(trait_name=trait_name)
            return exists
        except Exception as e:
            print(f"Error checking existence of trait: {e}")
            return False
        
    @classmethod
    def create(
        cls,
        trait_name: str,
        trait_units: str = None,
        trait_level: GEMINITraitLevel = GEMINITraitLevel.Plot,
        trait_info: dict = {},
        trait_metrics: dict = {},
        experiment_name: str = None
    ) -> Optional["Trait"]:
        try:
            trait_level_id = trait_level.value if isinstance(trait_level, GEMINITraitLevel) else trait_level
            trait = TraitModel.get_or_create(
                trait_name=trait_name,
                trait_units=trait_units,
                trait_level_id=trait_level_id,
                trait_metrics=trait_metrics,
                trait_info=trait_info,
            )
            trait = cls.model_validate(trait)
            if experiment_name:
                trait.associate_experiment(experiment_name)
            return trait
        except Exception as e:
            print(f"Error creating trait: {e}")
            return None
        
    @classmethod
    def get(
        cls,
        trait_name: str,
        experiment_name: str = None
    ) -> Optional["Trait"]:
        try:
            trait = ExperimentTraitsViewModel.get_by_parameters(
                trait_name=trait_name,
                experiment_name=experiment_name   
            )
            if not trait:
                print(f"Trait with name {trait_name} not found.")
                return None
            trait = cls.model_validate(trait)
            return trait
        except Exception as e:
            print(f"Error getting trait: {e}")
            return None
    
    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["Trait"]:
        try:
            trait = TraitModel.get(id)
            if not trait:
                print(f"Trait with ID {id} does not exist.")
                return None
            trait = cls.model_validate(trait)
            return trait
        except Exception as e:
            print(f"Error getting trait by ID: {e}")
            return None

    @classmethod
    def get_all(cls) -> Optional[List["Trait"]]:
        try:
            traits = TraitModel.all()
            if not traits or len(traits) == 0:
                print("No traits found.")
                return None
            traits = [cls.model_validate(trait) for trait in traits]
            return traits
        except Exception as e:
            print(f"Error getting all traits: {e}")
            return None
        
    @classmethod
    def search(
        cls, 
        trait_name: str = None,
        trait_units: str = None,
        trait_level: GEMINITraitLevel = None,
        trait_info: dict = None,
        trait_metrics: dict = None,
        experiment_name: str = None
    ) -> Optional[List["Trait"]]:
        try:
            if not any([experiment_name, trait_name, trait_units, trait_level, trait_info, trait_metrics]):
                print("At least one search parameter must be provided.")
                return None
            
            traits = ExperimentTraitsViewModel.search(
                experiment_name=experiment_name,
                trait_name=trait_name,
                trait_units=trait_units,
                trait_level_id=trait_level.value if trait_level else None,
                trait_info=trait_info,
                trait_metrics=trait_metrics
            )
            if not traits or len(traits) == 0:
                print("No traits found with the provided search parameters.")
                return None
            traits = [cls.model_validate(trait) for trait in traits]
            return traits if traits else None
        except Exception as e:
            print(f"Error searching traits: {e}")
            return None
            
    def update(
        self,
        trait_name: str = None, 
        trait_units: str = None,
        trait_level: GEMINITraitLevel = None,
        trait_info: dict = None,
        trait_metrics: dict = None,
    ) -> Optional["Trait"]:
        try:
            if not any([trait_units, trait_level, trait_info, trait_metrics, trait_name]):
                print("At least one update parameter must be provided.")
                return None

            current_id = self.id
            trait = TraitModel.get(current_id)
            if not trait:
                print(f"Trait with ID {current_id} does not exist.")
                return None
            
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
            print(f"Error updating trait: {e}")
            return None
    
    def delete(self) -> bool:
        try:
            current_id = self.id
            trait = TraitModel.get(current_id)
            if not trait:
                print(f"Trait with ID {current_id} does not exist.")
                return False
            TraitModel.delete(trait)
            return True
        except Exception as e:
            print(f"Error deleting trait: {e}")
            return False
        
    def refresh(self) -> Optional["Trait"]:
        try:
            db_instance = TraitModel.get(self.id)
            if not db_instance:
                print(f"Trait with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing trait: {e}")
            return None
        
    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            trait = TraitModel.get(current_id)
            if not trait:
                print(f"Trait with ID {current_id} does not exist.")
                return None
            trait_info = trait.trait_info
            if not trait_info:
                print("Trait info is empty.")
                return None
            return trait_info
        except Exception as e:
            print(f"Error getting trait info: {e}")
            return None
        
    def set_info(self, trait_info: dict) -> Optional["Trait"]:
        try:
            current_id = self.id
            trait = TraitModel.get(current_id)
            if not trait:
                print(f"Trait with ID {current_id} does not exist.")
                return None
            trait = TraitModel.update(
                trait,
                trait_info=trait_info
            )
            trait = self.model_validate(trait)
            self.refresh()
            return self
        except Exception as e:
            print(f"Error setting trait info: {e}")
            return None
        
    def get_associated_experiments(self):
        try:
            from gemini.api.experiment import Experiment
            experiment_traits = ExperimentTraitsViewModel.search(trait_id=self.id)
            if not experiment_traits or len(experiment_traits) == 0:
                print("No associated experiments found.")
                return None
            experiments = [Experiment.model_validate(experiment) for experiment in experiment_traits]
            return experiments
        except Exception as e:
            print(f"Error getting associated experiments: {e}")
            return None

    def associate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return None
            existing_association = ExperimentTraitModel.get_by_parameters(
                experiment_id=experiment.id,
                trait_id=self.id
            )
            if existing_association:
                print(f"Trait {self.trait_name} is already associated with experiment {experiment_name}.")
                return True
            new_association = ExperimentTraitModel.get_or_create(
                experiment_id=experiment.id,
                trait_id=self.id
            )
            if not new_association:
                print(f"Failed to associate trait {self.trait_name} with experiment {experiment_name}.")
                return False
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error associating experiment: {e}")
            return None

    def unassociate_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return None
            existing_association = ExperimentTraitModel.get_by_parameters(
                experiment_id=experiment.id,
                trait_id=self.id
            )
            if not existing_association:
                print(f"Trait {self.trait_name} is not associated with experiment {experiment_name}.")
                return None
            is_deleted = ExperimentTraitModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to unassociate trait {self.trait_name} from experiment {experiment_name}.")
                return False
            self.refresh()
            return experiment
        except Exception as e:
            print(f"Error unassociating experiment: {e}")
            return None

    def belongs_to_experiment(self, experiment_name: str):
        try:
            from gemini.api.experiment import Experiment
            experiment = Experiment.get(experiment_name)
            if not experiment:
                print(f"Experiment {experiment_name} does not exist.")
                return False
            association_exists = ExperimentTraitModel.exists(
                experiment_id=experiment.id,
                trait_id=self.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if trait belongs to experiment: {e}")
            return

    def get_associated_datasets(self):
        try:
            from gemini.api.dataset import Dataset
            datasets = TraitDatasetsViewModel.search(trait_id=self.id)
            if not datasets or len(datasets) == 0:
                print("No associated datasets found.")
                return None
            datasets = [Dataset.model_validate(dataset) for dataset in datasets]
            return datasets
        except Exception as e:
            print(f"Error getting associated datasets: {e}")
            return None

    def create_new_dataset(
        self,
        dataset_name: str,
        dataset_info: dict = {},
        collection_date: date = None,
        experiment_name: str = None
    ):
        try:
            from gemini.api.dataset import Dataset
            dataset = Dataset.create(
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type=GEMINIDatasetType.Trait,
                collection_date=collection_date,
                experiment_name=experiment_name
            )
            if not dataset:
                print(f"Failed to create dataset {dataset_name}.")
                return None
            dataset = self.associate_dataset(dataset_name)
            return dataset
        except Exception as e:
            print(f"Error creating new dataset: {e}")
            return None
    
    def associate_dataset(self, dataset_name: str):
        try:
            from gemini.api.dataset import Dataset
            dataset = Dataset.get(dataset_name)
            if not dataset:
                print(f"Dataset {dataset_name} does not exist.")
                return None
            existing_association = TraitDatasetModel.get_by_parameters(
                trait_id=self.id,
                dataset_id=dataset.id
            )
            if existing_association:
                print(f"Trait {self.trait_name} is already associated with dataset {dataset_name}.")
                return True
            new_association = TraitDatasetModel.get_or_create(
                trait_id=self.id,
                dataset_id=dataset.id
            )
            if not new_association:
                print(f"Failed to associate trait {self.trait_name} with dataset {dataset_name}.")
                return False
            self.refresh()
            return dataset
        except Exception as e:
            print(f"Error associating dataset: {e}")
            return None

    def insert_record(
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
            
            if not trait_value:
                raise ValueError("Trait value must be provided.")
            
            timestamp = timestamp if timestamp else datetime.now()
            collection_date = collection_date if collection_date else timestamp.date()
            trait_name = self.trait_name
            if not dataset_name:
                dataset_name = f"{trait_name} Dataset {collection_date}"
            trait_record = TraitRecord.create(
                timestamp=timestamp,
                collection_date=collection_date,
                trait_name=trait_name,
                dataset_name=dataset_name,
                trait_value=trait_value,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number if plot_number != -1 else None,
                plot_row_number=plot_row_number if plot_row_number != -1 else None,
                plot_column_number=plot_column_number if plot_column_number != -1 else None,
                record_info=record_info if record_info else {},
                insert_on_create=False
            )
            success, inserted_record_ids = TraitRecord.insert([trait_record])
            if not success:
                print(f"Failed to insert record for trait {trait_name}.")
                return False, []
            return success, inserted_record_ids
        except Exception as e:
            print(f"Error inserting record: {e}")
            return False, []
        
    def insert_records(
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
                dataset_name = f"{self.trait_name} Dataset {collection_date}"
            
            collection_date = collection_date if collection_date else timestamps[0].date()
            trait_records = []
            timestamps_length = len(timestamps)

            for i in tqdm(range(timestamps_length), desc="Arranging Records for Trait: " + self.trait_name):
                trait_record = TraitRecord.create(
                    timestamp=timestamps[i],
                    collection_date=collection_date,
                    trait_name=self.trait_name,
                    trait_value=trait_values[i] if trait_values else None,
                    dataset_name=dataset_name if dataset_name else f"{self.trait_name} Dataset {collection_date}",
                    experiment_name=experiment_name,
                    season_name=season_name,
                    site_name=site_name,
                    plot_number=plot_numbers[i] if plot_numbers else None,
                    plot_row_number=plot_row_numbers[i] if plot_row_numbers else None,
                    plot_column_number=plot_column_numbers[i] if plot_column_numbers else None,
                    record_info=record_info[i] if record_info else {},
                    insert_on_create=False
                )
                trait_records.append(trait_record)

            success, inserted_record_ids = TraitRecord.insert(trait_records)
            return success, inserted_record_ids
        except Exception as e:
            print(f"Error inserting records: {e}")
            return False, []
        
    def search_records(
        self,
        collection_date: date = None,
        dataset_name: str = None,
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
                dataset_name=dataset_name,
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
            print(f"Error searching records: {e}")
            return []
        
    def filter_records(
        self,
        start_timestamp: Optional[datetime] = None,
        end_timestamp: Optional[datetime] = None,
        dataset_names: Optional[List[str]] = None,
        experiment_names: Optional[List[str]] = None,
        season_names: Optional[List[str]] = None,
        site_names: Optional[List[str]] = None
    ) -> List[TraitRecord]:
        try:
            records = TraitRecord.filter(
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                trait_names=[self.trait_name],
                dataset_names=dataset_names,
                experiment_names=experiment_names,
                season_names=season_names,
                site_names=site_names
            )
            return records
        except Exception as e:
            print(f"Error filtering trait records: {e}")
            return []