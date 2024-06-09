from litestar.controller import Controller
from litestar.enums import RequestEncodingType, MediaType
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar import Response

from pydantic import BaseModel, UUID4
from datetime import datetime, date, timedelta

from gemini.api.experiment import Experiment

from gemini.rest_api.src.models import (
    ExperimentBase,
    ExperimentInput,
    ExperimentOutput,
    SeasonOutput,
    SiteOutput,
    SensorOutput,
    TraitOutput,
    ResourceOutput,
    CultivarOutput,
    ModelOutput,
    ProcedureOutput,
    ScriptOutput,
    DatasetOutput
)

from typing import List, Annotated, Optional





class ExperimentController(Controller):
    
    # Get Experiments
    @get()
    async def get_experiments(
        self,
        experiment_name: Optional[str] = None,
        experiment_start_date: Optional[date] = None,
        experiment_end_date: Optional[date] = None,
        experiment_info: Optional[str] = None
    ) -> List[ExperimentOutput]:
        try:
            experiments = Experiment.search(
                experiment_name=experiment_name,
                experiment_start_date=experiment_start_date,
                experiment_end_date=experiment_end_date,
                experiment_info=experiment_info
            )
            if experiments is None:
                return Response(content="No experiments found", status_code=404)
            experiments = [experiment.model_dump() for experiment in experiments]
            experiments = [ExperimentOutput.model_validate(experiment) for experiment in experiments]
            return experiments
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Create a new Experiment
    @post()
    async def create_experiment(
        self, data: Annotated[ExperimentInput, Body]
    ) -> ExperimentOutput:
        try:
            experiment = Experiment.create(
                experiment_name=data.experiment_name,
                experiment_info=data.experiment_info,
                experiment_start_date=data.experiment_start_date,
                experiment_end_date=data.experiment_end_date
            )
            if experiment is None:
                return Response(status_code=404)
            return ExperimentOutput.model_validate(experiment.model_dump())
        except Exception as e:
            return Response(content=str(e), status_code=500)
            
    # Get Experiment by Experiment Name
    @get(path="/{experiment_name:str}")
    async def get_experiment_by_name(self, experiment_name: str) -> ExperimentOutput:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                return Response(content="Experiment not found", status_code=404)
            return ExperimentOutput.model_validate(experiment.model_dump())
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Experiment Info by Experiment Name
    @get(path="/{experiment_name:str}/info")
    async def get_experiment_info(self, experiment_name: str) -> dict:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                return Response(content="Experiment not found", status_code=404)
            return experiment.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Set Experiment Info by Experiment Name
    @patch(path="/{experiment_name:str}/info")
    async def set_experiment_info(self, experiment_name: str, data: dict) -> dict:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                return Response(content="Experiment not found", status_code=404)
            experiment.set_info(experiment_info=data)
            return experiment.get_info()
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Experiment Seasons by Experiment Name
    @get(path="/{experiment_name:str}/seasons")
    async def get_experiment_seasons(self, experiment_name: str) -> List[SeasonOutput]:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                return Response(content="Experiment not found", status_code=404)
            seasons = experiment.get_seasons()
            seasons = [season.model_dump() for season in seasons]
            seasons = [SeasonOutput.model_validate(season) for season in seasons]
            return seasons
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Experiment Sites by Experiment Name
    @get(path="/{experiment_name:str}/sites")
    async def get_experiment_sites(self, experiment_name: str) -> List[SiteOutput]:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                return Response(content="Experiment not found", status_code=404)
            sites = experiment.get_sites()
            sites = [site.model_dump() for site in sites]
            sites = [SiteOutput.model_validate(site) for site in sites]
            return sites
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Experiment Sensors by Experiment Name
    @get(path="/{experiment_name:str}/sensors")
    async def get_experiment_sensors(self, experiment_name: str) -> List[SensorOutput]:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                return Response(content="Experiment not found", status_code=404)
            sensors = experiment.get_sensors()
            sensors = [sensor.model_dump() for sensor in sensors]
            sensors = [SensorOutput.model_validate(sensor) for sensor in sensors]
            return sensors
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Experiment Traits by Experiment Name
    @get(path="/{experiment_name:str}/traits")
    async def get_experiment_traits(self, experiment_name: str) -> List[TraitOutput]:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                return Response(content="Experiment not found", status_code=404)
            traits = experiment.get_traits()
            traits = [trait.model_dump() for trait in traits]
            traits = [TraitOutput.model_validate(trait) for trait in traits]
            return traits
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Experiment Resources by Experiment Name
    @get(path="/{experiment_name:str}/resources")
    async def get_experiment_resources(self, experiment_name: str) -> List[ResourceOutput]:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                return Response(content="Experiment not found", status_code=404)
            resources = experiment.get_resources()
            resources = [resource.model_dump() for resource in resources]
            resources = [ResourceOutput.model_validate(resource) for resource in resources]
            return resources
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Experiment Cultivars by Experiment Name
    @get(path="/{experiment_name:str}/cultivars")
    async def get_experiment_cultivars(self, experiment_name: str) -> List[CultivarOutput]:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                return Response(content="Experiment not found", status_code=404)
            cultivars = experiment.get_cultivars()
            cultivars = [cultivar.model_dump() for cultivar in cultivars]
            cultivars = [CultivarOutput.model_validate(cultivar) for cultivar in cultivars]
            return cultivars
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Experiment Datasets by Experiment Name
    @get(path="/{experiment_name:str}/datasets")
    async def get_experiment_datasets(self, experiment_name: str) -> List[DatasetOutput]:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                return Response(content="Experiment not found", status_code=404)
            datasets = experiment.get_datasets()
            datasets = [dataset.model_dump() for dataset in datasets]
            datasets = [DatasetOutput.model_validate(dataset) for dataset in datasets]
            return datasets
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Experiment Scripts by Experiment Name
    @get(path="/{experiment_name:str}/scripts")
    async def get_experiment_scripts(self, experiment_name: str) -> List[ScriptOutput]:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                return Response(content="Experiment not found", status_code=404)
            scripts = experiment.get_scripts()
            scripts = [script.model_dump() for script in scripts]
            scripts = [ScriptOutput.model_validate(script) for script in scripts]
            return scripts
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Experiment Procedures by Experiment Name
    @get(path="/{experiment_name:str}/procedures")
    async def get_experiment_procedures(self, experiment_name: str) -> List[ProcedureOutput]:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                return Response(content="Experiment not found", status_code=404)
            procedures = experiment.get_procedures()
            procedures = [procedure.model_dump() for procedure in procedures]
            procedures = [ProcedureOutput.model_validate(procedure) for procedure in procedures]
            return procedures
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    # Get Experiment Models by Experiment Name
    @get(path="/{experiment_name:str}/models")
    async def get_experiment_models(self, experiment_name: str) -> List[ModelOutput]:
        try:
            experiment = Experiment.get(experiment_name=experiment_name)
            if not experiment:
                return Response(status_code=404)
            models = experiment.get_models()
            models = [model.model_dump() for model in models]
            models = [ModelOutput.model_validate(model) for model in models]
            return models
        except Exception as e:
            return Response(content=str(e), status_code=500)
        
    