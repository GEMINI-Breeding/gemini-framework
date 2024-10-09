from typing import Optional, List
from gemini.api.base import APIBase
from gemini.server.database.models import DataFormatModel

class DataFormat(APIBase):
    """
    Represents a data format in the Gemini framework.

    Attributes:
        db_model: The database model associated with the data format.
        data_format_name: The name of the data format.
        data_format_mime_type: The MIME type of the data format.
        data_format_info: Additional information about the data format.
    """

    db_model = DataFormatModel

    data_format_name: str
    data_format_mime_type: Optional[str] = None
    data_format_info: Optional[dict] = None

    @classmethod
    def create(
        cls,
        data_format_name: str,
        data_format_mime_type: str = None,
        data_format_info: dict = None,
    ):
        """
        Creates a new data format.

        Args:
            data_format_name: The name of the data format.
            data_format_mime_type: The MIME type of the data format.
            data_format_info: Additional information about the data format.

        Returns:
            The created DataFormat instance.
        """
        db_instance = cls.db_model.get_or_create(
            data_format_name=data_format_name,
            data_format_mime_type=data_format_mime_type,
            data_format_info=data_format_info,
        )

        return cls.model_validate(db_instance)

    @classmethod
    def get(cls, data_format_name: str) -> "DataFormat":
        """
        Retrieves a data format by its name.

        Args:
            data_format_name: The name of the data format.

        Returns:
            The DataFormat instance with the specified name.
        """
        db_instance = cls.db_model.get_by_parameters(data_format_name=data_format_name)
        return cls.model_validate(db_instance)

    @classmethod
    def get_format_from_file_path(cls, file_path: str):
        """
        Retrieves the data formats associated with a file path.

        Args:
            file_path: The path of the file.

        Returns:
            A list of DataFormat instances associated with the file extension.
        """
        file_extension = file_path.split(".")[-1]
        data_formats = cls.db_model.search(data_format_name=file_extension)
        data_formats = [cls.model_validate(data_format) for data_format in data_formats]
        return data_formats

    def get_info(self) -> dict:
        """
        Retrieves the additional information about the data format.

        Returns:
            The additional information about the data format.
        """
        self.refresh()
        return self.data_format_info

    def set_info(self, data_format_info: Optional[dict] = None) -> "DataFormat":
        """
        Sets the additional information about the data format.

        Args:
            data_format_info: The additional information about the data format.

        Returns:
            The updated DataFormat instance.
        """
        self.update(data_format_info=data_format_info)
        return self

    def add_info(self, data_format_info: Optional[dict] = None) -> "DataFormat":
        """
        Adds additional information to the existing data format information.

        Args:
            data_format_info: The additional information to add.

        Returns:
            The updated DataFormat instance.
        """
        current_info = self.get_info()
        updated_info = {**current_info, **data_format_info}
        self.set_info(updated_info)
        return self

    def remove_info(self, keys_to_remove: List[str]) -> "DataFormat":
        """
        Removes specific keys from the data format information.

        Args:
            keys_to_remove: The keys to remove from the data format information.

        Returns:
            The updated DataFormat instance.
        """
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        return self
