from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import model_validator
from typing import Any, Optional, Union, ClassVar
from uuid import UUID
from abc import abstractmethod

from gemini.models.base_model import BaseModel as DBBaseModel
from gemini.models.columnar.columnar_base_model import ColumnarBaseModel
from gemini.models.views.view_base import ViewBaseModel
from gemini.logger import logger_service


class APIBase(BaseModel):
    """
    Base class for all API classes
    """
    db_model: ClassVar[DBBaseModel] = None
    model_config = ConfigDict(
        from_attributes=True, 
        arbitrary_types_allowed=True,
        protected_namespaces=(),
        extra="allow"
    )

    id: Optional[Union[UUID, int, str]] = None

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
        Create a new instance of the class and add it to the database.

        Args:
        **kwargs: The fields of the instance

        Returns:
        APIBase: The created instance
        """
        try:
            db_instance = cls.db_model.get_or_create(**kwargs)
            instance = cls.model_validate(db_instance)
            logger_service.info(
                "API",
                f"Created a new instance of {cls.__name__} with id {instance.id} in the database",
            )
            return instance
        except Exception as e:
            logger_service.error(
                "API",
                f"Failed to create a new instance of {cls.__name__} in the database: {str(e)}",
            )
            raise e

    @classmethod
    def get_by_id(cls, id: Union[UUID, int, str]) -> "APIBase":
        """
        Get an instance of the class by ID.

        Args:
        id (Union[int, UUID, str]): The ID of the instance

        Returns:
        APIBase: The instance with the given ID
        """
        try:
            instance_from_db = cls.db_model.get_by_id(id)
            instance = cls.model_validate(instance_from_db)
            logger_service.info(
                "API",
                f"Retrieved the instance of {cls.__name__} with id {id} from the database",
            )
            return instance
        except Exception as e:
            logger_service.error(
                "API",
                f"Failed to retrieve the instance of {cls.__name__} with id {id} from the database: {str(e)}",
            )
            raise e


    @classmethod
    def all(cls):
        """
        Get all instances of the class from the database.

        Returns:
        List[APIBase]: A list of all the instances of the class
        """
        try:
            db_instances = cls.db_model.get_all()
            instances = [cls.model_validate(instance) for instance in db_instances]
            logger_service.info(
                "API",
                f"Retrieved {len(instances)} instances of {cls.__name__} from the database",
            )
            return instances
        except Exception as e:
            logger_service.error(
                "API",
                f"Failed to retrieve all instances of {cls.__name__} from the database: {str(e)}",
            )
            raise e

    @classmethod
    def search(cls, **search_parameters):
        """
        Search for instances of the class in the database.

        Args:
        **search_parameters: The search parameters

        Returns:
        List[APIBase]: A list of the instances that match the search parameters
        """
        try:
            db_instances = cls.db_model.search(**search_parameters)
            instances = [cls.model_validate(instance) for instance in db_instances]
            logger_service.info(
                "API",
                f"Retrieved {len(instances)} instances of {cls.__name__} from the database",
            )
            return instances
        except Exception as e:
            logger_service.error(
                "API",
                f"Failed to search for instances of {cls.__name__} in the database: {str(e)}",
            )
            raise e


    def update(self, **kwargs):
        """
        Update the instance in the database.

        Args:
        **kwargs: The fields to update

        Returns:
        APIBase: The updated instance
        """
        try:
            db_instance = self.db_model.get_by_id(self.id)
            db_instance = self.db_model.update(db_instance, **kwargs)
            instance = self.model_validate(db_instance)
            logger_service.info(
                "API",
                f"Updated the instance of {self.__class__.__name__} with id {self.id} in the database",
            )
            self.refresh()
            return instance
        except Exception as e:
            logger_service.error(
                "API",
                f"Failed to update the instance of {self.__class__.__name__} with id {self.id} in the database: {str(e)}",
            )
            raise e

    

    def delete(self):
        """
        Delete the instance from the database.

        Returns:
        bool: True if the instance was deleted, False otherwise
        """
        try:
            db_instance = self.db_model.get_by_id(self.id)
            is_deleted = self.db_model.delete(db_instance)
            if not is_deleted:
                raise Exception("Failed to delete the instance from the database")
            logger_service.info(
                "API",
                f"Deleted the instance of {self.__class__.__name__} with id {self.id} from the database",
            )
            return is_deleted
        except Exception as e:
            logger_service.error(
                "API",
                f"Failed to delete the instance of {self.__class__.__name__} with id {self.id} from the database: {str(e)}",
            )
            raise e
        
    def refresh(self):
        """
        Refresh the instance from the database.

        Returns:
        APIBase: The refreshed instance
        """
        try:
            db_instance = self.db_model.get_by_id(self.id)
            instance = self.model_validate(db_instance)
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != "id":
                    actual_value = getattr(instance, key)
                    setattr(self, key, actual_value)
            logger_service.info(
                "API",
                f"Refreshed the instance of {self.__class__.__name__} with id {self.id} from the database",
            )
            return self
        except Exception as e:
            logger_service.error(
                "API",
                f"Failed to refresh the instance of {self.__class__.__name__} with id {self.id} from the database: {str(e)}",
            )
            raise e
