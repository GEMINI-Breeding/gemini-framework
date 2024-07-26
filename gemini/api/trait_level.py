from typing import Optional, List, Any
from gemini.api.base import APIBase, ID
from gemini.api.enums import GEMINITraitLevel
from gemini.models import TraitLevelModel, TraitModel
from gemini.logger import logger_service

from pydantic import Field, AliasChoices


class TraitLevel(APIBase):

    db_model = TraitLevelModel

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "trait_level_id"))
    trait_level_name: str
    trait_level_info: Optional[dict] = None


    @classmethod
    def create(cls, trait_level_name: str, trait_level_info: dict = None):
        db_instance = cls.db_model.get_or_create(
            trait_level_name=trait_level_name,
            trait_level_info=trait_level_info,
        )
        instance = cls.model_validate(db_instance)
        logger_service.info(
            "API",
            f"Created a new trait level with name {instance.trait_level_name} in the database",
        )
        return instance
    
    @classmethod
    def get(cls, trait_level_name: str) -> "TraitLevel":
        db_instance = cls.db_model.get_by_parameters(trait_level_name=trait_level_name)
        logger_service.info("API", f"Retrieved trait level with name {trait_level_name} from the database")
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info("API", f"Retrieved information about {self.trait_level_name} from the database")
        return self.trait_level_info
    
    def set_info(self, trait_level_info: Optional[dict] = None) -> "TraitLevel":
        self.update(trait_level_info=trait_level_info)
        logger_service.info("API", f"Set information about {self.trait_level_name} in the database")
        return self
    
    def add_info(self, trait_level_info: Optional[dict] = None) -> "TraitLevel":
        current_info = self.get_info()
        updated_info = {**current_info, **trait_level_info}
        self.set_info(updated_info)
        logger_service.info("API", f"Added information to {self.trait_level_name} in the database")
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "TraitLevel":
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info("API", f"Removed information from {self.trait_level_name} in the database")
        return self

