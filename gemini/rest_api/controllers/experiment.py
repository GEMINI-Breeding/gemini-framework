from litestar.contrib.pydantic import PydanticDTO
from litestar.controller import Controller
from litestar.dto import DTOConfig, DTOData
from litestar.enums import RequestEncodingType, MediaType
from litestar.params import Body
from litestar.handlers import get, post, patch, delete
from pydantic import BaseModel, UUID4

from typing import List, Annotated, Optional
from datetime import datetime, date
from uuid import UUID

from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.sensor import Sensor
from gemini.api.trait import Trait
from gemini.api.resource import Resource
from gemini.api.cultivar import Cultivar


class ExperimentInput(BaseModel):
    experiment_name: str
    experiment_info: Optional[dict] = {}
    experiment_start_date: Optional[date] = datetime.now().date()
    experiment_end_date: Optional[date] = datetime.now().date()


class ExperimentController(Controller):

    # Filter experiments
    @get()
    async def get_experiments(
        self,
        experiment_name: Optional[str] = None,
        experiment_start_date: Optional[date] = None,
        experiment_end_date: Optional[date] = None,
        experiment_info: Optional[dict] = None,
    ) -> List[Experiment]:
        experiments = Experiment.search(
            experiment_name=experiment_name,
            experiment_start_date=experiment_start_date,
            experiment_end_date=experiment_end_date,
            experiment_info=experiment_info,
        )
        return experiments

    # Get Experiment by name
    @get(path="/{experiment_name:str}")
    async def get_experiment_by_name(self, experiment_name: str) -> Experiment:
        experiment = Experiment.get_by_name(experiment_name)
        return experiment
    
    # Get Experiment by ID
    @get(path="/id/{experiment_id:uuid}")
    async def get_experiment_by_id(self, experiment_id: UUID) -> Experiment:
        experiment = Experiment.get_by_id(experiment_id)
        return experiment

    # Create Experiment
    @post()
    async def create_experiment(
        self, data: Annotated[ExperimentInput, Body]
    ) -> Experiment:
        experiment = Experiment.create(
            experiment_name=data.experiment_name,
            experiment_info=data.experiment_info,
            experiment_start_date=data.experiment_start_date,
            experiment_end_date=data.experiment_end_date,
        )
        return experiment
    
    # Update Experiment
    @patch(path="/{experiment_name:str}")
    async def update_experiment(
        self, experiment_name: str, data: Annotated[ExperimentInput, Body]
    ) -> Experiment:
        experiment = Experiment.get_by_name(experiment_name)
        experiment = experiment.update(
            experiment_info=data.experiment_info,
            experiment_start_date=data.experiment_start_date,
            experiment_end_date=data.experiment_end_date,
        )
        return experiment

    # Get Experiment info
    @get(path="/{experiment_name:str}/info")
    async def get_experiment_info(self, experiment_name: str) -> dict:
        experiment = Experiment.get_by_name(experiment_name)
        return experiment.experiment_info

    # Set Experiment info
    @patch(path="/{experiment_name:str}/info")
    async def set_experiment_info(
        self, experiment_name: str, data: dict
    ) -> Experiment:
        experiment = Experiment.get_by_name(experiment_name)
        experiment = experiment.set_info(experiment_info=data)
        return experiment

    # Delete Experiment
    @delete(path="/{experiment_name:str}")
    async def delete_experiment(self, experiment_name: str) -> None:
        experiment = Experiment.get_by_name(experiment_name)
        experiment.delete()

    # Get Experiment Seasons
    @get(path="/{experiment_name:str}/seasons")
    async def get_experiment_seasons(self, experiment_name: str) -> List[Season]:
        experiment = Experiment.get_by_name(experiment_name=experiment_name)
        if not experiment:
            return []
        seasons = experiment.get_seasons()
        return seasons
    
    # Add Season to Experiment

    # Get Experiment Sites
    @get(path="/{experiment_name:str}/sites")
    async def get_experiment_sites(self, experiment_name: str) -> List[Site]:
        experiment = Experiment.get_by_name(experiment_name=experiment_name)
        if not experiment:
            return []
        sites = experiment.get_sites()
        return sites
    
    # Add Site to Experiment

    # Get Experiment Traits
    @get(path="/{experiment_name:str}/traits")
    async def get_experiment_traits(self, experiment_name: str) -> List[Trait]:
        experiment = Experiment.get_by_name(experiment_name=experiment_name)
        if not experiment:
            return []
        traits = experiment.get_traits()
        return traits
    
    # Add Trait to Experiment

    # Get Experiment Resources
    @get(path="/{experiment_name:str}/resources")
    async def get_experiment_resources(self, experiment_name: str) -> List[Resource]:
        experiment = Experiment.get_by_name(experiment_name=experiment_name)
        if not experiment:
            return []
        resources = experiment.get_resources()
        return resources
    
    # Add Resource to Experiment

    # Get Experiment Sensors
    @get(path="/{experiment_name:str}/sensors")
    async def get_experiment_sensors(self, experiment_name: str) -> List[Sensor]:
        experiment = Experiment.get_by_name(experiment_name=experiment_name)
        if not experiment:
            return []
        sensors = experiment.get_sensors()
        return sensors
    
    # Add Sensor to Experiment

    # Get Experiment Cultivars
    @get(path="/{experiment_name:str}/cultivars")
    async def get_experiment_cultivars(self, experiment_name: str) -> List[Cultivar]:
        experiment = Experiment.get_by_name(experiment_name=experiment_name)
        if not experiment:
            return []
        cultivars = experiment.get_cultivars()
        return cultivars
