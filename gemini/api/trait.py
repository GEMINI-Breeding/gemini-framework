from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.api.enums import GEMINITraitLevel
from gemini.db.models.traits import TraitModel
from gemini.db.models.trait_levels import TraitLevelModel
from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.views.experiment_views import ExperimentTraitsViewModel


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
        trait_units: str,
        trait_level: GEMINITraitLevel = GEMINITraitLevel.Plot,
        trait_info: dict = {},
        experiment_name: str = "Default",
    ) -> "Trait":
        try:
            trait_level_id = trait_level.value
            trait = TraitModel.get_or_create(
                trait_name=trait_name,
                trait_units=trait_units,
                trait_level_id=trait_level_id,
                trait_info=trait_info,
            )
            trait = cls.model_validate(trait)
            experiment = ExperimentModel.get_by_parameters(experiment_name=experiment_name)
            if experiment:
                experiment.traits.append(trait)
            return trait
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, trait_name: str) -> "Trait":
        try:
            trait = TraitModel.get_by_parameters(trait_name=trait_name)
            trait = cls.model_validate(trait)
            return trait
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "Trait":
        try:
            trait = TraitModel.get(id)
            trait = cls.model_validate(trait)
            return trait
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
    def search(cls, **search_parameters) -> List["Trait"]:
        try:
            traits = ExperimentTraitsViewModel.search(**search_parameters)
            traits = [cls.model_validate(trait) for trait in traits]
            return traits if traits else None
        except Exception as e:
            raise e
        

    def update(self, **update_parameters) -> "Trait":
        try:
            current_id = self.id
            trait = TraitModel.get(current_id)
            trait = TraitModel.update(trait, **update_parameters)
            trait = self.model_validate(trait)
            self.refresh()
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
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            raise e


