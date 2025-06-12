from typing import Optional, List
from uuid import UUID

from pydantic import Field, AliasChoices
from gemini.api.types import ID
from gemini.api.base import APIBase
from gemini.db.models.data_types import DataTypeModel
from gemini.db.models.data_formats import DataFormatModel
from gemini.db.models.associations import DataTypeFormatModel
from gemini.db.models.views.datatype_format_view import DataTypeFormatsViewModel

class DataType(APIBase):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "data_type_id"))

    data_type_name: str
    data_type_info: Optional[dict] = None

    def __str__(self):
        return f"DataType(name={self.data_type_name}, id={self.id})"

    def __repr__(self):
        return f"DataType(data_type_name={self.data_type_name}, id={self.id})"

    @classmethod
    def exists(
        cls,
        data_type_name: str
    ) -> bool:
        try:
            exists = DataTypeModel.exists(data_type_name=data_type_name)
            return exists
        except Exception as e:
            print(f"Error checking existence of data type: {e}")
            return False

    @classmethod
    def create(
        cls,
        data_type_name: str,
        data_type_info: dict = {},
    ) -> Optional["DataType"]:
        try:
            db_instance = DataTypeModel.get_or_create(
                data_type_name=data_type_name,
                data_type_info=data_type_info,
            )
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error creating data type: {e}")
            return None

    @classmethod
    def get(cls, data_type_name: str) -> Optional["DataType"]:
        try:
            db_instance = DataTypeModel.get_by_parameters(data_type_name=data_type_name)
            if not db_instance:
                print(f"Data type with name {data_type_name} not found.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting data type: {e}")
            return None

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> Optional["DataType"]:
        try:
            db_instance = DataTypeModel.get(id)
            if not db_instance:
                print(f"Data type with ID {id} does not exist.")
                return None
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            print(f"Error getting data type by ID: {e}")
            return None

    @classmethod
    def get_all(cls) -> Optional[List["DataType"]]:
        try:
            instances = DataTypeModel.all()
            if not instances or len(instances) == 0:
                print("No data types found.")
                return None
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            print(f"Error getting all data types: {e}")
            return None

    @classmethod
    def search(
        cls,
        data_type_name: str = None,
        data_type_info: dict = None
    ) -> Optional[List["DataType"]]:
        try:
            if not any([data_type_name, data_type_info]):
                print("At least one search parameter must be provided.")
                return None

            instances = DataTypeModel.search(
                data_type_name=data_type_name,
                data_type_info=data_type_info
            )
            if not instances or len(instances) == 0:
                print("No data types found with the provided search parameters.")
                return None
            instances = [cls.model_validate(instance) for instance in instances]
            return instances
        except Exception as e:
            print(f"Error searching data types: {e}")
            return None

    def update(
        self,
        data_type_name: str = None,
        data_type_info: dict = None,
    ) -> Optional["DataType"]:
        try:
            if not any([data_type_name, data_type_info]):
                print("At least one parameter must be provided for update.")
                return None

            current_id = self.id
            data_type = DataTypeModel.get(current_id)
            if not data_type:
                print(f"Data type with ID {current_id} does not exist.")
                return None

            data_type = DataTypeModel.update(
                data_type,
                data_type_name=data_type_name,
                data_type_info=data_type_info
            )
            instance = self.model_validate(data_type)
            self.refresh()
            return instance
        except Exception as e:
            print(f"Error updating data type: {e}")
            return None

    def delete(self) -> bool:
        try:
            current_id = self.id
            data_type = DataTypeModel.get(current_id)
            if not data_type:
                print(f"Data type with ID {current_id} does not exist.")
                return False
            DataTypeModel.delete(data_type)
            return True
        except Exception as e:
            print(f"Error deleting data type: {e}")
            return False

    def refresh(self) -> Optional["DataType"]:
        try:
            db_instance = DataTypeModel.get(self.id)
            if not db_instance:
                print(f"Data type with ID {self.id} does not exist.")
                return self
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    setattr(self, key, value)
            return self
        except Exception as e:
            print(f"Error refreshing data type: {e}")
            return None

    def get_info(self) -> Optional[dict]:
        try:
            current_id = self.id
            data_type = DataTypeModel.get(current_id)
            if not data_type:
                print(f"Data type with ID {current_id} does not exist.")
                return None
            data_type_info = data_type.data_type_info
            if not data_type_info:
                print("DataType info is empty.")
                return None
            return data_type_info
        except Exception as e:
            print(f"Error getting data type info: {e}")
            return None

    def set_info(self, data_type_info: dict) -> Optional["DataType"]:
        try:
            current_id = self.id
            data_type = DataTypeModel.get(current_id)
            if not data_type:
                print(f"Data type with ID {current_id} does not exist.")
                return None
            data_type = DataTypeModel.update(
                data_type,
                data_type_info=data_type_info,
            )
            instance = self.model_validate(data_type)
            self.refresh()
            return instance
        except Exception as e:
            print(f"Error setting data type info: {e}")
            return None
        
    def get_associated_data_formats(self):
        try:
            from gemini.api.data_format import DataFormat
            current_id = self.id
            data_type_formats = DataTypeFormatsViewModel.search(data_type_id=current_id)
            if not data_type_formats or len(data_type_formats) == 0:
                print(f"No associated data formats found for data type ID {current_id}.")
                return None
            data_formats = [DataFormat.model_validate(df) for df in data_type_formats]
            return data_formats
        except Exception as e:
            print(f"Error getting associated data formats: {e}")
            return None

    def associate_data_format(self, data_format_name: str):
        try:
            from gemini.api.data_format import DataFormat
            data_format = DataFormat.get(data_format_name=data_format_name)
            if not data_format:
                print(f"Data format {data_format_name} does not exist.")
                return None
            existing_association = DataTypeFormatModel.get_by_parameters(
                data_type_id=self.id,
                data_format_id=data_format.id
            )
            if existing_association:
                print(f"Data format {data_format_name} is already associated with data type ID {self.id}.")
                return data_format
            new_association = DataTypeFormatModel.get_or_create(
                data_type_id=self.id,
                data_format_id=data_format.id
            )
            if not new_association:
                print(f"Failed to associate data format {data_format_name} with data type ID {self.id}.")
                return None
            self.refresh()
            return data_format
        except Exception as e:
            print(f"Error associating data format: {e}")
            return None

    def unassociate_data_format(self, data_format_name: str) -> Optional["DataType"]:
        try:
            from gemini.api.data_format import DataFormat
            data_format = DataFormat.get(data_format_name=data_format_name)
            if not data_format:
                print(f"Data format {data_format_name} does not exist.")
                return None
            existing_association = DataTypeFormatModel.get_by_parameters(
                data_type_id=self.id,
                data_format_id=data_format.id
            )
            if not existing_association:
                print(f"Data format {data_format_name} is not associated with data type ID {self.id}.")
                return None
            is_deleted = DataTypeFormatModel.delete(existing_association)
            if not is_deleted:
                print(f"Failed to unassociate data format {data_format_name} from data type ID {self.id}.")
                return None
            self.refresh()
            return data_format
        except Exception as e:
            print(f"Error unassociating data format: {e}")
            return None

    def belongs_to_data_format(self, data_format_name: str) -> bool:
        try:
            from gemini.api.data_format import DataFormat
            data_format = DataFormat.get(data_format_name=data_format_name)
            if not data_format:
                print(f"Data format {data_format_name} does not exist.")
                return False
            association_exists = DataTypeFormatModel.exists(
                data_type_id=self.id,
                data_format_id=data_format.id
            )
            return association_exists
        except Exception as e:
            print(f"Error checking if data type belongs to data format: {e}")
            return False
    
    def add_new_data_format(
        self,
        data_format_name: str,
        data_format_mime_type: str = None,
        data_format_info: dict = {}
    ):
        try:
            from gemini.api.data_format import DataFormat
            new_data_format = DataFormat.create(
                data_format_name=data_format_name,
                data_format_mime_type=data_format_mime_type,
                data_format_info=data_format_info
            )
            if not new_data_format:
                print(f"Failed to create new data format {data_format_name}.")
                return None
            new_association = DataTypeFormatModel.get_or_create(
                data_type_id=self.id,
                data_format_id=new_data_format.id
            )
            if not new_association:
                print(f"Failed to associate new data format {data_format_name} with data type ID {self.id}.")
                return None
            self.refresh()
            return new_data_format
        except Exception as e:
            print(f"Error adding new data format: {e}")
            return None