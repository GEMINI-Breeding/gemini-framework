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
from gemini.api.procedure import Procedure
from gemini.api.procedure_record import ProcedureRecord
from gemini.api.procedure_run import ProcedureRun
from gemini.rest_api.src.file_handler import file_handler

from typing import List, Annotated, Optional

async def procedure_record_search_generator(procedure_name: str, search_parameters: dict) -> AsyncGenerator[bytes, None]:
    procedure = Procedure.get(procedure_name=procedure_name)
    records = procedure.get_records(**search_parameters)
    for record in records:
        record = record.model_dump_json(exclude_none=True)
        yield record

class ProcedureInput(BaseModel):
    procedure_name: str = "Test Procedure"
    experiment_name: str = "Test Experiment"
    procedure_info: Optional[dict] = {}

class ProcedureRecordInput(BaseModel):

    model_config = {
        "arbitrary_types_allowed": True
    }

    file: Optional[UploadFile] = None
    timestamp: datetime = datetime.now()
    collection_date: date = datetime.now().date()
    procedure_data: dict = {}
    dataset_name: str = "Test Dataset"
    experiment_name: str = "Test Experiment"
    season_name: str = "2023"
    site_name: str = "Test Site"
    plot_number: int = 1
    plot_row_number: int = 1
    plot_column_number: int = 1
    record_info: Optional[dict] = {}


class ProcedureController(Controller):

    # Get Procedures
    @get()
    async def get_procedures(
        self,
        procedure_name: Optional[str] = None,
        procedure_info: Optional[dict] = None
    ) -> List[Procedure]:
        procedures = Procedure.search(
            procedure_name=procedure_name,
            procedure_info=procedure_info
        )
        if not procedures:
            return Response(content="No procedures found", status_code=404)
        return procedures
        
    # Get procedure by name
    @get('/{procedure_name:str}')
    async def get_procedure_by_name(
        self,
        procedure_name: str
    ) -> Procedure:
        procedure = Procedure.get(procedure_name=procedure_name)
        if not procedure:
            return Response(content="Procedure not found", status_code=404)
        return procedure
    
    # Get procedures by experiment name
    @get('/experiment/{experiment_name:str}')
    async def get_procedures_by_experiment_name(
        self,
        experiment_name: str
    ) -> List[Procedure]:
        procedures = Procedure.get_by_experiment_name(experiment_name=experiment_name)
        if not procedures:
            return Response(content="No procedures found", status_code=404)
        return procedures
    
    # Get Procedure Info
    @get('/info/{procedure_name:str}')
    async def get_procedure_info(
        self,
        procedure_name: str
    ) -> dict:
        procedure = Procedure.get(procedure_name=procedure_name)
        if not procedure:
            return Response(content="Procedure not found", status_code=404)
        return procedure.procedure_info
    
    # Set Procedure Info
    @patch('/info/{procedure_name:str}')
    async def set_procedure_info(
        self,
        procedure_name: str,
        data: dict
    ) -> dict:
        procedure = Procedure.get(procedure_name=procedure_name)
        if not procedure:
            return Response(content="Procedure not found", status_code=404)
        procedure.set_info(procedure_info=data)
        return procedure.procedure_info
    
    # Add Procedure Record
    @post('/{procedure_name:str}/record')
    async def add_procedure_record(
        self,
        procedure_name: str,
        data: Annotated[ProcedureRecordInput, Body(media_type=RequestEncodingType.MULTI_PART)]
    ) -> bool:
        
        if data.file is not None:
            file_path = await file_handler.save_file(data.file)
            data.procedure_data['file_path'] = file_path

        procedure = Procedure.get(procedure_name=procedure_name)
        if not procedure:
            return Response(content="Procedure not found", status_code=404)
        procedure.add_record(
            collection_date=data.collection_date,
            dataset_name=data.dataset_name,
            experiment_name=data.experiment_name,
            season_name=data.season_name,
            site_name=data.site_name,
            plot_number=data.plot_number,
            plot_row_number=data.plot_row_number,
            plot_column_number=data.plot_column_number,
            record_info=data.record_info,
            procedure_data=data.procedure_data
        )

        return True

    # Get Procedure Records
    @get('/{procedure_name:str}/records')
    async def search_procedure_records(
        self,
        procedure_name: str,
        collection_date: Optional[date] = None,
        dataset_name: Optional[str] = None,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        plot_number: Optional[int] = None,
        plot_row_number: Optional[int] = None,
        plot_column_number: Optional[int] = None,
        record_info: Optional[dict] = None
    ) -> Stream:
        search_parameters = {
            "collection_date": collection_date,
            "dataset_name": dataset_name,
            "experiment_name": experiment_name,
            "season_name": season_name,
            "site_name": site_name,
            "plot_number": plot_number,
            "plot_row_number": plot_row_number,
            "plot_column_number": plot_column_number,
            "record_info": record_info
        }
        return Stream(procedure_record_search_generator(procedure_name, search_parameters))
    


