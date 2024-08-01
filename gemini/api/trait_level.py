from typing import Optional, List
from gemini.api.base import APIBase, ID
from gemini.server.database.models import TraitLevelModel

from pydantic import Field, AliasChoices


class TraitLevel(APIBase):
    """
    Represents a trait level in the Gemini framework.
    """

    db_model = TraitLevelModel

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "trait_level_id"))
    trait_level_name: str
    trait_level_info: Optional[dict] = None


    @classmethod
    def create(cls, trait_level_name: str, trait_level_info: dict = None) -> "TraitLevel":
        """
        Creates a new TraitLevel instance with the given trait level name and info.

        Args:
            trait_level_name (str): The name of the trait level.
            trait_level_info (dict, optional): Additional information about the trait level. Defaults to None.

        Returns:
            TraitLevel: The created TraitLevel instance.
        """
        db_instance = cls.db_model.get_or_create(
            trait_level_name=trait_level_name,
            trait_level_info=trait_level_info,
        )
        instance = cls.model_validate(db_instance)
        return instance
    
    @classmethod
    def get(cls, trait_level_name: str) -> "TraitLevel":
        """
        Retrieves a TraitLevel instance with the given trait level name.

        Args:
            trait_level_name (str): The name of the trait level.

        Returns:
            TraitLevel: The retrieved TraitLevel instance.
        """
        db_instance = cls.db_model.get_by_parameters(trait_level_name=trait_level_name)
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        """
        Retrieves the information associated with the TraitLevel instance.

        Returns:
            dict: The information associated with the TraitLevel instance.
        """
        self.refresh()
        return self.trait_level_info
    
    def set_info(self, trait_level_info: Optional[dict] = None) -> "TraitLevel":
        """
        Sets the information associated with the TraitLevel instance.

        Args:
            trait_level_info (dict, optional): The information to be set. Defaults to None.

        Returns:
            TraitLevel: The updated TraitLevel instance.
        """
        self.update(trait_level_info=trait_level_info)
        return self
    
    def add_info(self, trait_level_info: Optional[dict] = None) -> "TraitLevel":
        """
        Adds additional information to the existing information associated with the TraitLevel instance.

        Args:
            trait_level_info (dict, optional): The additional information to be added. Defaults to None.

        Returns:
            TraitLevel: The updated TraitLevel instance.
        """
        current_info = self.get_info()
        updated_info = {**current_info, **trait_level_info}
        self.set_info(updated_info)
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "TraitLevel":
        """
        Removes specific keys from the information associated with the TraitLevel instance.

        Args:
            keys_to_remove (List[str]): The keys to be removed from the information.

        Returns:
            TraitLevel: The updated TraitLevel instance.
        """
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        return self
