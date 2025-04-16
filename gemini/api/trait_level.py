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
    def exists(
        cls,
        trait_level_name: str
    ) -> bool:
        try:
            exists = TraitLevelModel.exists(trait_level_name=trait_level_name)
            return exists
        except Exception as e:
            raise e

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
        
    def get_info(self) -> dict:
        try:
            current_id = self.id
            trait_level = TraitLevelModel.get(current_id)
            trait_level_info = trait_level.trait_level_info
            if not trait_level_info:
                raise Exception("TraitLevel info is empty.")
            return trait_level_info
        except Exception as e:
            raise e
        
    def set_info(self, trait_level_info: dict) -> "TraitLevel":
        try:
            current_id = self.id
            trait_level = TraitLevelModel.get(current_id)
            trait_level = TraitLevelModel.update(
                trait_level,
                trait_level_info=trait_level_info
            )
            trait_level = self.model_validate(trait_level)
            self.refresh()
            return self
        except Exception as e:
            raise e

        
    @classmethod
    def get(cls, trait_level_name: str) -> "TraitLevel":
        try:
            instance = TraitLevelModel.get_by_parameters(trait_level_name=trait_level_name)
            instance = cls.model_validate(instance)
            return instance if instance else None
        except Exception as e:
            raise e
        

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> "TraitLevel":
        try:
            instance = TraitLevelModel.get(id)
            instance = cls.model_validate(instance)
            return instance if instance else None
        except Exception as e:
            raise e
        

    @classmethod
    def get_all(cls) -> List["TraitLevel"]:
        try:
            instances = TraitLevelModel.all()
            instances = [cls.model_validate(instance) for instance in instances]
            return instances if instances else None
        except Exception as e:
            raise e
        


    @classmethod
    def search(
        cls,
        trait_level_name: str = None,
        trait_level_info: dict = None,
    ) -> List["TraitLevel"]:
        try:
            if not trait_level_name and not trait_level_info:
                raise Exception("Either trait_level_name or trait_level_info must be provided.")

            instances = TraitLevelModel.search(
                trait_level_name=trait_level_name,
                trait_level_info=trait_level_info,
            )
            instances = [cls.model_validate(instance) for instance in instances]
            return instances if instances else None
        except Exception as e:
            raise e
        
    
    def update(
        self,
        trait_level_name: str = None,
        trait_level_info: dict = None
    ) -> "TraitLevel":
        try:
            if not trait_level_info:
                raise ValueError("trait_level_info must be provided.")
            
            current_id = self.id
            trait_level = TraitLevelModel.get(current_id)
            trait_level = TraitLevelModel.update(
                trait_level,
                trait_level_name=trait_level_name,
                trait_level_info=trait_level_info,
            )
            trait_level = self.model_validate(trait_level)
            self.refresh()
            return trait_level
        except Exception as e:
            raise e
        
    
    def delete(self) -> bool:
        try:
            current_id = self.id
            trait_level = TraitLevelModel.get(current_id)
            TraitLevelModel.delete(trait_level)
            return True
        except Exception as e:
            raise e
    
    def refresh(self) -> "TraitLevel":  
        try:
            db_instance = TraitLevelModel.get(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e
