from typing import Optional, List, Generator

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.db.models.traits import TraitModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.columnar.trait_records import TraitRecordModel
from gemini.db.models.views.trait_records_immv import TraitRecordsIMMVModel

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
    experiment_id: Optional[ID] = None
    experiment_name : Optional[str] = None
    season_id: Optional[ID] = None
    season_name: Optional[str] = None
    site_id: Optional[ID] = None
    site_name: Optional[str] = None
    plot_id: Optional[ID] = None
    plot_number: Optional[str] = None
    plot_row_number: Optional[str] = None
    plot_column_number: Optional[str] = None
    record_info: Optional[dict] = None

    @classmethod
    def create(
        cls, 
        timestamp: datetime = datetime.now(),
        collection_date: date = date.today(),
        dataset_id: ID = None,
        dataset_name: str = None,
        trait_id: ID = None,
        trait_name: str = None,
        trait_value: float = None,
        experiment_id: ID = None,
        experiment_name: str = 'Default',
        site_id: ID = None,
        site_name: str = 'Default',
        season_id: ID = None,
        season_name: str = 'Default',
        plot_id: ID = None,
        plot_number: str = 'Default',
        plot_row_number: str = 'Default',
        plot_column_number: str = 'Default',
        record_info: dict = {}
    ) -> 'TraitRecord':
        try:
            record = TraitRecord.model_construct(
                _fields_set=TraitRecord.model_fields_set,
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_id=dataset_id,
                dataset_name=dataset_name,
                trait_id=trait_id,
                trait_name=trait_name,
                trait_value=trait_value,
                experiment_id=experiment_id,
                experiment_name=experiment_name,
                site_id=site_id,
                site_name=site_name,
                season_id=season_id,
                season_name=season_name,
                plot_id=plot_id,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                record_info=record_info
            )
            return record
        except Exception as e:
            raise e
        
    @classmethod
    def add(cls, records: List['TraitRecord']):
        try:
            records_to_insert = []
            dataset_id = DatasetModel.get_or_create(dataset_name=records[0].dataset_name).id
            records = [cls._preprocess_record(record) for record in records]
            for record in records:
                record_to_insert = {
                    'timestamp': record.timestamp,
                    'collection_date': record.timestamp.date(),
                    'dataset_id': dataset_id,
                    'dataset_name': record.dataset_name,
                    'trait_id': record.trait_id,
                    'trait_name': record.trait_name,
                    'trait_value': record.trait_value,
                    'experiment_id': record.experiment_id,
                    'experiment_name': record.experiment_name,
                    'site_id': record.site_id,
                    'site_name': record.site_name,
                    'season_id': record.season_id,
                    'season_name': record.season_name,
                    'plot_id': record.plot_id,
                    'plot_number': record.plot_number,
                    'plot_row_number': record.plot_row_number,
                    'plot_column_number': record.plot_column_number,
                    'record_info': record.record_info
                }
                records_to_insert.append(record_to_insert)
            TraitRecordModel.insert_bulk('trait_records_unique', records_to_insert)
            return True
        except Exception as e:
            return False


    @classmethod
    def delete(self):
        # Implement the delete method
        pass

    @classmethod
    def get_all(cls):
        # Implement the get_all method
        pass

    @classmethod
    def get_by_id(cls, id):
        # Implement the get_by_id method
        pass

    def refresh(self):
        # Implement the refresh method
        pass

    def update(self, **kwargs):
        # Implement the update method
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
            records = TraitRecordsIMMVModel.stream(**kwargs)
            for record in records:
                record = cls.model_construct(
                    _fields_set=cls.model_fields_set,
                    **record.to_dict()
                )
                yield record
        except Exception as e:
            raise e
        

    @classmethod
    def _preprocess_record(cls, record: 'TraitRecord') -> 'TraitRecord':
        try:
            return record
        except Exception as e:
            raise e
        
    @classmethod
    def _postprocess_record(cls, record: dict) -> dict:
        try:
            return record
        except Exception as e:
            raise e
        
    @classmethod
    def _upload_file(cls, file_key: str, absolute_file_path: str) -> str:
        pass
        
    def _download_file(self, output_folder: str) -> str:
        pass
        
    def _get_file_download_url(self, record_file_key: str) -> str:
        pass
        
    @classmethod
    def _create_file_uri(cls, record: 'TraitRecord') -> str:
        pass
        
        