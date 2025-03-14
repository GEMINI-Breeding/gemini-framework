from typing import Optional, List
from uuid import UUID

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
from datetime import date

class Trait(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "trait_id"))

    trait_name: str
    trait_units: str
    trait_level_id: Optional[int] = None
    trait_info: Optional[dict] = None
    trait_metrics: Optional[dict] = None

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
            raise e
        

        
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

    def add_record(
        self,
        record: TraitRecord
    ) -> bool:
        try:
            record.trait_id = self.id
            record.trait_name = self.trait_name
            record.dataset_name = f"{self.trait_name} Dataset"
            record.timestamp = record.timestamp if record.timestamp else date.today()

            success = TraitRecord.add([record])
            return success
        except Exception as e:
            raise e
        
    def add_records(
        self,
        records: List[TraitRecord]
    ) -> bool:
        try:
            for record in records:
                record.trait_id = self.id
                record.trait_name = self.trait_name
                record.dataset_name = f"{self.trait_name} Dataset"
                record.timestamp = record.timestamp if record.timestamp else date.today()

            success = TraitRecord.add(records)
            return success
        except Exception as e:
            raise e
        
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


