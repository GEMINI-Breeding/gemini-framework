from typing import Optional, List
from gemini.api.base import APIBase
from gemini.server.database.models import DatasetTypeModel


class DatasetType(APIBase):
    """
    Represents a dataset type in the Gemini framework.
    """

    db_model = DatasetTypeModel

    dataset_type_name: str
    dataset_type_info: Optional[dict] = None

    @classmethod
    def create(cls, dataset_type_name: str, dataset_type_info: dict = None):
        """
        Creates a new dataset type.

        Args:
            dataset_type_name (str): The name of the dataset type.
            dataset_type_info (dict, optional): Additional information about the dataset type. Defaults to None.

        Returns:
            DatasetType: The created dataset type.
        """
        db_instance = cls.db_model.get_or_create(
            dataset_type_name=dataset_type_name,
            dataset_type_info=dataset_type_info,
        )
        return cls.model_validate(db_instance)

    @classmethod
    def get(cls, dataset_type_name: str) -> "DatasetType":
        """
        Retrieves a dataset type by its name.

        Args:
            dataset_type_name (str): The name of the dataset type.

        Returns:
            DatasetType: The retrieved dataset type.
        """
        db_instance = cls.db_model.get_by_parameters(dataset_type_name=dataset_type_name)
        return cls.model_validate(db_instance)

    def get_info(self) -> dict:
        """
        Retrieves the information associated with the dataset type.

        Returns:
            dict: The information associated with the dataset type.
        """
        self.refresh()
        return self.dataset_type_info

    def set_info(self, dataset_type_info: Optional[dict] = None) -> "DatasetType":
        """
        Sets the information associated with the dataset type.

        Args:
            dataset_type_info (dict, optional): The information to set. Defaults to None.

        Returns:
            DatasetType: The updated dataset type.
        """
        self.update(dataset_type_info=dataset_type_info)
        return self

    def add_info(self, dataset_type_info: dict) -> "DatasetType":
        """
        Adds additional information to the dataset type.

        Args:
            dataset_type_info (dict): The additional information to add.

        Returns:
            DatasetType: The updated dataset type.
        """
        current_info = self.get_info()
        updated_info = {**current_info, **dataset_type_info}
        self.set_info(updated_info)
        return self

    def remove_info(self, keys_to_remove: List[str]) -> "DatasetType":
        """
        Removes specific keys from the information associated with the dataset type.

        Args:
            keys_to_remove (List[str]): The keys to remove from the information.

        Returns:
            DatasetType: The updated dataset type.
        """
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        return self

