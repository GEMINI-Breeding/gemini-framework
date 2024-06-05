from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar import Response

from pydantic import BaseModel, UUID4
from datetime import datetime, date

from gemini.api.experiment import Experiment
from gemini.api.site import Site

from typing import List, Annotated, Optional

class SiteInput(BaseModel):
    site_name: str = "Test Site"
    experiment_name: str = "Test Experiment"
    site_city: Optional[str] = "Test City"
    site_state: Optional[str] = "Test State"
    site_country: Optional[str] = "Test Country"
    site_info: Optional[dict] = {}
    
    
class SiteController(Controller):
    
    # Get Sites
    @get()
    async def get_sites(
        self,
        experiment_name: Optional[str] = None,
        site_name: Optional[str] = None,
        site_city: Optional[str] = None,
        site_state: Optional[str] = None,
        site_country: Optional[str] = None,
        site_info: Optional[dict] = None
    ) -> List[Site]:
        experiment = Experiment.get(experiment_name=experiment_name)
        sites = Site.search(
            experiment_id=experiment.id if experiment else None,
            site_name=site_name,
            site_city=site_city,
            site_state=site_state,
            site_country=site_country,
            site_info=site_info
        )
        if sites is None:
            return Response(status_code=404)
        return sites
    
    # Create a new Site
    @post()
    async def create_site(
        self, data: Annotated[SiteInput, Body]
    ) -> Site:
        site = Site.create(
            site_name=data.site_name,
            experiment_name=data.experiment_name,
            site_city=data.site_city,
            site_state=data.site_state,
            site_country=data.site_country,
            site_info=data.site_info
        )
        if site is None:
            return Response(status_code=404)
        return site
    
    # Get by site name
    @get('/{site_name:str}')
    async def get_site(
        self,
        site_name: str
    ) -> Site:
        site = Site.get(site_name=site_name)
        if site is None:
            return Response(status_code=404)
        return site
    
    # Get Site Info
    @get('/{site_name:str}/info')
    async def get_site_info(
        self,
        site_name: str
    ) -> dict:
        site = Site.get(site_name=site_name)
        if site is None:
            return Response(status_code=404)
        return site.get_info()
    
    # Set Site Info
    @patch('/{site_name:str}/info')
    async def set_site_info(
        self,
        site_name: str,
        data: dict
    ) -> dict:
        site = Site.get(site_name=site_name)
        if site is None:
            return Response(status_code=404)
        site.set_info(site_info=data)
        return site.get_info()