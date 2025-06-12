from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.data_formats import DataFormatModel
from gemini.db.models.associations import DataTypeFormatModel
from gemini.db.models.views.datatype_format_view import DataTypeFormatsViewModel

class DataFormat(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "data_format_id"))

    data_format_name: str
    data_format_mime_type: Optional[str] = None
    data_format_info: Optional[dict] = None

    def __str__(self):
        return f"DataFormat(name={self.data_format_name}, mime_type={self.data_format_mime_type}, id={self.id})"

    def __repr__(self):
        return f"DataFormat(data_format_name={self.data_format_name}, data_format_mime_type={self.data_format_mime_type}, id={self.id})"

    @classmethod
    def exists(
        cls,
        data_format_name: str
    ) -> bool:
        try:
            exists = DataFormatModel.exists(data_format_name=data_format_name)
            return exists
        except Exception as e:
            print(f"Error checking existence of data format: {e}")
            return False

    @classmethod
    def create(
        cls,
        data_format_name: str,
        data_format_mime_type: str = None,
        data_format_info: dict = {},
    ) -> Optional["DataFormat"]:
        try:
            db_instance = DataFormatModel.get_or_create(
                data_format_name=data_format_name,
                data_format_mime_type=data_format_mime_type,
                data_format_info=data_format_info,
            )
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error creating data format: {e}")
            return None

    @classmethod
    def get(cls, data_format_name: str) -> Optional["DataFormat"]:
        try:
            db_instance = DataFormatModel.get_by_parameters(data_format_name=data_format_name)
            if not db_instance:
                print(f"Data format with name {data_format_name} not found.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting data format: {e}")
            return None

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["DataFormat"]:
        try:
            db_instance = DataFormatModel.get(id)
            if not db_instance:
                print(f"Data format with ID {id} does not exist.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting data format by ID: {e}")
            return None

    @classmethod
    def get_all(cls) -> Optional[List["DataFormat"]]:
        try:
            instances = DataFormatModel.all()
            if not instances or len(instances) == 0:
                print("No data formats found.")
                return None
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            print(f"Error getting all data formats: {e}")
            return None

    @classmethod
    def search(
        cls,
        data_format_name: str = None,
        data_format_mime_type: str = None,
        data_format_info: dict = None
    ) -> Optional[List["DataFormat"]]:
        try:
            if not any([data_format_name, data_format_mime_type, data_format_info]):
                print("At least one search parameter must be provided.")
                return None

            data_formats = DataFormatModel.search(
                data_format_name=data_format_name,
                data_format_mime_type=data_format_mime_type,
                data_format_info=data_format_info,
            )
            if not data_formats or len(data_formats) == 0:
                print("No data formats found with the provided search parameters.")
                return None
            data_formats = [cls.model_validate(data_format) for data_format in data_formats]
            return data_formats
        except Exception as e:
            print(f"Error searching data formats: {e}")
            return None

    def update(
        self,
        data_format_name: str = None,
        data_format_mime_type: str = None,
        data_format_info: dict = None,
    ) -> Optional["DataFormat"]:
        try:
            if not any([data_format_name, data_format_mime_type, data_format_info]):
                print("At least one parameter must be provided for update.")
                return None

            current_id = self.id
            data_format = DataFormatModel.get(current_id)
            if not data_format:
                print(f"Data format with ID {current_id} does not exist.")
                return None

            data_format = DataFormatModel.update(
                data_format,
                data_format_name=data_format_name,
                data_format_mime_type=data_format_mime_type,
                data_format_info=data_format_info,
            )
            instance = self.model_validate(data_format)
            self.refresh() # Refresh self with updated data
            return instance # Return the validated instance
        except Exception as e:
            print(f"Error updating data format: {e}")
            return None

    def delete(self) -> bool:
        try:
            current_id = self.id
            data_format = DataFormatModel.get(current_id)
            if not data_format:
                print(f"Data format with ID {current_id} does not exist.")
                return False
            DataFormatModel.delete(data_format)
            return True
        except Exception as e:
            print(f"Error deleting data format: {e}")
            return False

    def refresh(self) -> Optional["DataFormat"]:
        try:
            db_instance = DataFormatModel.get(self.id)
            if not db_instance:
                print(f"Data format with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            # Update self attributes
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing data format: {e}")
            return None

    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            data_format = DataFormatModel.get(current_id)
            if not data_format:
                print(f"Data format with ID {current_id} does not exist.")
                return None
            data_format_info = data_format.data_format_info
            if not data_format_info:
                print("DataFormat info is empty.")
                return None # Return None if info is empty/None
            return data_format_info
        except Exception as e:
            print(f"Error getting data format info: {e}")
            return None

    def set_info(self, data_format_info: dict) -> Optional["DataFormat"]:
        try:
            current_id = self.id
            data_format = DataFormatModel.get(current_id)
            if not data_format:
                print(f"Data format with ID {current_id} does not exist.")
                return None
            data_format = DataFormatModel.update(
                data_format,
                data_format_info=data_format_info,
            )
            instance = self.model_validate(data_format)
            self.refresh() # Refresh self
            return instance # Return validated instance
        except Exception as e:
            print(f"Error setting data format info: {e}")
            return None

    def get_associated_data_types(self):
        try:
            from gemini.api.data_type import DataType
            current_id = self.id
            data_type_formats = DataTypeFormatsViewModel.search(
                data_format_id=current_id
            )
            if not data_type_formats or len(data_type_formats) == 0:
                print(f"No associated data types found for data format ID {current_id}.")
                return None
            data_types = [DataType.model_validate(data_type_format) for data_type_format in data_type_formats]
            return data_types
        except Exception as e:
            print(f"Error getting associated data types: {e}")
            return None

    def associate_data_type(self, data_type_name: str):
        try:
            from gemini.api.data_type import DataType
            data_type = DataType.get(data_type_name=data_type_name)
            if not data_type:
                print(f"Data type with name {data_type_name} does not exist.")
                return None
            existing_association = DataTypeFormatModel.get_or_create(
                data_type_id=data_type.id,
                data_format_id=self.id
            )
            if existing_association:
                print(f"Data type {data_type_name} is already associated with data format ID {self.id}.")
                return data_type
            new_association = DataTypeFormatModel.create(
                data_type_id=data_type.id,
                data_format_id=self.id
            )
            if not new_association:
                print(f"Failed to create association for data type {data_type_name} with data format ID {self.id}.")
                return None
            self.refresh()  # Refresh self with updated data
            return data_type
        except Exception as e:
            print(f"Error associating data type {data_type_name} with data format: {e}")
            return None


    def unassociate_data_type(self, data_type_name: str):
        try:
            from gemini.api.data_type import DataType
            data_type = DataType.get(data_type_name=data_type_name)
            if not data_type:
                print(f"Data type with name {data_type_name} does not exist.")
                return None
            existing_association = DataTypeFormatModel.get_by_parameters(
                data_type_id=data_type.id,
                data_format_id=self.id
            )
            if not existing_association:
                print(f"Data type {data_type_name} is not associated with data format ID {self.id}.")
                return None
            is_deleted = DataTypeFormatModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to unassociate data type {data_type_name} from data format ID {self.id}.")
                return None
            self.refresh()  # Refresh self with updated data
            return data_type
        except Exception as e:
            print(f"Error unassociating data type {data_type_name} from data format: {e}")
            return None

    def belongs_to_data_type(self, data_type_name: str) -> bool:
        try:
            from gemini.api.data_type import DataType
            data_type = DataType.get(data_type_name=data_type_name)
            if not data_type:
                print(f"Data type with name {data_type_name} does not exist.")
                return False
            association_exists = DataTypeFormatModel.exists(
                data_type_id=data_type.id,
                data_format_id=self.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if data format belongs to data type {data_type_name}: {e}")
            return False
