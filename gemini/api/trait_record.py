from typing import Optional, List, Any, Generator
from gemini.api.base import APIBase
from gemini.models import TraitRecordModel, TraitModel, DatasetModel
from gemini.logger import logger_service

from datetime import datetime, date
from uuid import UUID


class TraitRecord(APIBase):

    db_model = TraitRecordModel

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_name: Optional[str] = None
    trait_name: Optional[str] = None
    trait_value: Optional[float] = None
    record_info: Optional[dict] = None


    @classmethod
    def create(cls, **kwargs) -> 'TraitRecord':
        record = cls.model_construct(
            _fields_set=cls.model_fields_set,
            **kwargs
        )
        return record

    @classmethod
    def add(cls, records: List['TraitRecord']) -> bool:
        try:
            records_to_insert = []
            dataset_id = DatasetModel.get_by_parameters(dataset_name=records[0].dataset_name).id
            trait_id = TraitModel.get_or_create(trait_name=records[0].trait_name).id
            for record in records:
                record_to_add = {}
                record_to_add['timestamp'] = record.timestamp
                record_to_add['collection_date'] = record.collection_date
                record_to_add['dataset_id'] = dataset_id
                record_to_add['dataset_name'] = record.dataset_name
                record_to_add['trait_id'] = trait_id
                record_to_add['trait_name'] = record.trait_name
                record_to_add['trait_value'] = record.trait_value
                record_to_add['record_info'] = record.record_info
                records_to_insert.append(record_to_add)
            cls.db_model.insert_bulk("trait_records_unique", records_to_insert)
            logger_service.info(
                "API",
                f"Added {len(records)} trait records to the database",
            )
            return True
        except Exception as e:
            logger_service.error(
                "API",
                f"Failed to add trait records to the database",
            )
            return False
        
    @classmethod
    def get(cls, record_id: UUID) -> 'TraitRecord':
        record = cls.db_model.get_by_id(record_id)
        return cls.model_validate(record)
    
    def get_info(self) -> dict:
        self.refresh()
        logger_service.info(
            "API",
            f"Getting information of the record with id {self.id}",
        )
        return self.record_info

    def set_info(self, record_info: dict) -> 'TraitRecord':
        self.update(record_info=record_info)
        logger_service.info(
            "API",
            f"Set information of the record with id {self.id}",
        )
        return self
    
    def add_info(self, record_info: dict) -> 'TraitRecord':
        current_info = self.get_info()
        updated_info = {**current_info, **record_info}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Added information to the record with id {self.id}",
        )
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> 'TraitRecord':
        current_info = self.get_info()
        updated_info = {key: value for key, value in current_info.items() if key not in keys_to_remove}
        self.set_info(updated_info)
        logger_service.info(
            "API",
            f"Removed information from the record with id {self.id}",
        )
        return self
    
    @classmethod
    def search(cls, **kwargs) -> Generator['TraitRecord', None, None]:
        searched_records = cls.db_model.stream(**kwargs)
        for record in searched_records:
            record = record.to_dict()
            record = cls.model_construct(
                _fields_set=cls.model_fields_set,
                **record
            )
            yield record
