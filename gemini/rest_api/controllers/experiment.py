from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar import Response


from pydantic import BaseModel, UUID4
from datetime import datetime, date, timedelta

from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.sensor import Sensor
from gemini.api.trait import Trait
from gemini.api.resource import Resource
from gemini.api.cultivar import Cultivar
from gemini.api.model import Model
from gemini.api.procedure import Procedure
from gemini.api.script import Script
from gemini.api.dataset import Dataset


from typing import List, Annotated, Optional

class ExperimentInput(BaseModel):
    experiment_name: str = "Test Experiment"
    experiment_info: Optional[dict] = {}
    experiment_start_date: Optional[date] = date.today()
    experiment_end_date: Optional[date] = date.today() + timedelta(days=1)


class ExperimentController(Controller):
    
    # Get Experiments
    @get()
    async def get_experiments(
        self,
        experiment_name: Optional[str] = None,
        experiment_start_date: Optional[date] = None,
        experiment_end_date: Optional[date] = None,
        experiment_info: Optional[dict] = None
    ) -> List[Experiment]:
        experiments = Experiment.search(
            experiment_name=experiment_name,
            experiment_start_date=experiment_start_date,
            experiment_end_date=experiment_end_date,
            experiment_info=experiment_info
        )
        if experiments is None:
            return Response(content="No experiments found", status_code=404)
        return experiments
    
    # Create a new Experiment
    @post()
    async def create_experiment(
        self, data: Annotated[ExperimentInput, Body]
    ) -> Experiment:
        experiment = Experiment.create(
            experiment_name=data.experiment_name,
            experiment_info=data.experiment_info,
            experiment_start_date=data.experiment_start_date,
            experiment_end_date=data.experiment_end_date
        )
        if experiment is None:
            return Response(status_code=404)
        return experiment
    
    # Get Experiment Info
    @get(path="/{experiment_name:str}/info")
    async def get_experiment_info(self, experiment_name: str) -> dict:
        experiment = Experiment.get(experiment_name=experiment_name)
        if not experiment:
            return Response(content="Experiment not found", status_code=404)
        return experiment.get_info()
    
    # Set Experiment Info
    @patch(path="/{experiment_name:str}/info")
    async def set_experiment_info(self, experiment_name: str, data: dict) -> dict:
        experiment = Experiment.get(experiment_name=experiment_name)
        if not experiment:
            return Response(content="Experiment not found", status_code=404)
        experiment.set_info(experiment_info=data)
        return experiment.get_info()
    
    # Get Experiment by name
    @get(path="/{experiment_name:str}")
    async def get_experiment_by_name(self, experiment_name: str) -> Experiment:
        experiment = Experiment.get(experiment_name=experiment_name)
        if not experiment:
            return Response(content="Experiment not found", status_code=404)
        return experiment
    
    # Get Experiment Seasons
    @get(path="/{experiment_name:str}/seasons")
    async def get_experiment_seasons(self, experiment_name: str) -> List[Season]:
        experiment = Experiment.get(experiment_name=experiment_name)
        if not experiment:
            return Response(content="Experiment not found", status_code=404)
        seasons = experiment.get_seasons()
        return seasons
    
    # Get Experiment Sites
    @get(path="/{experiment_name:str}/sites")
    async def get_experiment_sites(self, experiment_name: str) -> List[Site]:
        experiment = Experiment.get(experiment_name=experiment_name)
        if not experiment:
            return Response(content="Experiment not found", status_code=404)
        sites = experiment.get_sites()
        return sites
    
    # Get Experiment Traits
    @get(path="/{experiment_name:str}/traits")
    async def get_experiment_traits(self, experiment_name: str) -> List[Trait]:
        experiment = Experiment.get(experiment_name=experiment_name)
        if not experiment:
            return Response(content="Experiment not found", status_code=404)
        traits = experiment.get_traits()
        return traits
    
    # Get Experiment Resources
    @get(path="/{experiment_name:str}/resources")
    async def get_experiment_resources(self, experiment_name: str) -> List[Resource]:
        experiment = Experiment.get(experiment_name=experiment_name)
        if not experiment:
            return Response(content="Experiment not found", status_code=404)
        resources = experiment.get_resources()
        return resources
    
    # Get Experiment Sensors
    @get(path="/{experiment_name:str}/sensors")
    async def get_experiment_sensors(self, experiment_name: str) -> List[Sensor]:
        experiment = Experiment.get(experiment_name=experiment_name)
        if not experiment:
            return Response(content="Experiment not found", status_code=404)
        sensors = experiment.get_sensors()
        return sensors
    
    # Get Experiment Cultivars
    @get(path="/{experiment_name:str}/cultivars")
    async def get_experiment_cultivars(self, experiment_name: str) -> List[Cultivar]:
        experiment = Experiment.get(experiment_name=experiment_name)
        if not experiment:
            return Response(content="Experiment not found", status_code=404)
        cultivars = experiment.get_cultivars()
        return cultivars
    
    # Get Experiment Datasets
    @get(path="/{experiment_name:str}/datasets")
    async def get_experiment_datasets(self, experiment_name: str) -> List[Dataset]:
        experiment = Experiment.get(experiment_name=experiment_name)
        if not experiment:
            return Response(content="Experiment not found", status_code=404)
        datasets = experiment.get_datasets()
        return datasets
    
    # Get Experiment Scripts
    @get(path="/{experiment_name:str}/scripts")
    async def get_experiment_scripts(self, experiment_name: str) -> List[Script]:
        experiment = Experiment.get(experiment_name=experiment_name)
        if not experiment:
            return Response(content="Experiment not found", status_code=404)
        scripts = experiment.get_scripts()
        return scripts
    
    # Get Experiment Procedures
    @get(path="/{experiment_name:str}/procedures")
    async def get_experiment_procedures(self, experiment_name: str) -> List[Procedure]:
        experiment = Experiment.get(experiment_name=experiment_name)
        if not experiment:
            return Response(content="Experiment not found", status_code=404)
        procedures = experiment.get_procedures()
        return procedures
    
    # Get Experiment Models
    @get(path="/{experiment_name:str}/models")
    async def get_experiment_models(self, experiment_name: str) -> List[Model]:
        experiment = Experiment.get(experiment_name=experiment_name)
        if not experiment:
            return Response(status_code=404)
        models = experiment.get_models()
        return models
        
 