from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller
from litestar.response import Stream, Redirect
from litestar.serialization import encode_json
from litestar.enums import RequestEncodingType

from collections.abc import AsyncGenerator, Generator

from pydantic import BaseModel

from gemini.api.procedure import Procedure
from gemini.api.procedure_record import ProcedureRecord 
from gemini.rest_api.models import (
    ProcedureInput,
    ProcedureOutput,
    ProcedureUpdate,
    ProcedureRunOutput,
    DatasetOutput,
    RESTAPIError,
    JSONB,
    str_to_dict
)

from gemini.rest_api.models import (
    ProcedureRecordInput,
    ProcedureRecordOutput,
    ProcedureRecordUpdate,
)

from gemini.rest_api.file_handler import api_file_handler

from typing import List, Annotated, Optional


async def procedure_records_bytes_generator(procedure_record_generator : Generator[ProcedureRecord, None, None]) -> AsyncGenerator[bytes, None]:
    for record in procedure_record_generator:
        record = record.model_dump(exclude_none=True)
        record = encode_json(record) + b'\n'
        yield record


class ProcedureProcedureRunInput(BaseModel):
    procedure_run_info: Optional[JSONB] = {}


class ProcedureDatasetInput(BaseModel):
    dataset_name: str
    dataset_info: Optional[JSONB] = {}
    collection_date: Optional[str] = None
    experiment_name: Optional[str] = 'Experiment A'

