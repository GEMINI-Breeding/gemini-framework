from typing import Optional, List, Generator
from gemini.api.base import APIBase, ID, FileHandlerMixin
from gemini.server.database.models import SensorRecordModel, SensorModel, DatasetModel, SensorRecordsIMMVModel
from datetime import datetime, date
from rich.progress import track


class SensorRecord(APIBase, FileHandlerMixin):

    db_model = SensorRecordModel

    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    dataset_name: Optional[str] = None
    dataset_id: Optional[ID] = None
    sensor_name: Optional[str] = None
    sensor_id: Optional[ID] = None
    sensor_data: Optional[dict] = None
    record_info: Optional[dict] = None

    
    @classmethod
    def create(cls, **kwargs) -> 'SensorRecord':
        record = SensorRecord.model_construct(
            _fields_set=SensorRecord.model_fields_set,
            **kwargs
        )
        return record

    @classmethod
    def add(cls, records: List['SensorRecord']) -> bool:
        try:
            records_to_insert = []
            sensor_id = SensorModel.get_by_parameters(sensor_name=records[0].sensor_name).id
            dataset_id = DatasetModel.get_by_parameters(dataset_name=records[0].dataset_name).id
            for record in track(records, description="Adding sensor records"):
                record_to_insert = {
                    'timestamp': record.timestamp,
                    'collection_date': record.collection_date,
                    'dataset_id': dataset_id,
                    'dataset_name': record.dataset_name,
                    'sensor_id': sensor_id,
                    'sensor_name': record.sensor_name,
                    'sensor_data': record.sensor_data,
                    'record_info': record.record_info
                }
                
                records_to_insert.append(record_to_insert)
            # Preprocess records
            records_to_insert = [cls._preprocess_record(record) for record in records_to_insert]
            SensorRecordModel.insert_bulk("sensor_records_unique", records_to_insert)
            return True
        except Exception as e:
            print(e)
            return False
        
    @classmethod
    def get(cls, record_id: ID) -> 'SensorRecord':
        record = cls.db_model.get_by_id(record_id)
        record = record.to_dict()
        record = cls._postprocess_record(record)
        record = cls.model_construct(
            _fields_set=cls.model_fields_set,
            **record
        )
        return cls.model_validate(record)
    
    @classmethod
    def get_by_id(cls, record_id: ID) -> 'SensorRecord':
        record = cls.db_model.get_by_id(record_id)
        record = record.to_dict()
        record = cls._postprocess_record(record)
        record = cls.model_construct(
            _fields_set=cls.model_fields_set,
            **record
        )
        return record
    
    def get_info(self) -> dict:
        self.refresh()
        return self.record_info
    
    def set_info(self, record_info: Optional[dict] = None) -> 'SensorRecord':
        self.update(record_info=record_info)
        return self
    
    def add_info(self, record_info: Optional[dict] = None) -> 'SensorRecord':
        current_info = self.get_info()
        updated_info = {**current_info, **record_info}
        self.set_info(updated_info)
        return self
    
    def remove_info(self, keys_to_remove: List[str]) -> 'SensorRecord':
        current_info = self.get_info()
        updated_info = {k: v for k, v in current_info.items() if k not in keys_to_remove}
        self.set_info(updated_info)
        return self
    
    @classmethod
    def search(cls, local: bool = False, **kwargs) -> Generator['SensorRecord', None, None]:
        for record in SensorRecordsIMMVModel.stream(**kwargs):
            record = record.to_dict()
            record = cls._postprocess_record(record)
            record = cls.model_construct(
                _fields_set=cls.model_fields_set,
                **record
            )
            yield record


