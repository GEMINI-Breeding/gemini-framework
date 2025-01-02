from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase

from gemini.db.models.trait_levels import TraitLevelModel

class TraitLevel(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "trait_level_id"))

    trait_level_name: str
    trait_level_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        trait_level_name: str,
        trait_level_info: dict = {},
    ) -> "TraitLevel":
        try:
            instance = TraitLevelModel.get_or_create(
                trait_level_name=trait_level_name,
                trait_level_info=trait_level_info,
            )
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        

    @classmethod
    def get(cls, trait_level_name: str) -> "TraitLevel":
        try:
            instance = TraitLevelModel.get_by_parameters(trait_level_name=trait_level_name)
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "TraitLevel":
        try:
            instance = TraitLevelModel.get(id)
            instance = cls.model_validate(instance)
            return instance
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["TraitLevel"]:
        try:
            instances = TraitLevelModel.get_all()
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            raise e
        


    @classmethod
    def search(
        cls,
        trait_level_name: str = None,
        trait_level_info: dict = None,
    ) -> List["TraitLevel"]:
        try:
            instances = TraitLevelModel.search(
                trait_level_name=trait_level_name,
                trait_level_info=trait_level_info,
            )
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            raise e
        
    
    def update(self, **kwargs) -> "TraitLevel":
        return super().update(**kwargs)
    
    def delete(self) -> bool:
        return super().delete()
    
    def refresh(self) -> "TraitLevel":  
        return super().refresh()