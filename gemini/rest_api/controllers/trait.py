from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar import Response
from litestar.response import Stream, File
from litestar.serialization import encode_json

from pydantic import BaseModel
from datetime import datetime, date
from collections.abc import AsyncGenerator

from gemini.api.trait import Trait
from gemini.api.trait_record import TraitRecord
from gemini.api.experiment import Experiment
from gemini.api.enums import GEMINITraitLevel
from gemini.rest_api.src.models import (
    TraitInput,
    TraitOutput,
    TraitSearch,
    TraitRecordInput,
    TraitRecordOutput,
    TraitRecordSearch,
    DatasetOutput
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
        
        
class TraitController(Controller):
    
    # Get Traits
    @get()
    async def get_traits(
        self,
        trait_name: Optional[str] = None,
        trait_units: Optional[str] = None,
        trait_level_id: Optional[GEMINITraitLevel] = None,
        trait_info: Optional[dict] = None,
        experiment_name: Optional[str] = 'Default'
    ) -> List[TraitOutput]:
        try:
            traits = Trait.search(
                trait_name=trait_name,
                trait_units=trait_units,
                trait_level_id=trait_level_id,
                trait_info=trait_info,
                experiment_name=experiment_name
            )
            if traits is None:
                return Response(content="No traits found", status_code=404)
            traits = [trait.model_dump() for trait in traits]
            traits = [TraitOutput.model_validate(trait) for trait in traits]
            return traits
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Create a new Trait
    @post()
    async def create_trait(
        self,
        data: Annotated[TraitInput, Body]
    ) -> TraitOutput:
        try:
            trait = Trait.create(
                trait_name=data.trait_name,
                trait_units=data.trait_units,
                trait_level=GEMINITraitLevel(data.trait_level_id),
                trait_info=data.trait_info
            )
            if trait is None:
                return Response(content="Trait already exists", status_code=409)
            trait = TraitOutput.model_validate(trait.model_dump())
            return trait
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Traits by Level ID
    @get(path="/level/{trait_level_id:int}")
    async def get_traits_by_level(
        self, trait_level_id: int
    ) -> List[TraitOutput]:
        try:
            traits = Trait.get_by_level(trait_level=GEMINITraitLevel(trait_level_id))
            if traits is None:
                return Response(content="No traits found", status_code=404)
            traits = [trait.model_dump() for trait in traits]
            traits = [TraitOutput.model_validate(trait) for trait in traits]
            return traits
        except Exception as e:
            return Response(content=str(e), status_code=500)
            
    # Get Trait by Trait Name
    @get('/{trait_name:str}')
    async def get_trait(
        self,
        trait_name: str
    ) -> TraitOutput:
        try:
            trait = Trait.get(trait_name=trait_name)
            if trait is None:
                return Response(content="Trait not found", status_code=404)
            return TraitOutput.model_validate(trait.model_dump())
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Trait Info by Trait Name
    @get('/{trait_name:str}/info')
    async def get_trait_info(
        self,
        trait_name: str
    ) -> dict:
        try:
            trait = Trait.get(trait_name=trait_name)
            if trait is None:
                return Response(content="Trait not found", status_code=404)
            return trait.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Set Trait Info by Trait Name
    @patch('/{trait_name:str}/info')
    async def set_trait_info(
        self,
        trait_name: str,
        data: dict
    ) -> dict:
        try:
            trait = Trait.get(trait_name=trait_name)
            if trait is None:
                return Response(content="Trait not found", status_code=404)
            trait.set_info(data)
            return trait.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Trait Datasets
    @get('/{trait_name:str}/datasets')
    async def get_trait_datasets(
        self,
        trait_name: str
    ) -> List[DatasetOutput]:
        try:
            trait = Trait.get(trait_name=trait_name)
            if trait is None:
                return Response(content="Trait not found", status_code=404)
            datasets = trait.get_datasets()
            if datasets is None:
                return Response(content="No datasets found", status_code=404)
            datasets = [dataset.model_dump() for dataset in datasets]
            datasets = [DatasetOutput.model_validate(dataset) for dataset in datasets]
            return datasets
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
        
    # Get Trait Records
    @get('/{trait_name:str}/records')
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
    @post('/{trait_name:str}/records')
    async def create_trait_record(
        self,
        trait_name: str,
        data: Annotated[TraitRecordInput, Body]
    ) -> TraitRecordOutput:
        try:
            trait = Trait.get(trait_name=trait_name)
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
    @get('/records/{record_id:str}')
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
        
    # Get Trait Record Info by Record ID
    @get('/records/{record_id:str}/info')
    async def get_trait_record_info(
        self,
        record_id: str
    ) -> dict:
        try:
            record = TraitRecord.get_by_id(record_id)
            if record is None:
                return Response(content="Record not found", status_code=404)
            return record.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Set Trait Record Info by Record ID
    @patch('/records/{record_id:str}/info')
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
    @delete('/records/{record_id:str}')
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
        
        
    
    