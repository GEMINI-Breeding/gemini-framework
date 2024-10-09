from litestar.controller import Controller
from litestar.handlers import get, post, patch
from litestar.params import Body
from litestar import Response

from gemini.api.trait import Trait
from gemini.api.enums import GEMINITraitLevel
from gemini.server.rest_api.src.models import (
    TraitInput,
    TraitOutput,
    DatasetOutput
)

from typing import List, Annotated, Optional

        
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
                trait_info=data.trait_info,
                experiment_name=data.experiment_name
            )
            if trait is None:
                return Response(content="Trait already exists", status_code=409)
            trait = TraitOutput.model_validate(trait.model_dump())
            return trait
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    
    # Get Traits by ID
    @get(path="/id/{trait_id:str}")
    async def get_trait_by_id(
        self, trait_id: str
    ) -> TraitOutput:
        try:
            trait = Trait.get_by_id(trait_id=trait_id)
            if trait is None:
                return Response(content="Trait not found", status_code=404)
            return TraitOutput.model_validate(trait.model_dump())
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
        
  