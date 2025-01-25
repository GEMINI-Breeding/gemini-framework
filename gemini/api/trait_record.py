from typing import Optional, List, Generator

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.db.models.traits import TraitModel
from gemini.db.models.columnar.trait_records import TraitRecordModel

from datetime import date, datetime

class TraitRecord(APIBase, FileHandlerMixin):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "trait_record_id"))

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[ID] = None
    dataset_name: Optional[str] = None
    trait_id: Optional[ID] = None
    trait_name: Optional[str] = None
    trait_value: Optional[float] = None
    record_info: Optional[dict] = None

    @classmethod
    def create(cls, **kwargs):
        try:
            record = TraitRecord.model_construct(
                _fields_set=TraitRecord.model_fields_set,
                **kwargs
            )
            return record
        except Exception as e:
            raise e
        
    @classmethod
    def add(cls, records: List['TraitRecord']):
        pass

    @classmethod
    def get(cls, trait_record_id: ID) -> 'TraitRecord':
        try:
            db_instance = TraitRecordModel.get(trait_record_id)
            record = cls.model_validate(db_instance)
            return record
        except Exception as e:
            raise e
        
    @classmethod
    def search(cls, **kwargs) -> Generator['TraitRecord', None, None]:
        try:
            records = TraitRecordModel.stream(**kwargs)
            for record in records:
                record = cls.model_construct(
                    _fields_set=cls.model_fields_set,
                    **record.to_dict()
                )
                yield record
        except Exception as e:
            raise e
        
        