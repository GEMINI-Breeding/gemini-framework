from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar import Response

from pydantic import BaseModel, UUID4
from datetime import datetime, date

from gemini.api.experiment import Experiment
from gemini.api.site import Site
from gemini.rest_api.src.models import (
    SiteInput,
    SiteBase,
    SiteOutput,
    SiteSearch
)

from typing import List, Annotated, Optional


class SiteController(Controller):
    
    # Get Sites
    @get()
    async def get_sites(
        self,
        site_name: Optional[str] = None,
        site_city: Optional[str] = None,
        site_state: Optional[str] = None,
        site_country: Optional[str] = None,
        site_info: Optional[dict] = None,
        experiment_name: Optional[str] = 'Default'
    ) -> List[SiteOutput]:
        try:
            sites = Site.search(
                site_name=site_name,
                site_city=site_city,
                site_state=site_state,
                site_country=site_country,
                site_info=site_info,
                experiment_name=experiment_name
            )
            if sites is None:
                return Response(content="No sites found", status_code=404)
            sites = [site.model_dump() for site in sites]
            sites = [SiteOutput.model_validate(site) for site in sites]
            return sites
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Site by ID
    @get(path="/id/{site_id:str}")
    async def get_site_by_id(
        self, site_id: str
    ) -> SiteOutput:
        try:
            site = Site.get_by_id(site_id=site_id)
            if site is None:
                return Response(content="Site not found", status_code=404)
            return SiteOutput.model_validate(site.model_dump())
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Create a new Site
    @post()
    async def create_site(
        self, data: Annotated[SiteInput, Body]
    ) -> Site:
        try:
            site = Site.create(
                site_name=data.site_name,
                site_city=data.site_city,
                site_state=data.site_state,
                site_country=data.site_country,
                site_info=data.site_info,
                experiment_name=data.experiment_name
            )
            if site is None:
                return Response(content="Site already exists", status_code=409)
            site = SiteOutput.model_validate(site.model_dump())
            return site
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
        
    # Get by site name
    @get('/{site_name:str}')
    async def get_site(
        self,
        site_name: str
    ) -> Site:
        try:
            site = Site.get(site_name=site_name)
            if site is None:
                return Response(content="Site not found", status_code=404)
            return SiteOutput.model_validate(site.model_dump())
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Site Info
    @get('/{site_name:str}/info')
    async def get_site_info(
        self,
        site_name: str
    ) -> dict:
        try:
            site = Site.get(site_name=site_name)
            if site is None:
                return Response(content="Site not found", status_code=404)
            return site.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Set Site Info
    @patch('/{site_name:str}/info')
    async def set_site_info(
        self,
        site_name: str,
        data: dict
    ) -> dict:
        try:
            site = Site.get(site_name=site_name)
            if site is None:
                return Response(content="Site not found", status_code=404)
            site.set_info(data)
            return site.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
    
  