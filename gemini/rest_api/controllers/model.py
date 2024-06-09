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
from gemini.api.dataset import Dataset
from gemini.api.model import Model
from gemini.api.model_record import ModelRecord
from gemini.api.model_run import ModelRun
from gemini.rest_api.src.file_handler import file_handler

from typing import List, Annotated, Optional

async def model_record_search_generator(model_name: str, search_parameters: dict) -> AsyncGenerator[bytes, None]:
    model = Model.get(model_name=model_name)
    records = model.get_records(**search_parameters)
    for record in records:
        record = record.model_dump_json(exclude_none=True)
        yield record

class ModelInput(BaseModel):
    model_name: str = "Test Model"
    experiment_name: str = "Test Experiment"
    model_url: Optional[str] = None
    model_info: Optional[dict] = {}

class ModelRecordInput(BaseModel):

    model_config = {
        "arbitrary_types_allowed": True
    }

    file: Optional[UploadFile] = None
    timestamp: datetime = datetime.now()
    collection_date: date = datetime.now().date()
    model_data: dict = {}
    dataset_name: str = "Test Dataset"
    experiment_name: str = "Test Experiment"
    season_name: str = "2023"
    site_name: str = "Test Site"
    plot_number: int = 1
    plot_row_number: int = 1
    plot_column_number: int = 1
    record_info: Optional[dict] = {}


class ModelController(Controller):

    # Get Models
    @get()
    async def get_models(
        self,
        model_name: Optional[str] = None,
        model_url: Optional[str] = None,
        model_info: Optional[dict] = {}
    ) -> List[Model]:
        models = Model.search(
            model_name=model_name,
            model_url=model_url,
            model_info=model_info
        )
        if models is None:
            return Response(content="No models found", status_code=404)
        return models
    
    # Get Model by Name
    @get('/{model_name:str}')
    async def get_model_by_name(
        self,
        model_name: str
    ) -> Model:
        model = Model.get(model_name=model_name)
        if model is None:
            return Response(content="Model not found", status_code=404)
        return model
    
    # Get Models by Experiment
    @get('/experiment/{experiment_name:str}')
    async def get_models_by_experiment(
        self,
        experiment_name: str
    ) -> List[Model]:
        models = Model.get_by_experiment(experiment_name=experiment_name)
        if models is None:
            return Response(content="No models found", status_code=404)
        return models
    
    # Get Model Info
    @get('/{model_name:str}/info')
    async def get_model_info(
        self,
        model_name: str
    ) -> dict:
        model = Model.get(model_name=model_name)
        if model is None:
            return Response(content="Model not found", status_code=404)
        return model.model_info
    
    # Set Model Info
    @patch('/{model_name:str}/info')
    async def set_model_info(
        self,
        model_name: str,
        data: dict
    ) -> dict:
        model = Model.get(model_name=model_name)
        if model is None:
            return Response(content="Model not found", status_code=404)
        model.set_info(model_info=data)
        return model.model_info
    
    # Add Model Record
    @post('/{model_name:str}/record')
    async def add_model_record(
        self,
        model_name: str,
        data: Annotated[ModelRecordInput, Body(media_type=RequestEncodingType.MULTI_PART)]
    ) -> bool:
        
        if data.file is not None:
            file_path = await file_handler.create_file(data.file)
            data.model_data = {"file": file_path}

        model = Model.get(model_name=model_name)
        if model is None:
            return Response(content="Model not found", status_code=404)
        
        model.add_record(
            timestamp=data.timestamp,
            collection_date=data.collection_date,
            model_data=data.model_data,
            dataset_name=data.dataset_name,
            experiment_name=data.experiment_name,
            season_name=data.season_name,
            site_name=data.site_name,
            plot_number=data.plot_number,
            plot_row_number=data.plot_row_number,
            plot_column_number=data.plot_column_number,
            record_info=data.record_info
        )
        return True
    
    # Get Model Records
    @get('/{model_name:str}/records')
    async def search_model_records(
        self,
        model_name: str,
        collection_date: Optional[date] = None,
        dataset_name: Optional[str] = None,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        plot_number: Optional[int] = None,
        plot_row_number: Optional[int] = None,
        plot_column_number: Optional[int] = None
    ) -> Stream:
        search_parameters = {
            "collection_date": collection_date,
            "dataset_name": dataset_name,
            "experiment_name": experiment_name,
            "season_name": season_name,
            "site_name": site_name,
            "plot_number": plot_number,
            "plot_row_number": plot_row_number,
            "plot_column_number": plot_column_number
        }
        return Stream(model_record_search_generator(model_name, search_parameters))
    
    # Set Dataset Record Info by Record ID
    @patch('/record/{record_id:str}/info')
    async def set_model_record_info(
        self,
        record_id: str,
        data: dict
    ) -> dict:
        record = ModelRecord.get(record_id=record_id)
        if record is None:
            return Response(content="Record not found", status_code=404)
        record.set_info(record_info=data)
        return record.record_info
    
    # Get Dataset Record Info by Record ID
    @get('/record/{record_id:str}/info')
    async def get_model_record_info(
        self,
        record_id: str
    ) -> dict:
        record = ModelRecord.get(record_id=record_id)
        if record is None:
            return Response(content="Record not found", status_code=404)
        return record.record_info
    
