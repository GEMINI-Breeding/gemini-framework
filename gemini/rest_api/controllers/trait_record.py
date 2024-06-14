from litestar.controller import Controller
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.response import Stream
from litestar import Response
from litestar.serialization import encode_json

from datetime import datetime, date
from collections.abc import AsyncGenerator

from gemini.api.trait import Trait
from gemini.api.trait_record import TraitRecord

from gemini.rest_api.src.models import (
    TraitRecordBase,
    TraitRecordInput,
    TraitRecordOutput,
    TraitRecordSearch,
    TraitOutput
)

from typing import List, Annotated, Optional

async def trait_record_search_generator(search_parameters: TraitRecordSearch) -> AsyncGenerator[bytes, None]:
    search_parameters = search_parameters.model_dump(exclude_none=True)
    trait = Trait.get(trait_name=search_parameters['trait_name'])
    
    # Remove trait_name from search parameters
    search_parameters.pop('trait_name')
    trait_records = trait.get_records(**search_parameters)
    
    for record in trait_records:
        record = record.model_dump_json(exclude_none=True)
        yield record
        

class TraitRecordController(Controller):
          
    # Get Trait Records
    @get()
    async def get_trait_records(
        self,
        trait_name: str,
        collection_date: Optional[date] = None,
        experiment_name: Optional[str] = None,
        season_name: Optional[str] = None,
        site_name: Optional[str] = None,
        plot_number: Optional[int] = None,
        plot_row_number: Optional[int] = None,
        plot_column_number: Optional[int] = None,
        record_info: Optional[dict] = None
    ) -> Stream:
        try:
            search_parameters = TraitRecordSearch(
                trait_name=trait_name,
                collection_date=collection_date,
                experiment_name=experiment_name,
                season_name=season_name,
                site_name=site_name,
                plot_number=plot_number,
                plot_row_number=plot_row_number,
                plot_column_number=plot_column_number,
                record_info=record_info
            )
            records = Stream(trait_record_search_generator(search_parameters))
            return records
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    
    # Create a Trait Record
    @post()
    async def create_trait_record(
        self,
        data: Annotated[TraitRecordInput, Body]
    ) -> TraitRecordOutput:
        try:
            trait = Trait.get(trait_name=data.trait_name)
            if trait is None:
                return Response(content="Trait not found", status_code=404)
            record = trait.add_record(
                timestamp=data.timestamp,
                trait_value = data.trait_data,
                collection_date = data.collection_date,
                experiment_name = data.experiment_name,
                season_name = data.season_name,
                site_name = data.site_name,
                plot_number = data.plot_number,
                plot_row_number = data.plot_row_number,
                plot_column_number = data.plot_column_number,
                record_info = data.record_info
            )
            if record is None:
                return Response(content="Record already exists", status_code=409)
            record = TraitRecordOutput.model_validate(record.model_dump())
            return record
        except Exception as e:
            return Response(content=str(e), status_code=500)
    
    # Get Trait Record by Record ID 
    @get('/{record_id:str}')
    async def get_trait_record(
        self,
        record_id: str
    ) -> TraitRecordOutput:
        try:
            record = TraitRecord.get_by_id(record_id)
            if record is None:
                return Response(content="Record not found", status_code=404)
            return TraitRecordOutput.model_validate(record.model_dump())
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Set Trait Record Info by Record ID
    @patch('/{record_id:str}/info')
    async def set_trait_record_info(
        self,
        record_id: str,
        data: dict
    ) -> dict:
        try:
            record = TraitRecord.get_by_id(record_id)
            if record is None:
                return Response(content="Record not found", status_code=404)
            record.set_info(data)
            return record.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Delete Trait Record by Record ID
    @delete('/{record_id:str}')
    async def delete_trait_record(
        self,
        record_id: str
    ) -> None:
        try:
            record = TraitRecord.get_by_id(record_id)
            if record is None:
                return Response(content="Record not found", status_code=404)
            success_deleted = record.delete()
            if not success_deleted:
                return Response(content="Record not deleted", status_code=500)
            return None
        except Exception as e:
            return Response(content=str(e), status_code=500)