class ProcedureController(Controller):

    # Get All Procedures
    @get(path="/all")
    async def get_all_procedures(self) -> List[ProcedureOutput]:
        try:
            procedures = Procedure.get_all()
            if procedures is None:
                error_html = RESTAPIError(
                    error="No Procedures Found",
                    error_description="No procedures found"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return procedures
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)

    # Get Procedures
    @get()
    async def get_procedures(
        self,
        procedure_name: Optional[str] = None,
        procedure_info: Optional[JSONB] = None,
        experiment_name: Optional[str] = 'Experiment A'
    ) -> List[ProcedureOutput]:
        try:
            if procedure_info is not None:
                procedure_info = str_to_dict(procedure_info)

            procedures = Procedure.search(
                procedure_name=procedure_name,
                procedure_info=procedure_info,
                experiment_name=experiment_name
            )
            if procedures is None:
                error_html = RESTAPIError(
                    error="No Procedures Found",
                    error_description="No procedures found with the given search parameters"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return procedures
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Procedure by ID
    @get(path="/id/{procedure_id:str}")
    async def get_procedure_by_id(
        self, procedure_id: str
    ) -> ProcedureOutput:
        try:
            procedure = Procedure.get_by_id(id=procedure_id)
            if procedure is None:
                error_html = RESTAPIError(
                    error="Procedure Not Found",
                    error_description="No procedure found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return procedure
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
        

    # Create Procedure
    @post()
    async def create_procedure(
        self,
        data: Annotated[ProcedureInput, Body]
    ) -> ProcedureOutput:
        try:
            procedure = Procedure.create(
                procedure_name=data.procedure_name,
                procedure_info=data.procedure_info,
                experiment_name=data.experiment_name
            )
            if procedure is None:
                error_html = RESTAPIError(
                    error="Procedure Creation Failed",
                    error_description="Failed to create the procedure"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return procedure
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
        
    # Update Procedure
    @patch(path="/id/{procedure_id:str}")
    async def update_procedure(
        self,
        procedure_id: str,
        data: Annotated[ProcedureUpdate, Body]
    ) -> ProcedureOutput:
        try:
            procedure = Procedure.get_by_id(id=procedure_id)
            if procedure is None:
                error_html = RESTAPIError(
                    error="Procedure Not Found",
                    error_description="No procedure found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            procedure = procedure.update(
                procedure_name=data.procedure_name,
                procedure_info=data.procedure_info
            )
            if not procedure:
                error_html = RESTAPIError(
                    error="Procedure Update Failed",
                    error_description="Failed to update the procedure"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return procedure
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
        

    # Delete Procedure
    @delete(path="/id/{procedure_id:str}")
    async def delete_procedure(
        self, procedure_id: str
    ) -> None:
        try:
            procedure = Procedure.get_by_id(id=procedure_id)
            if procedure is None:
                error_html = RESTAPIError(
                    error="Procedure Not Found",
                    error_description="No procedure found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = procedure.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Procedure Deletion Failed",
                    error_description="Failed to delete the procedure"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Procedure Runs
    @get(path="/id/{procedure_id:str}/runs")
    async def get_procedure_runs(
        self, procedure_id: str
    ) -> List[ProcedureRunOutput]:
        try:
            procedure = Procedure.get_by_id(id=procedure_id)
            if procedure is None:
                error_html = RESTAPIError(
                    error="Procedure Not Found",
                    error_description="No procedure found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            runs = procedure.get_runs()
            if runs is None:
                error_html = RESTAPIError(
                    error="No Procedure Runs Found",
                    error_description="No runs found for the given procedure"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return runs
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
        
    
    # Get Procedure Datasets
    @get(path="/id/{procedure_id:str}/datasets")
    async def get_procedure_datasets(
        self, procedure_id: str
    ) -> List[DatasetOutput]:
        try:
            procedure = Procedure.get_by_id(id=procedure_id)
            if procedure is None:
                error_html = RESTAPIError(
                    error="Procedure Not Found",
                    error_description="No procedure found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            datasets = procedure.get_datasets()
            if datasets is None:
                error_html = RESTAPIError(
                    error="No Procedure Datasets Found",
                    error_description="No datasets found for the given procedure"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return datasets
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
        
    # Create Procedure Run
    @post(path="/id/{procedure_id:str}/runs")
    async def create_procedure_run(
        self,
        procedure_id: str,
        data: Annotated[ProcedureProcedureRunInput, Body]
    ) -> ProcedureRunOutput:
        try:
            procedure = Procedure.get_by_id(id=procedure_id)
            if procedure is None:
                error_html = RESTAPIError(
                    error="Procedure Not Found",
                    error_description="No procedure found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            run = procedure.create_run(procedure_run_info=data.procedure_run_info)
            if run is None:
                error_html = RESTAPIError(
                    error="Procedure Run Creation Failed",
                    error_description="Failed to create the procedure run"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return run
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
        
    # Create Procedure Dataset
    @post(path="/id/{procedure_id:str}/datasets")
    async def create_procedure_dataset(
        self,
        procedure_id: str,
        data: Annotated[ProcedureDatasetInput, Body]
    ) -> DatasetOutput:
        try:
            procedure = Procedure.get_by_id(id=procedure_id)
            if procedure is None:
                error_html = RESTAPIError(
                    error="Procedure Not Found",
                    error_description="No procedure found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            dataset = procedure.create_dataset(
                dataset_name=data.dataset_name,
                dataset_info=data.dataset_info,
                collection_date=data.collection_date,
                experiment_name=data.experiment_name
            )
            if dataset is None:
                error_html = RESTAPIError(
                    error="Procedure Dataset Creation Failed",
                    error_description="Failed to create the procedure dataset"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return dataset
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
        
    # Add a Procedure Record
    @post(path="/id/{procedure_id:str}/records")
    async def add_procedure_record(
        self,
        procedure_id: str,
        data: Annotated[ProcedureRecordInput, Body(media_type=RequestEncodingType.MULTI_PART)]
    ) -> ProcedureRecordOutput:
        try:
            procedure = Procedure.get_by_id(id=procedure_id)
            if procedure is None:
                error_html = RESTAPIError(
                    error="Procedure Not Found",
                    error_description="No procedure found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            if data.record_file:
                record_file_path = await api_file_handler.create_file(data.record_file)

            add_success, inserted_record_ids = procedure.add_record(
                timestamp=data.timestamp,
                collection_date=data.collection_date,
                procedure_data=data.procedure_data,
                dataset_name=data.dataset_name,
                experiment_name=data.experiment_name,
                season_name=data.season_name,
                site_name=data.site_name,
                record_file=record_file_path if data.record_file else None,
                record_info=data.record_info
            )
            if not add_success:
                error_html = RESTAPIError(
                    error="Procedure Record Addition Failed",
                    error_description="Failed to add the procedure record"
                ).to_html()
                return Response(content=error_html, status_code=500)
            inserted_record_id = inserted_record_ids[0]
            inserted_procedure_record = ProcedureRecord.get_by_id(id=inserted_record_id)
            if inserted_procedure_record is None:
                error_html = RESTAPIError(
                    error="Procedure Record Not Found",
                    error_description="No procedure record found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return inserted_procedure_record
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Procedure Records
    @get(path="/id/{procedure_id:str}/records")
    async def search_procedure_records(
        self,
        procedure_id: str,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        collection_date: Optional[str] = None
    ) -> Stream:
        try:
            procedure = Procedure.get_by_id(id=procedure_id)
            if procedure is None:
                error_html = RESTAPIError(
                    error="Procedure Not Found",
                    error_description="No procedure found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            records = procedure.get_records(
                collection_date=collection_date,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name
            )
            return Stream(procedure_records_bytes_generator(records), media_type="application/ndjson")
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Procedure Record by ID
    @get(path="/records/id/{procedure_record_id:str}")
    async def get_procedure_record_by_id(
        self, procedure_record_id: str
    ) -> ProcedureRecordOutput:
        try:
            record = ProcedureRecord.get_by_id(id=procedure_record_id)
            if record is None:
                error_html = RESTAPIError(
                    error="Procedure Record Not Found",
                    error_description="No procedure record found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return record
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
        
    # Get Procedure Record File
    @get(path="/records/id/{record_id:str}/download")
    async def download_procedure_record_file(
        self, record_id: str
    ) -> Redirect:
        try:
            procedure_record = ProcedureRecord.get_by_id(id=record_id)
            if procedure_record is None:
                error_html = RESTAPIError(
                    error="Procedure Record Not Found",
                    error_description="No procedure record found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            record_file = procedure_record.record_file
            if record_file is None:
                error_html = RESTAPIError(
                    error="Procedure Record File Not Found",
                    error_description="No file associated with the procedure record"
                ).to_html()
                return Response(content=error_html, status_code=404)
            bucket_name = "gemini"
            object_name = record_file
            object_path = f"{bucket_name}/{object_name}"
            return Redirect(path=f"/api/files/download/{object_path}")
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
    
            
    # Update Procedure Record
    @patch(path="/records/id/{procedure_record_id:str}")
    async def update_procedure_record(
        self,
        procedure_record_id: str,
        data: Annotated[ProcedureRecordUpdate, Body]
    ) -> ProcedureRecordOutput:
        try:
            procedure_record = ProcedureRecord.get_by_id(id=procedure_record_id)
            if procedure_record is None:
                error_html = RESTAPIError(
                    error="Procedure Record Not Found",
                    error_description="No procedure record found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            procedure_record = procedure_record.update(
                procedure_data=data.procedure_data,
                record_info=data.record_info
            )
            if not procedure_record:
                error_html = RESTAPIError(
                    error="Procedure Record Update Failed",
                    error_description="Failed to update the procedure record"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return procedure_record
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)
        
    # Delete Procedure Record
    @delete(path="/records/id/{procedure_record_id:str}")
    async def delete_procedure_record(
        self, procedure_record_id: str
    ) -> None:
        try:
            procedure_record = ProcedureRecord.get_by_id(id=procedure_record_id)
            if procedure_record is None:
                error_html = RESTAPIError(
                    error="Procedure Record Not Found",
                    error_description="No procedure record found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            is_deleted = procedure_record.delete()
            if not is_deleted:
                error_html = RESTAPIError(
                    error="Procedure Record Deletion Failed",
                    error_description="Failed to delete the procedure record"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return None
        except Exception as e:
            error_html = RESTAPIError(
                error="Internal Server Error",
                error_description=str(e)
            ).to_html()
            return Response(content=error_html, status_code=500)