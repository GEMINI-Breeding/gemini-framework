from typing import Optional, List
from gemini.api.base import APIBase
from gemini.api.data_format import DataFormat
from gemini.server.database.models import DataTypeModel


class DataType(APIBase):
    """
    Represents a data type in the Gemini framework.

    Attributes:
        db_model (Type[BaseModel]): The database model associated with the data type.
        data_type_name (str): The name of the data type.
        data_type_info (Optional[dict]): Additional information about the data type.
        formats (Optional[List[DataFormat]]): The list of data formats associated with the data type.
    """

    db_model = DataTypeModel

    data_type_name: str
    data_type_info: Optional[dict] = None

    formats: Optional[List[DataFormat]] = None

    @classmethod
    def create(cls, data_type_name: str, data_type_info: dict = None):
        """
        Creates a new data type with the given name and information.

        Args:
            data_type_name (str): The name of the data type.
            data_type_info (dict, optional): Additional information about the data type.

        Returns:
            DataType: The created data type.
        """
        db_instance = cls.db_model.get_or_create(
            data_type_name=data_type_name,
            data_type_info=data_type_info,
        )
        return cls.model_validate(db_instance)
    
    @classmethod
    def get(cls, data_type_name: str) -> "DataType":
        """
        Retrieves the data type with the given name.

        Args:
            data_type_name (str): The name of the data type.

        Returns:
            DataType: The retrieved data type.
        """
        db_instance = cls.db_model.get_by_parameters(data_type_name=data_type_name)
        return cls.model_validate(db_instance)
    
    def get_info(self) -> dict:
        """
        Retrieves the additional information about the data type.

        Returns:
            dict: The additional information about the data type.
        """
        self.refresh()
        return self.data_type_info
    
    def set_info(self, data_type_info: Optional[dict] = None) -> "DataType":
        """
        Sets the additional information about the data type.

        Args:
            data_type_info (dict, optional): The additional information about the data type.

        Returns:
            DataType: The updated data type.
        """
        self.update(data_type_info=data_type_info)
        return self
    
    def add_info(self, data_type_info: Optional[dict] = None) -> "DataType":
        """
        Adds or updates the additional information about the data type.

        Args:
            data_type_info (dict, optional): The additional information to add or update.

        Returns:
            DataType: The updated data type.
        """
        current_info = self.get_info()
        updated_info = {**current_info, **data_type_info}
        self.set_info(updated_info)
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> "DataType":
        """
        Removes the specified keys from the additional information of the data type.

        Args:
            keys_to_remove (List[str]): The keys to remove from the additional information.

        Returns:
            DataType: The updated data type.
        """
        current_info = self.get_info()
        updated_info = {
            key: value
            for key, value in current_info.items()
            if key not in keys_to_remove
        }
        self.set_info(updated_info)
        return self
    
    @classmethod
    def get_data_formats(cls, data_type_name: str) -> List[DataFormat]:
        """
        Retrieves the list of data formats associated with the data type.

        Args:
            data_type_name (str): The name of the data type.

        Returns:
            List[DataFormat]: The list of data formats associated with the data type.
        """
        data_type = cls.get(data_type_name)
        data_formats = data_type.formats
        return data_formats


