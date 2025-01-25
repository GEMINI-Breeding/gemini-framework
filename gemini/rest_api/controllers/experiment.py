from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from gemini.api.experiment import Experiment
from gemini.rest_api.models import ExperimentInput, ExperimentOutput, ExperimentUpdate, RESTAPIError, str_to_dict, JSONB
from gemini.rest_api.models import (
    SeasonOutput,
    SiteOutput,
    CultivarOutput,
    SensorPlatformOutput,
    TraitOutput,
    SensorOutput,
    ScriptOutput,
    ProcedureOutput,
    ModelOutput,
    DatasetOutput
)
from typing import List, Annotated, Optional


class ExperimentController(Controller):

    # Get Experiments
    @get()
    async def get_experiments(
        self,
        experiment_name: Optional[str] = None,
        experiment_info: Optional[JSONB] = None,
        experiment_start_date: Optional[str] = None,
        experiment_end_date: Optional[str] = None
    ) -> List[ExperimentOutput]:
        try:

            if experiment_info is not None:
                experiment_info = str_to_dict(experiment_info)

            experiments = Experiment.search(
                experiment_name=experiment_name,
                experiment_info=experiment_info,
                experiment_start_date=experiment_start_date,
                experiment_end_date=experiment_end_date
            )
            if experiments is None:
                error_html = RESTAPIError(
                    error="No experiments found",
                    error_description="No experiments were found with the given search criteria"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return experiments
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving experiments"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        
    
    # Get Experiment by ID
    @get(path="/id/{experiment_id:str}")
    async def get_experiment_by_id(
        self, experiment_id: str
    ) -> ExperimentOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return experiment
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Create Experiment
    @post()
    async def create_experiment(
        self, data: Annotated[ExperimentInput, Body]
    ) -> ExperimentOutput:
        try:
            experiment = Experiment.create(
                experiment_name=data.experiment_name,
                experiment_info=data.experiment_info,
                experiment_start_date=data.experiment_start_date,
                experiment_end_date=data.experiment_end_date,
            )
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not created",
                    error_description="The experiment could not be created"
                ).to_html()
                return Response(content=error_html, status_code=500)
            return experiment
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the experiment"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Update Existing Experiment
    @patch(path="/id/{experiment_id:str}")
    async def update_experiment(
        self, experiment_id: str, data: Annotated[ExperimentUpdate, Body]
    ) -> ExperimentOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            parameters = data.model_dump()
            experiment = experiment.update(**parameters)
            return experiment
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the experiment"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Delete Experiment
    @delete(path="/id/{experiment_id:str}")
    async def delete_experiment(
        self, experiment_id: str
    ) -> None:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            experiment.delete()
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the experiment"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
    
    # Get Experiment Seasons
    @get(path="/id/{experiment_id:str}/seasons")
    async def get_experiment_seasons(
        self, experiment_id: str
    ) -> List[SeasonOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            seasons = experiment.get_seasons()
            if seasons is None:
                error_html = RESTAPIError(
                    error="No seasons found",
                    error_description="No seasons were found for the given experiment"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return seasons
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment seasons"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Experiment Sites
    @get(path="/id/{experiment_id:str}/sites")
    async def get_experiment_sites(
        self, experiment_id: str
    ) -> List[SiteOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            sites = experiment.get_sites()
            if sites is None:
                error_html = RESTAPIError(
                    error="No sites found",
                    error_description="No sites were found for the given experiment"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return sites
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment sites"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Experiment Cultivars
    @get(path="/id/{experiment_id:str}/cultivars")
    async def get_experiment_cultivars(
        self, experiment_id: str
    ) -> List[CultivarOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            cultivars = experiment.get_cultivars()
            if cultivars is None:
                error_html = RESTAPIError(
                    error="No cultivars found",
                    error_description="No cultivars were found for the given experiment"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return cultivars
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment cultivars"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Experiment Sensor Platforms
    @get(path="/id/{experiment_id:str}/sensor_platforms")
    async def get_experiment_sensor_platforms(
        self, experiment_id: str
    ) -> List[SensorPlatformOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            sensor_platforms = experiment.get_sensor_platforms()
            if sensor_platforms is None:
                error_html = RESTAPIError(
                    error="No sensor platforms found",
                    error_description="No sensor platforms were found for the given experiment"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return sensor_platforms
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment sensor platforms"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Experiment Traits
    @get(path="/id/{experiment_id:str}/traits")
    async def get_experiment_traits(
        self, experiment_id: str
    ) -> List[TraitOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            traits = experiment.get_traits()
            if traits is None:
                error_html = RESTAPIError(
                    error="No traits found",
                    error_description="No traits were found for the given experiment"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return traits
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment traits"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Experiment Sensors
    @get(path="/id/{experiment_id:str}/sensors")
    async def get_experiment_sensors(
        self, experiment_id: str
    ) -> List[SensorOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            sensors = experiment.get_sensors()
            if sensors is None:
                error_html = RESTAPIError(
                    error="No sensors found",
                    error_description="No sensors were found for the given experiment"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return sensors
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment sensors"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Experiment Scripts
    @get(path="/id/{experiment_id:str}/scripts")
    async def get_experiment_scripts(
        self, experiment_id: str
    ) -> List[ScriptOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            scripts = experiment.get_scripts()
            if scripts is None:
                error_html = RESTAPIError(
                    error="No scripts found",
                    error_description="No scripts were found for the given experiment"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return scripts
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment scripts"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Experiment Procedures
    @get(path="/id/{experiment_id:str}/procedures")
    async def get_experiment_procedures(
        self, experiment_id: str
    ) -> List[ProcedureOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            procedures = experiment.get_procedures()
            if procedures is None:
                error_html = RESTAPIError(
                    error="No procedures found",
                    error_description="No procedures were found for the given experiment"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return procedures
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment procedures"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Experiment Models
    @get(path="/id/{experiment_id:str}/models")
    async def get_experiment_models(
        self, experiment_id: str
    ) -> List[ModelOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            models = experiment.get_models()
            if models is None:
                error_html = RESTAPIError(
                    error="No models found",
                    error_description="No models were found for the given experiment"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return models
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment models"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        

    # Get Experiment Datasets
    @get(path="/id/{experiment_id:str}/datasets")
    async def get_experiment_datasets(
        self, experiment_id: str
    ) -> List[DatasetOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_html = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error_html, status_code=404)
            datasets = experiment.get_datasets()
            if datasets is None:
                error_html = RESTAPIError(
                    error="No datasets found",
                    error_description="No datasets were found for the given experiment"
                ).to_html()
                return Response(content=error_html, status_code=404)
            return datasets
        except Exception as e:
            error_message = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment datasets"
            )
            error_html = error_message.to_html()
            return Response(content=error_html, status_code=500)
        