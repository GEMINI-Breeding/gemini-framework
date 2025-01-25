from typing import Optional, List, Generator

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.db.models.scripts import ScriptModel
from gemini.db.models.columnar.script_records import ScriptRecordModel

from datetime import date, datetime

class ScriptRecord(APIBase, FileHandlerMixin):

    id: Optional[ID] = Field(None, validation_alias=AliasChoices("id", "script_record_id"))

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_id: Optional[ID] = None
    dataset_name: Optional[str] = None
    script_id: Optional[ID] = None
    script_name: Optional[str] = None
    script_data: Optional[dict] = None
    record_info: Optional[dict] = None

    @classmethod
    def create(cls, **kwargs):
        try:
            record = ScriptRecord.model_construct(
                _fields_set=ScriptRecord.model_fields_set,
                **kwargs
            )
            return record
        except Exception as e:
            raise e
        
    @classmethod
    def add(cls, records: List['ScriptRecord']):
        pass

    @classmethod
    def get(cls, script_record_id: ID) -> 'ScriptRecord':
        try:
            db_instance = ScriptRecordModel.get(script_record_id)
            record = cls.model_validate(db_instance)
            return record
        except Exception as e:
            raise e

    @classmethod
    def search(cls, **kwargs) -> Generator['ScriptRecord', None, None]:
        try:
            records = ScriptRecordModel.stream(**kwargs)
            for record in records:
                record = cls.model_construct(
                    _fields_set=cls.model_fields_set,
                    **record.to_dict()
                )
                yield record
        except Exception as e:
            raise e