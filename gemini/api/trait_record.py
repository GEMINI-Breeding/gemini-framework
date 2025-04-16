from typing import Optional, List, Generator
from uuid import UUID
from tqdm import tqdm

from gemini.api.types import ID
from pydantic import Field, AliasChoices
from gemini.api.base import APIBase, FileHandlerMixin
from gemini.api.dataset import Dataset, GEMINIDatasetType
from gemini.api.plot import Plot
from gemini.db.models.traits import TraitModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.columnar.trait_records import TraitRecordModel
from gemini.db.models.views.trait_records_immv import TraitRecordsIMMVModel
from gemini.db.models.views.validation_views import ValidTraitDatasetCombinationsViewModel
from gemini.db.models.views.dataset_views import TraitDatasetsViewModel
from gemini.db.models.views.plot_view import PlotViewModel
from gemini.db.models.views.experiment_views import (
    ExperimentTraitsViewModel,
    ExperimentDatasetsViewModel,
    ExperimentSitesViewModel,
    ExperimentSeasonsViewModel,
)

from gemini.db.models.experiments import ExperimentModel
from gemini.db.models.datasets import DatasetModel
from gemini.db.models.associations import TraitDatasetModel

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
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    record_info: Optional[dict] = None

    @classmethod
    def exists(
        cls,
        timestamp: datetime,
        trait_name: str,
        dataset_name: str,
        experiment_name: str,
        site_name: str,
        season_name: str,
        plot_number: int,
        plot_row_number: int,
        plot_column_number: int,
    ) -> bool:
        try:
            exists = TraitRecordModel.exists(
                timestamp=timestamp,
                trait_name=trait_name,
                dataset_name=dataset_name,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number
            )
            return exists
        except Exception as e:
            raise e

    @classmethod
    def create(
        cls,
        timestamp: datetime = datetime.now(),
        collection_date: date = None,
        dataset_name: str = None,
        trait_name: str = None,
        trait_value: float = None,
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        record_info: dict = {}
    ) -> 'TraitRecord':
        try:
            if not trait_name:
                raise ValueError('Trait name is required')
            
            if not dataset_name:
                raise ValueError('Dataset name is required')
            
            if not experiment_name:
                raise ValueError('Experiment name is required')
            
            if not site_name:
                raise ValueError('Site name is required')
            
            if not season_name:
                raise ValueError('Season name is required')
            
            record = TraitRecord(
                timestamp=timestamp,
                collection_date=collection_date,
                dataset_name=dataset_name,
                trait_name=trait_name,
                trait_value=trait_value,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                record_info=record_info
            )

            return record
        except Exception as e:
            raise e

    @classmethod
    def add(cls, records: List['TraitRecord']) -> tuple[bool, List[str]]:
        try:
            records = cls._verify_records(records)
            records = [cls._preprocess_record(record) for record in tqdm(records, desc="Preprocessing Records for Trait: " + records[0].trait_name)]
            records_to_insert = []
            for record in records:
                record_to_insert = record.model_dump()
                record_to_insert = {k: v for k, v in record_to_insert.items() if v is not None}
                records_to_insert.append(record_to_insert)
            print(f"Inserting Records for Trait: {records[0].trait_name}")
            inserted_record_ids = TraitRecordModel.insert_bulk('trait_records_unique', records_to_insert)
            print(f"Inserted {len(inserted_record_ids)} Records for Trait: {records[0].trait_name}")
            return True, inserted_record_ids
        except Exception as e:
            return False, []


    def delete(self) -> bool:
        try:
            current_id = self.id
            trait_record = TraitRecordModel.get(current_id)
            TraitRecordModel.delete(trait_record)
            return True
        except Exception as e:
            return False

    @classmethod
    def get_all(cls, limit: int = 100) -> List['TraitRecord']:
        try:
            instances = TraitRecordModel.all(limit=limit)
            records = [cls.model_validate(instance) for instance in instances]
            return records if records else None
        except Exception as e:
            raise e

    @classmethod
    def get_by_id(cls, id: UUID | int | str) -> 'TraitRecord':
        try:
            record = TraitRecordModel.get(id)
            record = cls.model_construct(
                _fields_set=cls.model_fields_set,
                **record.to_dict()
            )
            record = record.model_dump()
            # record = cls._postprocess_record(record)
            record = cls.model_validate(record)
            return record
        except Exception as e:
            raise e

    def refresh(self) -> 'TraitRecord':
        try:
            db_instance = TraitRecordModel.get(self.id)
            instance = self.model_construct(
                _fields_set=self.model_fields_set,
                **db_instance.to_dict()
            )
            for key, value in instance.model_dump().items():
                if hasattr(self, key) and key != 'id':
                    setattr(self, key, value)
            return self
        except Exception as e:
            raise e


    def update(
        self,
        trait_value: float = None,
        record_info: dict = None
    ) -> 'TraitRecord':
        try:
            if not trait_value and not record_info:
                raise ValueError('At least one parameter must be provided.')
            current_id = self.id
            trait_record = TraitRecordModel.get(current_id)
            trait_record = TraitRecordModel.update(
                trait_record,
                trait_value=trait_value,
                record_info=record_info
            )
            trait_record = self.model_validate(trait_record)
            self.refresh()
            return trait_record
        except Exception as e:
            raise e


    @classmethod
    def get(cls, trait_record_id: ID) -> 'TraitRecord':
        try:
            db_instance = TraitRecordModel.get(trait_record_id)
            record = cls.model_validate(db_instance)
            return record if record else None
        except Exception as e:
            raise e
        
    def get_record_info(self) -> dict:
        try:
            if not self.id:
                raise ValueError('Record ID is required.')
            record = TraitRecordModel.get(self.id)
            record_info = record.record_info
            return record_info if record_info else None
        except Exception as e:
            raise e
        
    def set_record_info(self, record_info: dict) -> dict:
        try:
            if not self.id:
                raise ValueError('Record ID is required.')
            record = TraitRecordModel.get(self.id)
            record = TraitRecordModel.update(record, record_info=record_info)
            self.refresh()
            return record
        except Exception as e:
            raise e
        
    @classmethod
    def search(
        cls,
        dataset_name: str = None,
        trait_name: str = None,
        trait_value: float = None,
        experiment_name: str = None,
        site_name: str = None,
        season_name: str = None,
        plot_number: int = None,
        plot_row_number: int = None,
        plot_column_number: int = None,
        collection_date: date = None,
        record_info: dict = None
    ) -> Generator['TraitRecord', None, None]:
        try:
            if not any([dataset_name, trait_name, trait_value, experiment_name, site_name, season_name, plot_number, plot_row_number, plot_column_number, collection_date, record_info]):
                raise ValueError('At least one search parameter must be provided.')
            
            records = TraitRecordsIMMVModel.stream(
                dataset_name=dataset_name,
                trait_name=trait_name,
                trait_value=trait_value,
                experiment_name=experiment_name,
                site_name=site_name,
                season_name=season_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                collection_date=collection_date,
                record_info=record_info
            )

            for record in records:
                record = cls.model_construct(
                    _fields_set=cls.model_fields_set,
                    **record.to_dict()
                )
                record = record.model_dump()
                # record = cls._postprocess_record(record)
                record = cls.model_validate(record)
                yield record
        except Exception as e:
            raise e
        
    def set_experiment(self, experiment_name: str) -> "TraitRecord":
        try:
            record = TraitRecordModel.get(self.id)
            experiment = ExperimentModel.get_or_create(experiment_name=experiment_name)
            record = TraitRecordModel.update(record, experiment_id=experiment.id, experiment_name=experiment_name)
            self.refresh()
            return self
        except Exception as e:
            raise e
        
    def set_season(self, season_name: str) -> "TraitRecord":
        try:
            record = TraitRecordModel.get(self.id)
            experiment = ExperimentModel.get(record.experiment_id)
            season = ExperimentSeasonsViewModel.get_by_parameters(
                experiment_id=experiment.id,
                season_name=season_name
            )
            TraitRecordModel.update(record, season_id=season.season_id, season_name=season_name)
            self.refresh()
            return self
        except Exception as e:
            raise e
        
    def set_site(self, site_name: str) -> "TraitRecord":
        try:
            record = TraitRecordModel.get(self.id)
            experiment = ExperimentModel.get(record.experiment_id)
            site = ExperimentSitesViewModel.get_by_parameters(
                experiment_id=experiment.id,
                site_name=site_name
            )
            TraitRecordModel.update(record, site_id=site.site_id, site_name=site_name)
            self.refresh()
            return self
        except Exception as e:
            raise e
        
    def set_plot(self, plot_number: int, plot_row_number: int, plot_column_number: int) -> "TraitRecord":
        try:
            record = TraitRecordModel.get(self.id)
            plot = PlotViewModel.get_by_parameters(
                experiment_id=record.experiment_id,
                site_id=record.site_id,
                season_id=record.season_id,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number
            )
            TraitRecordModel.update(record, plot_id=plot.plot_id, plot_number=plot_number, plot_row_number=plot_row_number, plot_column_number=plot_column_number)
            self.refresh()
            return self
        except Exception as e:
            raise e
        

    @classmethod
    def get_valid_combinations(
        cls,
        experiment_name: str = None,
        dataset_name: str = None,
        trait_name: str = None,
        site_name: str = None,
        season_name: str = None
    ) -> List[dict]:
        try:
            valid_combinations = ValidTraitDatasetCombinationsViewModel.search(
                experiment_name=experiment_name,
                dataset_name=dataset_name,
                trait_name=trait_name,
                site_name=site_name,
                season_name=season_name
            )
            valid_combinations = [record.to_dict() for record in valid_combinations]
            return valid_combinations if valid_combinations else None
        except Exception as e:
            raise e


    @classmethod
    def _verify_records(cls, records: List['TraitRecord']) -> List['TraitRecord']:
        try:

            # Refresh all the views
            ExperimentTraitsViewModel.refresh()
            ExperimentDatasetsViewModel.refresh()
            ExperimentSitesViewModel.refresh()
            ExperimentSeasonsViewModel.refresh()
            PlotViewModel.refresh()

            # Verify the records
            trait = None
            datasets = {}
            experiments = {}
            sites = {}
            seasons = {}

            for record in records:
                if not record.timestamp:
                    raise ValueError("Timestamp is required.")
                if not record.collection_date:
                    record.collection_date = record.timestamp.date()

                if trait and record.trait_name != trait.trait_name:
                    raise ValueError("All records must have the same trait name.")
                
                if not trait and TraitModel.exists(trait_name=record.trait_name):
                    trait = TraitModel.get_by_parameters(trait_name=record.trait_name)

                record.trait_id = trait.id

                if record.dataset_name not in datasets:
                    if DatasetModel.exists(dataset_name=record.dataset_name):
                        datasets[record.dataset_name] = DatasetModel.get_by_parameters(dataset_name=record.dataset_name)
                    else:
                        created_dataset = Dataset.create(
                            dataset_name=record.dataset_name,
                            experiment_name=record.experiment_name,
                            dataset_type=GEMINIDatasetType.Trait
                        )
                        TraitDatasetModel.get_or_create(
                            dataset_id=created_dataset.id,
                            trait_id=trait.id
                        )
                        ExperimentDatasetsViewModel.refresh()
                        TraitDatasetsViewModel.refresh()
                        datasets[record.dataset_name] = DatasetModel.get_by_parameters(dataset_name=created_dataset.dataset_name)

                record.dataset_id = datasets[record.dataset_name].id

                if record.experiment_name not in experiments and ExperimentDatasetsViewModel.exists(experiment_name=record.experiment_name, dataset_name=record.dataset_name):
                    experiments[record.experiment_name] = ExperimentDatasetsViewModel.get_by_parameters(experiment_name=record.experiment_name, dataset_name=record.dataset_name)
        
                record.experiment_id = experiments[record.experiment_name].experiment_id

                if record.site_name not in sites and ExperimentSitesViewModel.exists(experiment_id=record.experiment_id, site_name=record.site_name):
                    sites[record.site_name] = ExperimentSitesViewModel.get_by_parameters(experiment_id=record.experiment_id, site_name=record.site_name)

                record.site_id = sites[record.site_name].site_id

                if record.season_name not in seasons and ExperimentSeasonsViewModel.exists(experiment_id=record.experiment_id, season_name=record.season_name):
                    seasons[record.season_name] = ExperimentSeasonsViewModel.get_by_parameters(experiment_id=record.experiment_id, season_name=record.season_name)

                record.season_id = seasons[record.season_name].season_id

                if record.plot_number and record.plot_row_number and record.plot_column_number:
                    plot = PlotViewModel.get_by_parameters(
                        experiment_id=record.experiment_id,
                        site_id=record.site_id,
                        season_id=record.season_id,
                        plot_number=record.plot_number,
                        plot_row_number=record.plot_row_number,
                        plot_column_number=record.plot_column_number
                    )
                    record.plot_id = plot.plot_id if plot else None
                    if not plot:
                        plot = Plot.create(
                            experiment_name=record.experiment_name,
                            site_name=record.site_name,
                            season_name=record.season_name,
                            plot_number=record.plot_number,
                            plot_row_number=record.plot_row_number,
                            plot_column_number=record.plot_column_number
                        )
                        record.plot_id = plot.id
            return records
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
        
        