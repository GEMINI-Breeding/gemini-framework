import os

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import model_validator
from typing import Any, Optional, Union, ClassVar
from uuid import UUID
from gemini.api.types import ID
from gemini.server.file_server.handler import MinioFileHandler
from gemini.server.database.models import BaseModel as DBBaseModel
from gemini.server.database.models.columnar.columnar_base_model import ColumnarBaseModel
from gemini.server.database.models.views.view_base import ViewBaseModel



class APIBase(BaseModel):
    """
    Base class for all API classes

    Attributes:
    - db_model (ClassVar[DBBaseModel]): The database model associated with the API class.
    - minio_client (ClassVar[Minio]): The Minio client for the API class.
    - model_config (ConfigDict): Configuration for the model, including attribute handling and namespaces.
    - id (Optional[Union[UUID, str, int]]): The ID of the instance (optional).

    Methods:
    - check_db_model(cls, data: Any) -> Any: Checks if the given data is an instance of the database model.
    - create(cls, **kwargs) -> APIBase: Creates a new instance of the class and adds it to the database.
    - get_by_id(cls, id: Union[UUID, int, str]) -> APIBase: Retrieves an instance of the class by ID.
    - all(cls) -> List[APIBase]: Retrieves all instances of the class from the database.
    - search(cls, **search_parameters) -> List[APIBase]: Searches for instances of the class in the database.

    - update(self, **kwargs) -> APIBase: Updates the instance in the database.
    - delete(self) -> bool: Deletes the instance from the database.
    - refresh(self) -> APIBase: Refreshes the instance from the database.
    """

    db_model: ClassVar[DBBaseModel] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        protected_namespaces=(),
        extra="allow"
    )

    id: Optional[ID] = None

    @model_validator(mode="before")
    @classmethod
    def check_db_model(cls, data: Any) -> Any:
        if isinstance(data, (DBBaseModel, ColumnarBaseModel, ViewBaseModel)):
            return data

        db_instance = cls.db_model.get_or_create(**data)
        return db_instance

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a new instance of the class and adds it to the database.

        Args:
        - **kwargs: The fields of the instance.

        Returns:
        - APIBase: The created instance.

        Raises:
        - Exception: If an error occurs during creation.
        """
        try:
            db_instance = cls.db_model.get_or_create(**kwargs)
            instance = cls.model_validate(db_instance)
            return instance
        except Exception as e:
            raise e

    @classmethod
    def get_by_id(cls, id: Union[UUID, int, str]) -> "APIBase":
        """
        Retrieves an instance of the class by ID.

        Args:
        - id (Union[UUID, int, str]): The ID of the instance.

        Returns:
        - APIBase: The instance with the given ID.

        Raises:
        - Exception: If an error occurs during retrieval.
        """
        try:
            instance_from_db = cls.db_model.get_by_id(id)
            instance = cls.model_validate(instance_from_db)
            return instance
        except Exception as e:
            raise e

    @classmethod
    def all(cls):
        """
        Retrieves all instances of the class from the database.

        Returns:
        - List[APIBase]: A list of all the instances of the class.

        Raises:
        - Exception: If an error occurs during retrieval.
        """
        try:
            db_instances = cls.db_model.get_all()
            instances = [cls.model_validate(instance) for instance in db_instances]
            return instances
        except Exception as e:
            raise e

    @classmethod
    def search(cls, **search_parameters):
        """
        Searches for instances of the class in the database.

        Args:
        - **search_parameters: The search parameters.

        Returns:
        - List[APIBase]: A list of the instances that match the search parameters.

        Raises:
        - Exception: If an error occurs during the search.
        """
        try:
            db_instances = cls.db_model.search(**search_parameters)
            instances = [cls.model_validate(instance) for instance in db_instances]
            return instances
        except Exception as e:
            raise e

    def update(self, **kwargs):
        """
        Updates the instance in the database.

        Args:
        - **kwargs: The fields to update.

        Returns:
        - APIBase: The updated instance.

        Raises:
        - Exception: If an error occurs during the update.
        """
        try:
            db_instance = self.db_model.get_by_id(self.id)
            db_instance = self.db_model.update(db_instance, **kwargs)
            instance = self.model_validate(db_instance)
            self.refresh()
            return instance
        except Exception as e:
            raise e

    def delete(self):
        """
        Deletes the instance from the database.

        Returns:
        - bool: True if the instance was deleted, False otherwise.

        Raises:
        - Exception: If an error occurs during the deletion.
        """
        try:
            db_instance = self.db_model.get_by_id(self.id)
            is_deleted = self.db_model.delete(db_instance)
            if not is_deleted:
                raise Exception("Failed to delete the instance from the database")
            return is_deleted
        except Exception as e:
            raise e

    def refresh(self):
        """
        Refreshes the instance from the database.

        Returns:
        - APIBase: The refreshed instance.

        Raises:
        - Exception: If an error occurs during the refresh.
        """
        try:
            db_instance = self.db_model.get_by_id(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            return self
        except Exception as e:
            raise e

class FileHandlerMixin(BaseModel):

    file_handler: ClassVar[MinioFileHandler] = MinioFileHandler()

    @classmethod
    def _preprocess_record(cls, record: dict) -> dict:
        """
        Preprocesses the record before inserting it into the database.

        Args:
        - record (dict): The record to preprocess.

        Returns:
        - dict: The preprocessed record.
        """
        record_data = None
        record_type = None

        for key, value in record.items():
            if key.endswith("_data"):
                record_data = value
                record_type = key.split("_")[0]
                break
        
        if not record_data:
            return record
        
        # Get Source Name
        source_name = record.get(f"{record_type}_name")

        if not source_name:
            raise ValueError(f"Source name not found for record {record}")
        
        file_path = record_data.get("file_path")
        file_key = cls._get_file_uri(file_path, record.get("collection_date"), record_type, source_name)
        if file_path:
            cls._upload_file(file_key=file_key, absolute_file_path=file_path)
            record_data = {
                "file_key": file_key,
                **record_data
            }
            record_data.pop("file_path")

        # Change the record_data field in record with the record_data
        record[f"{record_type}_data"] = record_data

        return record
    

    @classmethod
    def _postprocess_record(cls, record: dict) -> dict:
        """
        Postprocesses the record after retrieving it from the database.

        Args:
        - record (dict): The record to postprocess.

        Returns:
        - dict: The postprocessed record.
        """
        record_data = None
        record_type = None

        for key, value in record.items():
            if key.endswith("_data"):
                record_data = value
                record_type = key.split("_")[0]
                break

        if not record_data:
            return record
        
        # Get Source Name
        source_name = record.get(f"{record_type}_name")

        if not source_name:
            raise ValueError(f"Source name not found for record {record}")
        
        file_key = record_data.get("file_key")

        if file_key:
            file_url = cls._get_file_download_url(file_key)
            record_data = {
                "file_url": file_url,
                **record_data
            }
            record_data.pop("file_key")

        # Change the record_data field in record with the record_data
        record[f"{record_type}_data"] = record_data
        return record


    @classmethod
    def _upload_file(cls, file_key: str, absolute_file_path: str) -> str:
        """
        Uploads a file to the Minio server.

        Args:
        - absolute_file_path (str): The absolute path of the file to upload.

        Returns:
        - str: The URL of the uploaded file.
        """
        try:

            with open(absolute_file_path, "rb") as file:
                file_url = cls.file_handler.upload_file(
                    object_name=file_key,
                    data_stream=file
                )
                return file_url
    
        except Exception as e:
            raise e
        
    @classmethod
    def _download_file(cls, file_url: str, save_path: str) -> str:
        """
        Downloads a file from the Minio server.

        Args:
        - file_url (str): The URL of the file to download.
        - save_path (str): The path to save the downloaded file.

        Returns:
        - str: The path of the downloaded file.
        """
        try:
            file_path = cls.file_handler.download_file(file_url, save_path)
            return file_path
        except Exception as e:
            raise e
        
    
    @classmethod
    def _get_file_download_url(cls, file_key: str) -> str:
        """
        Gets the download URL for a file.

        Args:
        - file_key (str): The key of the file.

        Returns:
        - str: The download URL of the file.
        """
        try:
            file_url = cls.file_handler.get_download_url(file_key)
            return file_url
        except Exception as e:
            raise e
        
        
    
    @classmethod
    def _get_file_uri(cls, absolute_file_path: str, collection_date: str, record_type: str, source_name: str) -> str:
        """
        Generates the file URI for a given file path.

        Args:
        - absolute_file_path (str): The absolute path of the file.
        - record (dict): The record associated with the file.

        Returns:
        - str: The file URI.
        """

        if not os.path.exists(absolute_file_path):
            raise FileNotFoundError(f"File not found at path {absolute_file_path}")
        
        file_name = os.path.basename(absolute_file_path)
        collection_date = collection_date

        record_type_case = {
            "sensor": f"sensor_data/{collection_date}/{source_name}/{file_name}",
            "trait": f"trait_data/{collection_date}/{source_name}/{file_name}",
            "model": f"model_data/{collection_date}/{source_name}/{file_name}"
        }

        file_uri = record_type_case.get(record_type)
        return file_uri

