from typing import Optional, List, Generator
from gemini.api.base import APIBase, FileHandlerMixin, ID
from gemini.server.database.models import DatasetRecordModel, DatasetModel
from datetime import datetime, date
from rich.progress import track


class DatasetRecord(APIBase, FileHandlerMixin):
    """
    Represents a dataset record.

    Attributes:
        db_model (Type[DatasetRecordModel]): The database model associated with the dataset record.
        timestamp (Optional[datetime]): The timestamp of the record.
        collection_date (Optional[date]): The collection date of the record.
        dataset_id (Optional[ID]): The ID of the dataset.
        dataset_name (Optional[str]): The name of the dataset.
        dataset_data (Optional[dict]): The data associated with the dataset record.
        record_info (Optional[dict]): Additional information about the record.

    Methods:
        create(**kwargs): Creates a new dataset record.
        add(records: List['DatasetRecord']) -> bool: Adds multiple dataset records to the dataset.
        get(record_id: ID) -> 'DatasetRecord': Retrieves a dataset record by its ID.
        set_info(record_info: Optional[dict] = None) -> 'DatasetRecord': Sets the additional information for the record.
        get_info() -> dict: Retrieves the additional information for the record.
        add_info(record_info: Optional[dict] = None) -> 'DatasetRecord': Adds additional information to the record.
        remove_info(keys_to_remove: List[str]) -> 'DatasetRecord': Removes specific keys from the additional information of the record.
        search(**kwargs) -> Generator['DatasetRecord', None, None]: Searches for dataset records based on specified criteria.
        preprocess_record(record: dict) -> dict: Preprocesses the dataset record before insertion.
        postprocess_record(record: dict) -> dict: Postprocesses the dataset record after retrieval.
    """
    
    db_model = DatasetRecordModel

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id : Optional[ID] = None
    dataset_name : Optional[str] = None
    dataset_data: Optional[dict] = None
    record_info: Optional[dict] = None

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a new dataset record.

        Args:
            **kwargs: Additional keyword arguments to initialize the record.

        Returns:
            The created dataset record.
        """
        record = DatasetRecord.model_construct(
            _fields_set=DatasetRecord.model_fields_set,
            **kwargs
        )
        return record

    @classmethod
    def add(cls, records: List['DatasetRecord']) -> bool:
        """
        Adds multiple dataset records to the dataset.

        Args:
            records (List['DatasetRecord']): The list of dataset records to add.

        Returns:
            bool: True if the records were added successfully, False otherwise.
        """
        try:
            records_to_insert = []
            dataset_id = DatasetModel.get_or_create(dataset_name=records[0].dataset_name).id
            for record in track(records, description=f"Adding {len(records)} records to the dataset"):
                record_to_insert = {
                    'timestamp': record.timestamp,
                    'collection_date': record.timestamp.date(),
                    'dataset_id': dataset_id,
                    'dataset_name': record.dataset_name,
                    'dataset_data': record.dataset_data,
                    'record_info': record.record_info
                }
                records_to_insert.append(record_to_insert)

            # Preprocess records
            records_to_insert = [cls._preprocess_record(record) for record in records_to_insert]

            DatasetRecordModel.insert_bulk('dataset_records_unique', records_to_insert)
            return True
        except Exception as e:
            return False
        
    @classmethod
    def get(cls, record_id: ID) -> 'DatasetRecord':
        """
        Retrieves a dataset record by its ID.

        Args:
            record_id (ID): The ID of the record to retrieve.

        Returns:
            'DatasetRecord': The retrieved dataset record.
        """
        record = DatasetRecordModel.get_by_id(record_id)
        return record
    
    def set_info(self, record_info: Optional[dict] = None) -> 'DatasetRecord':
        """
        Sets the additional information for the record.

        Args:
            record_info (Optional[dict]): The additional information to set.

        Returns:
            'DatasetRecord': The updated dataset record.
        """
        self.update(record_info=record_info)
        return self
    
    def get_info(self) -> dict:
        """
        Retrieves the additional information for the record.

        Returns:
            dict: The additional information of the record.
        """
        self.refresh()
        return self.record_info
    
    def add_info(self, record_info: Optional[dict] = None) -> 'DatasetRecord':
        """
        Adds additional information to the record.

        Args:
            record_info (Optional[dict]): The additional information to add.

        Returns:
            'DatasetRecord': The updated dataset record.
        """
        current_info = self.record_info
        updated_info = {**current_info, **record_info}
        self.set_info(updated_info)
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> 'DatasetRecord':
        """
        Removes specific keys from the additional information of the record.

        Args:
            keys_to_remove (List[str]): The keys to remove from the additional information.

        Returns:
            'DatasetRecord': The updated dataset record.
        """
        current_info = self.record_info
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        return self
    
    @classmethod
    def search(cls, **kwargs) -> Generator['DatasetRecord', None, None]:
        """
        Searches for dataset records based on specified criteria.

        Args:
            **kwargs: Additional keyword arguments to filter the records.

        Yields:
            'DatasetRecord': The dataset records that match the search criteria.
        """
        records = DatasetRecordModel.stream(**kwargs)
        for record in records:
            record = record.to_dict()
            record = cls.postprocess_record(record)
            record = cls.model_construct(
                _fields_set=cls.model_fields_set,
                **record
            )
            yield record

