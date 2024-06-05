from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar import Response
from litestar.response import Stream, File
from litestar.datastructures import UploadFile
from litestar.serialization import encode_json

from pydantic import BaseModel, UUID4
from datetime import datetime, date
from collections.abc import AsyncGenerator

from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.cultivar import Cultivar
from gemini.api.plot import Plot, PlotSearchParameters
from gemini.api.plant import Plant
from gemini.api.dataset import Dataset
from gemini.api.dataset_record import DatasetRecord
from gemini.api import GEMINIDatasetType
from gemini.rest_api.src.file_handler import file_handler

from typing import List, Annotated, Optional

async def dataset_record_search_generator(dataset_name: str, search_parameters: dict) -> AsyncGenerator[bytes, None]:
    dataset = Dataset.get(dataset_name=dataset_name)
    records = dataset.get_records(**search_parameters)
    for record in records:
        record = record.model_dump_json(exclude_none=True)
        yield record


class DatasetInput(BaseModel):
    dataset_name: str = "Test Dataset"
    experiment_name: str = "Test Experiment"
    dataset_info: Optional[dict] = {}
    is_derived: Optional[bool] = False
    collection_date: Optional[date] = datetime.now().date()
    dataset_type: Optional[GEMINIDatasetType] = GEMINIDatasetType.Default
    
class DatasetRecordInput(BaseModel):
    
    model_config = {
        "arbitrary_types_allowed": True
    }
    
    file: Optional[UploadFile] = None
    timestamp: datetime = datetime.now()
    collection_date: date = datetime.now().date()
    dataset_data: dict = {}
    experiment_name: str = "Test Experiment"
    season_name: str = "2023"
    site_name: str = "Test Site"
    plot_number: int = 1
    plot_row_number: int = 1
    plot_column_number: int = 1
    record_info: Optional[dict] = {}
    

class DatasetRecordFilesInput(BaseModel):
    
    model_config = {
        "arbitrary_types_allowed": True
    }
    
    files: List[UploadFile]
    timestamps : List[datetime] = None  
    experiment_name: str = "Test Experiment"
    season_name: str = "2023"
    site_name: str = "Test Site"
    plot_numbers: List[int] = None
    plot_row_numbers: List[int] = None
    plot_column_numbers: List[int] = None
    record_info: Optional[dict] = {}
    

    
    
class DatasetController(Controller):
    
    # Get Datasets
    @get()
    async def get_datasets(
        self,
        experiment_name: Optional[str] = None,
        dataset_name: Optional[str] = None,
        collection_date: Optional[date] = None,
        dataset_type: Optional[GEMINIDatasetType] = None,
        dataset_info: Optional[dict] = None
    ) -> List[Dataset]:
        experiment = Experiment.get(experiment_name=experiment_name)
        datasets = Dataset.search(
            experiment_id=experiment.id,
            dataset_name=dataset_name,
            collection_date=collection_date,
            dataset_info=dataset_info,
            dataset_type_id=dataset_type.value if dataset_type is not None else None
        )
        if datasets is None:
            return Response(status_code=404)
        return datasets
    
    # Get Dataset by name
    @get('/{dataset_name:str}')
    async def get_dataset(
        self,
        dataset_name: str
    ) -> Dataset:
        dataset = Dataset.get(dataset_name=dataset_name)
        if dataset is None:
            return Response(status_code=404)
        return dataset
    
    # Get Datasets by Type
    @get('/type/{dataset_type:int}')
    async def get_datasets_by_type(
        self,
        dataset_type: GEMINIDatasetType
    ) -> List[Dataset]:
        datasets = Dataset.get_by_type(dataset_type=dataset_type)
        if datasets is None:
            return Response(status_code=404)
        return datasets
    
    # Get Dataset Info
    @get('/{dataset_name:str}/info')
    async def get_dataset_info(
        self,
        dataset_name: str
    ) -> dict:
        dataset = Dataset.get(dataset_name=dataset_name)
        if dataset is None:
            return Response(status_code=404)
        return dataset.get_info()
    
    # Set Dataset Info
    @patch('/{dataset_name:str}/info')
    async def set_dataset_info(
        self,
        dataset_name: str,
        data: dict
    ) -> dict:
        dataset = Dataset.get(dataset_name=dataset_name)
        if dataset is None:
            return Response(status_code=404)
        dataset.set_info(data)
        return dataset.get_info()
    

    @post('/{dataset_name:str}/record')
    async def add_dataset_record(
        self,
        dataset_name: str,
        data: Annotated[DatasetRecordInput, Body(media_type=RequestEncodingType.MULTI_PART)]
    ) -> bool:
        
        if data.file is not None:
            file_path = await file_handler.create_file(data.file)
            data.dataset_data = {"file": file_path}
        
        dataset = Dataset.get(dataset_name=dataset_name)
        if dataset is None:
            return Response(content="Dataset not found", status_code=404)
        success = dataset.add_record(
            dataset_data=data.dataset_data,
            timestamp=data.timestamp,
            collection_date=data.collection_date,
            experiment_name=data.experiment_name,
            season_name=data.season_name,
            site_name=data.site_name,
            plot_number=data.plot_number,
            plot_row_number=data.plot_row_number,
            plot_column_number=data.plot_column_number,
            record_info=data.record_info
        )
        return success
    
    @post('/{dataset_name:str}/records/files')
    async def add_dataset_file_records(
        self,
        dataset_name: str,
        data: Annotated[DatasetRecordFilesInput, Body(media_type=RequestEncodingType.MULTI_PART)]
    ) -> bool:
        files = data.files
        if not files:
            return Response(content="No files found", status_code=400)
        file_paths = []
        for file in files:
            file_path = await file_handler.create_file(file)
            file_paths.append(file_path)
            
        dataset = Dataset.get(dataset_name=dataset_name)
        if dataset is None:
            return Response(content="Dataset not found", status_code=404)
        
        pass
    
    
    # Search Dataset Records
    @get('/{dataset_name:str}/record')
    async def search_dataset_records(
        self,
        dataset_name: str,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        plot_number: Optional[int] = None,
        plot_row_number: Optional[int] = None,
        plot_column_number: Optional[int] = None,
        record_info: Optional[dict] = None
    ) -> Stream:
        search_parameters = {
            "experiment_name": experiment_name,
            "season_name": season_name,
            "site_name": site_name,
            "plot_number": plot_number,
            "plot_row_number": plot_row_number,
            "plot_column_number": plot_column_number,
            "record_info": record_info
        }
        return Stream(dataset_record_search_generator(dataset_name, search_parameters))
    
    # Set Dataset Record info by Dataset Record Id
    @patch('/record/{record_id:str}/info')
    async def set_dataset_record_info(
        self,
        record_id: str,
        data: dict
    ) -> dict:
        record = DatasetRecord.get_by_id(record_id)
        if record is None:
            return Response(status_code=404)
        record.set_info(data)
        return record.get_info()
    
    # Get Dataset Record Info by Dataset Record Id
    @get('/record/{record_id:str}/info')
    async def get_dataset_record_info(
        self,
        record_id: str
    ) -> dict:
        record = DatasetRecord.get_by_id(record_id)
        if record is None:
            return Response(status_code=404)
        return record.get_info()