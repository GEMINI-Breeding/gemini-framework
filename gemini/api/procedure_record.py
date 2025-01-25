from typing import Optional, List, Generator

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.db.models.models import ModelModel
from gemini.db.models.columnar.model_records import ModelRecordModel

from datetime import date, datetime

class ModelRecord(APIBase, FileHandlerMixin):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "model_record_id"))

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[ID] = None
    dataset_name: Optional[str] = None
    procedure_id: Optional[ID] = None
    procedure_name: Optional[str] = None
    procedure_data: Optional[dict] = None
    record_info: Optional[dict] = None

    @classmethod
    def create(cls, **kwargs):
        try:
            record = ModelRecord.model_construct(
                _fields_set=ModelRecord.model_fields_set,
                **kwargs
            )
            return record
        except Exception as e:
            raise e
        

    @classmethod
    def add(cls, records: List['ModelRecord']):
        pass

    @classmethod
    def get(cls, model_record_id: ID) -> 'ModelRecord':
        try:
            db_instance = ModelRecordModel.get(model_record_id)
            record = cls.model_validate(db_instance)
            return record
        except Exception as e:
            raise e
        

    @classmethod
    def search(cls, **kwargs) -> Generator['ModelRecord', None, None]:
        try:
            records = ModelRecordModel.stream(**kwargs)
            for record in records:
                record = cls.model_construct(
                    _fields_set=cls.model_fields_set,
                    **record.to_dict()
                )
                yield record
        except Exception as e:
            raise e