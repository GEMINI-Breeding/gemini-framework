from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller
from litestar.response import Stream
from litestar.serialization import encode_json
from litestar.enums import RequestEncodingType


from collections.abc import AsyncGenerator, Generator

from gemini.api.dataset import Dataset
from gemini.api.dataset_record import DatasetRecord
from gemini.api.enums import GEMINIDatasetType
from gemini.rest_api.models import ( 
    DatasetInput, 
    DatasetOutput, 
    RESTAPIError, 
    DatasetUpdate, 
    str_to_dict, 
    JSONB
)
from gemini.rest_api.models import (
    DatasetRecordInput,
    DatasetRecordOutput,
    DatasetRecordUpdate,
    DatasetRecordSearch
)

from gemini.rest_api.file_handler import api_file_handler

from typing import List, Annotated, Optional


async def dataset_records_bytes_generator(dataset_record_generator: Generator[DatasetOutput, None, None]) -> AsyncGenerator[bytes, None]:
    for record in dataset_record_generator:
        record = record.model_dump(exclude_none=True)
        record = encode_json(record) + b'\n'
        yield record


class DatasetController(Controller):

    # Get All Datasets
    @get(path="/all")
    async def get_all_datasets(self) -> List[DatasetOutput]:
        try:
            datasets = Dataset.get_all()
            if datasets is None:
                error_html = RESTAPIError(
                    error="No datasets found",
                    error_description="No datasets were found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return datasets
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving all datasets"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

    # Get Datasets
    @get()
    async def get_datasets(
        self,
        dataset_name: Optional[str] = None,
        dataset_info: Optional[JSONB] = None,
        dataset_type_id: Optional[int] = None,
        experiment_name: Optional[str] = 'Experiment A',
        collection_date: Optional[str] = None
    ) -> List[DatasetOutput]:
        try:
            if dataset_info is not None:
                dataset_info = str_to_dict(dataset_info)

            datasets = Dataset.search(
                dataset_name=dataset_name,
                dataset_info=dataset_info,
                dataset_type=GEMINIDatasetType(dataset_type_id) if dataset_type_id else None,
                experiment_name=experiment_name,
                collection_date=collection_date
            )
            if datasets is None:
                error_html = RESTAPIError(
                    error="No datasets found",
                    error_description="No datasets were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return datasets
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving datasets"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Dataset by ID
    @get(path="/id/{dataset_id:str}")
    async def get_dataset_by_id(
        self, dataset_id: str
    ) -> DatasetOutput:
        try:
            dataset = Dataset.get_by_id(id=dataset_id)
            if dataset is None:
                error_html = RESTAPIError(
                    error="Dataset not found",
                    error_description="No dataset was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return dataset
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the dataset"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Create Dataset
    @post()
    async def create_dataset(
        self, data: Annotated[DatasetInput, Body]
    ) -> DatasetOutput:
        try:
            dataset = Dataset.create(
                collection_date=data.collection_date,
                dataset_name=data.dataset_name,
                dataset_info=data.dataset_info,
                dataset_type=GEMINIDatasetType(data.dataset_type_id),
                experiment_name=data.experiment_name
            )
            if dataset is None:
                error_html = RESTAPIError(
                    error="Dataset not created",
                    error_description="The dataset was not created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return dataset
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the dataset"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Update Dataset
    @patch(path="/id/{dataset_id:str}")
    async def update_dataset(
        self, dataset_id: str, data: Annotated[DatasetUpdate, Body]
    ) -> DatasetOutput:
        try:
            dataset = Dataset.get_by_id(id=dataset_id)
            if dataset is None:
                error_html = RESTAPIError(
                    error="Dataset not found",
                    error_description="No dataset was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            
            dataset = dataset.update(
                collection_date=data.collection_date,
                dataset_name=data.dataset_name,
                dataset_info=data.dataset_info,
                dataset_type=GEMINIDatasetType(data.dataset_type_id) if data.dataset_type_id else None,
            )
            if dataset is None:
                error_html = RESTAPIError(
                    error="Dataset not updated",
                    error_description="The dataset could not be updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return dataset
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the dataset"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Delete Dataset
    @delete(path="/id/{dataset_id:str}")
    async def delete_dataset(
        self, dataset_id: str
    ) -> None:
        try:
            dataset = Dataset.get_by_id(id=dataset_id)
            if dataset is None:
                error_html = RESTAPIError(
                    error="Dataset not found",
                    error_description="No dataset was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = dataset.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Dataset not deleted",
                    error_description="The dataset could not be deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the dataset"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Add a Dataset Record
    @post(path="/id/{dataset_id:str}/records")
    async def add_dataset_record(
        self,
        dataset_id: str,
        data: Annotated[DatasetRecordInput, Body(media_type=RequestEncodingType.MULTI_PART)]
    ) -> DatasetRecordOutput:
        try:
            dataset = Dataset.get_by_id(id=dataset_id)
            if dataset is None:
                error_html = RESTAPIError(
                    error="Dataset not found",
                    error_description="No dataset was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            
            if data.record_file:
                record_file_path = await api_file_handler.create_file(data.record_file)
            
            add_success, inserted_record_ids = dataset.add_record(
                timestamp=data.timestamp,
                collection_date=data.collection_date,
                dataset_data=data.dataset_data,
                experiment_name=data.experiment_name,
                season_name=data.season_name,
                site_name=data.site_name,
                record_file=record_file_path if data.record_file else None,
                record_info=data.record_info
            )
            if not add_success:
                error_html = RESTAPIError(
                    error="Dataset record not added",
                    error_description="The dataset record was not added"
                ).to_html()
                return Response(content=error_html, status_code=500)
            inserted_record_id = inserted_record_ids[0]
            inserted_dataset_record = DatasetRecord.get_by_id(id=inserted_record_id)
            if inserted_dataset_record is None:
                error_html = RESTAPIError(
                    error="Dataset record not found",
                    error_description="The dataset record was not found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return inserted_dataset_record
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while adding the dataset record"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)


    # Search Dataset Records
    @get(path="/id/{dataset_id:str}/records")
    async def search_dataset_records(
        self,
        dataset_id: str,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        collection_date: Optional[str] = None
    ) -> Stream:
        try:
            dataset = Dataset.get_by_id(id=dataset_id)
            if dataset is None:
                error_html = RESTAPIError(
                    error="Dataset not found",
                    error_description="No dataset was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            records = dataset.get_records(
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                collection_date=collection_date
            )
            return Stream(dataset_records_bytes_generator(records), media_type="application/ndjson")
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving dataset records"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
    

    # Get Dataset Record by ID
    @get(path="/records/id/{record_id:str}")
    async def get_dataset_record_by_id(
        self, record_id: str
    ) -> DatasetRecordOutput:
        try:
            dataset_record = DatasetRecord.get_by_id(id=record_id)
            if dataset_record is None:
                error_html = RESTAPIError(
                    error="Dataset record not found",
                    error_description="No dataset record was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return dataset_record
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the dataset record"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    # Download Dataset Record by ID
    @get(path="/records/id/{record_id:str}/download")
    async def download_dataset_record_by_id(
        self, record_id: str
    ) -> DatasetRecordOutput:
        try:
            dataset_record = DatasetRecord.get_by_id(id=record_id)
            if dataset_record is None:
                error_html = RESTAPIError(
                    error="Dataset record not found",
                    error_description="No dataset record was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            record_file = dataset_record.record_file
            if record_file is None:
                error_html = RESTAPIError(
                    error="Dataset record file not found",
                    error_description="No dataset record file was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            # Redirect to link in record_file
            return Response(content=record_file, status_code=302)
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the dataset record file"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

    # Update Dataset Record
    @patch(path="/records/id/{record_id:str}")
    async def update_dataset_record(
        self, record_id: str, data: Annotated[DatasetRecordUpdate, Body]
    ) -> DatasetRecordOutput:
        try:
            dataset_record = DatasetRecord.get_by_id(id=record_id)
            if dataset_record is None:
                error_html = RESTAPIError(
                    error="Dataset record not found",
                    error_description="No dataset record was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            
            dataset_record = dataset_record.update(
                dataset_data=data.dataset_data,
                record_info=data.record_info,
            )
            if dataset_record is None:
                error_html = RESTAPIError(
                    error="Dataset record not updated",
                    error_description="The dataset record could not be updated"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return dataset_record
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the dataset record"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)

    # Delete Dataset Record
    @delete(path="/records/id/{record_id:str}")
    async def delete_dataset_record(
        self, record_id: str
    ) -> None:
        try:
            dataset_record = DatasetRecord.get_by_id(id=record_id)
            if dataset_record is None:
                error_html = RESTAPIError(
                    error="Dataset record not found",
                    error_description="No dataset record was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = dataset_record.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Dataset record not deleted",
                    error_description="The dataset record could not be deleted"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the dataset record"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
    