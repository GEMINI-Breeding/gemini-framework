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

    def __str__(self):
        return f"TraitLevel(name={self.trait_level_name}, id={self.id})"

    def __repr__(self):
        return f"TraitLevel(trait_level_name={self.trait_level_name}, id={self.id})"

    @classmethod
    def exists(
        cls,
        trait_level_name: str
    ) -> bool:
        try:
            exists = TraitLevelModel.exists(trait_level_name=trait_level_name)
            return exists
        except Exception as e:
            print(f"Error checking existence of trait level: {e}")
            return False

    @classmethod
    def create(
        cls,
        trait_level_name: str,
        trait_level_info: dict = {},
    ) -> Optional["TraitLevel"]:
        try:
            db_instance = TraitLevelModel.get_or_create(
                trait_level_name=trait_level_name,
                trait_level_info=trait_level_info,
            )
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error creating trait level: {e}")
            return None

    @classmethod
    def get(cls, trait_level_name: str) -> Optional["TraitLevel"]:
        try:
            db_instance = TraitLevelModel.get_by_parameters(trait_level_name=trait_level_name)
            if not db_instance:
                print(f"Trait level with name {trait_level_name} not found.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting trait level: {e}")
            return None

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["TraitLevel"]:
        try:
            db_instance = TraitLevelModel.get(id)
            if not db_instance:
                print(f"Trait level with ID {id} does not exist.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting trait level by ID: {e}")
            return None

    @classmethod
    def get_all(cls) -> Optional[List["TraitLevel"]]:
        try:
            instances = TraitLevelModel.all()
            if not instances or len(instances) == 0:
                print("No trait levels found.")
                return None
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            print(f"Error getting all trait levels: {e}")
            return None

    @classmethod
    def search(
        cls,
        trait_level_name: str = None,
        trait_level_info: dict = None
    ) -> Optional[List["TraitLevel"]]:
        try:
            if not any([trait_level_name, trait_level_info]):
                print("At least one search parameter must be provided.")
                return None

            instances = TraitLevelModel.search(
                trait_level_name=trait_level_name,
                trait_level_info=trait_level_info
            )
            if not instances or len(instances) == 0:
                print("No trait levels found with the provided search parameters.")
                return None
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            print(f"Error searching trait levels: {e}")
            return None

    def update(
            self,
            trait_level_name: str = None,
            trait_level_info: dict = None
        ) -> Optional["TraitLevel"]:
        try:
            if not any([trait_level_name, trait_level_info]):
                print("At least one parameter must be provided for update.")
                return None

            current_id = self.id
            trait_level = TraitLevelModel.get(current_id)
            if not trait_level:
                 print(f"Trait level with ID {current_id} does not exist.")
                 return None

            trait_level = TraitLevelModel.update(
                trait_level,
                trait_level_name=trait_level_name,
                trait_level_info=trait_level_info,
            )
            instance = self.model_validate(trait_level)
            self.refresh()
            return instance
        except Exception as e:
            print(f"Error updating trait level: {e}")
            return None

    def delete(self) -> bool:
        try:
            current_id = self.id
            trait_level = TraitLevelModel.get(current_id)
            if not trait_level:
                 print(f"Trait level with ID {current_id} does not exist.")
                 return False
            TraitLevelModel.delete(trait_level)
            return True
        except Exception as e:
            print(f"Error deleting trait level: {e}")
            return False

    def refresh(self) -> Optional["TraitLevel"]:
        try:
            db_instance = TraitLevelModel.get(self.id)
            if not db_instance:
                print(f"Trait level with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing trait level: {e}")
            return None

    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            trait_level = TraitLevelModel.get(current_id)
            if not trait_level:
                print(f"Trait level with ID {current_id} does not exist.")
                return None
            trait_level_info = trait_level.trait_level_info
            if not trait_level_info:
                print("TraitLevel info is empty.")
                return None
            return trait_level_info
        except Exception as e:
            print(f"Error getting trait level info: {e}")
            return None

    def set_info(self, trait_level_info: dict) -> Optional["TraitLevel"]:
        try:
            current_id = self.id
            trait_level = TraitLevelModel.get(current_id)
            if not trait_level:
                print(f"Trait level with ID {current_id} does not exist.")
                return None
            trait_level = TraitLevelModel.update(
                trait_level,
                trait_level_info=trait_level_info,
            )
            instance = self.model_validate(trait_level)
            self.refresh()
            return instance
        except Exception as e:
            print(f"Error setting trait level info: {e}")
            return None
