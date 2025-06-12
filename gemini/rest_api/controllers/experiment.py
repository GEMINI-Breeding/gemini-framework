from litestar import Response
from litestar.handlers import get, post, patch, delete
from litestar.params import Body
from litestar.controller import Controller

from pydantic import BaseModel

from gemini.api.experiment import Experiment
from gemini.api.enums import GEMINIDataFormat, GEMINIDatasetType, GEMINISensorType, GEMINIDataType, GEMINITraitLevel
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
    DatasetOutput,
)
from typing import List, Annotated, Optional

class ExperimentSeasonInput(BaseModel):
    season_name: str
    season_info: Optional[JSONB] = {}
    season_start_date: Optional[str] = None
    season_end_date: Optional[str] = None

class ExperimentSiteInput(BaseModel):
    site_name: str
    site_info: Optional[JSONB] = {}
    site_city: Optional[str] = None
    site_state: Optional[str] = None
    site_country: Optional[str] = None

class ExperimentCultivarInput(BaseModel):
    cultivar_population: str
    cultivar_accession: Optional[str] = None
    cultivar_info: Optional[JSONB] = {}

class ExperimentSensorPlatformInput(BaseModel):
    sensor_platform_name: str
    sensor_platform_info: Optional[JSONB] = {}

class ExperimentTraitInput(BaseModel):
    trait_name: str
    trait_units: Optional[str] = None
    trait_level_id: Optional[int] = None
    trait_info: Optional[JSONB] = {}
    trait_metrics: Optional[JSONB] = {}

class ExperimentSensorInput(BaseModel):
    sensor_name: str
    sensor_data_type_id: Optional[int] = None
    sensor_data_format_id: Optional[int] = None
    sensor_type_id: Optional[int] = None
    sensor_info: Optional[JSONB] = {}
    sensor_platform_name: Optional[str] = None

class ExperimentScriptInput(BaseModel):
    script_name: str
    script_extension: Optional[str] = None
    script_url: Optional[str] = None
    script_info: Optional[JSONB] = {}

class ExperimentProcedureInput(BaseModel):
    procedure_name: str
    procedure_info: Optional[JSONB] = {}

class ExperimentModelInput(BaseModel):
    model_name: str
    model_url: Optional[str] = None
    model_info: Optional[JSONB] = {}

class ExperimentDatasetInput(BaseModel):
    dataset_name: str
    dataset_info: Optional[JSONB] = {}
    collection_date: Optional[str] = None
    dataset_type_id: Optional[int] = None


class ExperimentController(Controller):

    # Get All Experiments
    @get(path="/all")
    async def get_all_experiments(self) -> List[ExperimentOutput]:
        try:
            experiments = Experiment.get_all()
            if experiments is None:
                error = RESTAPIError(
                    error="No experiments found",
                    error_description="No experiments were found"
                )
                return Response(content=error, status_code=404)
            return experiments
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving all experiments"
            )
            return Response(content=error, status_code=500)

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
                error = RESTAPIError(
                    error="No experiments found",
                    error_description="No experiments were found with the given search criteria"
                )
                return Response(content=error, status_code=404)
            return experiments
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving experiments"
            )
            return Response(content=error, status_code=500)
        
    
    # Get Experiment by ID
    @get(path="/id/{experiment_id:str}")
    async def get_experiment_by_id(
        self, experiment_id: str
    ) -> ExperimentOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            return experiment
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment"
            )
            return Response(content=error, status_code=500)
        

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
                error = RESTAPIError(
                    error="Experiment not created",
                    error_description="The experiment could not be created"
                )
                return Response(content=error, status_code=500)
            return experiment
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the experiment"
            )
            return Response(content=error, status_code=500)
        

    # Update Existing Experiment
    @patch(path="/id/{experiment_id:str}")
    async def update_experiment(
        self, experiment_id: str, data: Annotated[ExperimentUpdate, Body]
    ) -> ExperimentOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error_ = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            experiment = experiment.update(
                experiment_name=data.experiment_name,
                experiment_info=data.experiment_info,
                experiment_start_date=data.experiment_start_date,
                experiment_end_date=data.experiment_end_date
            )
            return experiment
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while updating the experiment"
            )
            return Response(content=error, status_code=500)
        

    # Delete Experiment
    @delete(path="/id/{experiment_id:str}")
    async def delete_experiment(
        self, experiment_id: str
    ) -> None:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            experiment.delete()
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while deleting the experiment"
            )
            return Response(content=error, status_code=500)
    
    # Get Experiment Seasons
    @get(path="/id/{experiment_id:str}/seasons")
    async def get_experiment_seasons(
        self, experiment_id: str
    ) -> List[SeasonOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            seasons = experiment.get_associated_seasons()
            if seasons is None:
                error = RESTAPIError(
                    error="No seasons found",
                    error_description="No seasons were found for the given experiment"
                )
                return Response(content=error, status_code=404)
            return seasons
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment seasons"
            )
            return Response(content=error, status_code=500)
        

    # Create Season for Experiment
    @post(path="/id/{experiment_id:str}/seasons")
    async def create_experiment_season(
        self, experiment_id: str, data: Annotated[ExperimentSeasonInput, Body]
    ) -> SeasonOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            season = experiment.create_new_season(
                season_name=data.season_name,
                season_info=data.season_info,
                season_start_date=data.season_start_date,
                season_end_date=data.season_end_date
            )
            if not season:
                error = RESTAPIError(
                    error="Season not created",
                    error_description="The season could not be created"
                )
                return Response(content=error, status_code=500)
            return season
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the experiment season"
            )
            return Response(content=error, status_code=500)
        

    # Get Experiment Sites
    @get(path="/id/{experiment_id:str}/sites")
    async def get_experiment_sites(
        self, experiment_id: str
    ) -> List[SiteOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            sites = experiment.get_associated_sites()
            if sites is None:
                error = RESTAPIError(
                    error="No sites found",
                    error_description="No sites were found for the given experiment"
                )
                return Response(content=error, status_code=404)
            return sites
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment sites"
            )
            return Response(content=error, status_code=500)
        

    # Create Site for Experiment
    @post(path="/id/{experiment_id:str}/sites")
    async def create_experiment_site(
        self, experiment_id: str, data: Annotated[ExperimentSiteInput, Body]
    ) -> SiteOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            site = experiment.create_new_site(
                site_name=data.site_name,
                site_info=data.site_info,
                site_city=data.site_city,
                site_state=data.site_state,
                site_country=data.site_country
            )
            if not site:
                error = RESTAPIError(
                    error="Site not created",
                    error_description="The site could not be created"
                )
                return Response(content=error, status_code=500)
            return site
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the experiment site"
            )
            return Response(content=error, status_code=500)
        

    # Get Experiment Cultivars
    @get(path="/id/{experiment_id:str}/cultivars")
    async def get_experiment_cultivars(
        self, experiment_id: str
    ) -> List[CultivarOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                ).to_html()
                return Response(content=error, status_code=404)
            cultivars = experiment.get_associated_cultivars()
            if cultivars is None:
                error = RESTAPIError(
                    error="No cultivars found",
                    error_description="No cultivars were found for the given experiment"
                )
                return Response(content=error, status_code=404)
            return cultivars
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment cultivars"
            )
            return Response(content=error, status_code=500)

    
    # Create Cultivar for Experiment
    @post(path="/id/{experiment_id:str}/cultivars")
    async def create_experiment_cultivar(
        self, experiment_id: str, data: Annotated[ExperimentCultivarInput, Body]
    ) -> CultivarOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            cultivar = experiment.create_new_cultivar(
                cultivar_population=data.cultivar_population,
                cultivar_accession=data.cultivar_accession,
                cultivar_info=data.cultivar_info
            )
            if not cultivar:
                error = RESTAPIError(
                    error="Cultivar not created",
                    error_description="The cultivar could not be created"
                )
                return Response(content=error, status_code=500)
            return cultivar
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the experiment cultivar"
            )
            return Response(content=error, status_code=500)
        

    # Get Experiment Sensor Platforms
    @get(path="/id/{experiment_id:str}/sensor_platforms")
    async def get_experiment_sensor_platforms(
        self, experiment_id: str
    ) -> List[SensorPlatformOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            sensor_platforms = experiment.get_associated_sensor_platforms()
            if sensor_platforms is None:
                error = RESTAPIError(
                    error="No sensor platforms found",
                    error_description="No sensor platforms were found for the given experiment"
                )
                return Response(content=error, status_code=404)
            return sensor_platforms
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment sensor platforms"
            )
            return Response(content=error, status_code=500)
        

    # Create Sensor Platform for Experiment
    @post(path="/id/{experiment_id:str}/sensor_platforms")
    async def create_experiment_sensor_platform(
        self, experiment_id: str, data: Annotated[ExperimentSensorPlatformInput, Body]
    ) -> SensorPlatformOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            sensor_platform = experiment.create_new_sensor_platform(
                sensor_platform_name=data.sensor_platform_name,
                sensor_platform_info=data.sensor_platform_info,
            )
            if not sensor_platform:
                error = RESTAPIError(
                    error="Sensor Platform not created",
                    error_description="The sensor platform could not be created"
                )
                return Response(content=error, status_code=500)
            return sensor_platform
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the experiment sensor platform"
            )
            return Response(content=error, status_code=500)
        

    # Get Experiment Traits
    @get(path="/id/{experiment_id:str}/traits")
    async def get_experiment_traits(
        self, experiment_id: str
    ) -> List[TraitOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            traits = experiment.get_associated_traits()
            if traits is None:
                error = RESTAPIError(
                    error="No traits found",
                    error_description="No traits were found for the given experiment"
                )
                return Response(content=error, status_code=404)
            return traits
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment traits"
            )
            return Response(content=error, status_code=500)
        
    # Create Trait for Experiment
    @post(path="/id/{experiment_id:str}/traits")
    async def create_experiment_trait(
        self, experiment_id: str, data: Annotated[ExperimentTraitInput, Body]
    ) -> TraitOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            trait = experiment.create_new_trait(
                trait_name=data.trait_name,
                trait_units=data.trait_units,
                trait_level=GEMINITraitLevel(data.trait_level_id),
                trait_info=data.trait_info,
                trait_metrics=data.trait_metrics
            )
            if not trait:
                error = RESTAPIError(
                    error="Trait not created",
                    error_description="The trait could not be created"
                )
                return Response(content=error, status_code=500)
            return trait
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the experiment trait"
            )
            return Response(content=error, status_code=500)
        

    # Get Experiment Sensors
    @get(path="/id/{experiment_id:str}/sensors")
    async def get_experiment_sensors(
        self, experiment_id: str
    ) -> List[SensorOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            sensors = experiment.get_associated_sensors()
            if sensors is None:
                error = RESTAPIError(
                    error="No sensors found",
                    error_description="No sensors were found for the given experiment"
                )
                return Response(content=error, status_code=404)
            return sensors
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment sensors"
            )
            return Response(content=error, status_code=500)
        
    # Create Sensor for Experiment
    @post(path="/id/{experiment_id:str}/sensors")
    async def create_experiment_sensor(
        self, experiment_id: str, data: Annotated[ExperimentSensorInput, Body]
    ) -> SensorOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            sensor = experiment.create_new_sensor(
                sensor_name=data.sensor_name,
                sensor_data_type=GEMINIDataType(data.sensor_data_type_id),
                sensor_data_format=GEMINIDataFormat(data.sensor_data_format_id),
                sensor_type=GEMINISensorType(data.sensor_type_id),
                sensor_info=data.sensor_info,
                sensor_platform_name=data.sensor_platform_name
            )
            if not sensor:
                error = RESTAPIError(
                    error="Sensor not created",
                    error_description="The sensor could not be created"
                )
                return Response(content=error, status_code=500)
            return sensor
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the experiment sensor"
            )
            return Response(content=error, status_code=500)
        

    # Get Experiment Scripts
    @get(path="/id/{experiment_id:str}/scripts")
    async def get_experiment_scripts(
        self, experiment_id: str
    ) -> List[ScriptOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            scripts = experiment.get_associated_scripts()
            if scripts is None:
                error = RESTAPIError(
                    error="No scripts found",
                    error_description="No scripts were found for the given experiment"
                )
                return Response(content=error, status_code=404)
            return scripts
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment scripts"
            )
            return Response(content=error, status_code=500)
        

    # Create Experiment Script
    @post(path="/id/{experiment_id:str}/scripts")
    async def create_experiment_script(
        self, experiment_id: str, data: Annotated[ExperimentScriptInput, Body]
    ) -> ScriptOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            script = experiment.create_new_script(
                script_name=data.script_name,
                script_extension=data.script_extension,
                script_url=data.script_url,
                script_info=data.script_info
            )
            if not script:
                error = RESTAPIError(
                    error="Script not created",
                    error_description="The script could not be created"
                )
                return Response(content=error, status_code=500)
            return script
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the experiment script"
            )
            return Response(content=error, status_code=500)
        

    # Get Experiment Procedures
    @get(path="/id/{experiment_id:str}/procedures")
    async def get_experiment_procedures(
        self, experiment_id: str
    ) -> List[ProcedureOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            procedures = experiment.get_associated_procedures()
            if procedures is None:
                error = RESTAPIError(
                    error="No procedures found",
                    error_description="No procedures were found for the given experiment"
                )
                return Response(content=error, status_code=404)
            return procedures
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment procedures"
            )
            return Response(content=error, status_code=500)
        

    # Create Experiment Procedure
    @post(path="/id/{experiment_id:str}/procedures")
    async def create_experiment_procedure(
        self, experiment_id: str, data: Annotated[ExperimentProcedureInput, Body]
    ) -> ProcedureOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            procedure = experiment.create_new_procedure(
                procedure_name=data.procedure_name,
                procedure_info=data.procedure_info,
            )
            if not procedure:
                error = RESTAPIError(
                    error="Procedure not created",
                    error_description="The procedure could not be created"
                )
                return Response(content=error, status_code=500)
            return procedure
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the experiment procedure"
            )
            return Response(content=error, status_code=500)
        

    # Get Experiment Models
    @get(path="/id/{experiment_id:str}/models")
    async def get_experiment_models(
        self, experiment_id: str
    ) -> List[ModelOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            models = experiment.get_associated_models()
            if models is None:
                error = RESTAPIError(
                    error="No models found",
                    error_description="No models were found for the given experiment"
                )
                return Response(content=error, status_code=404)
            return models
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment models"
            )
            return Response(content=error, status_code=500)
        

    # Create Experiment Model
    @post(path="/id/{experiment_id:str}/models")
    async def create_experiment_model(
        self, experiment_id: str, data: Annotated[ExperimentModelInput, Body]
    ) -> ModelOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            model = experiment.create_new_model(
                model_name=data.model_name,
                model_info=data.model_info,
                model_url=data.model_url
            )
            if not model:
                error = RESTAPIError(
                    error="Model not created",
                    error_description="The model could not be created"
                )
                return Response(content=error, status_code=500)
            return model
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the experiment model"
            )
            return Response(content=error, status_code=500)
        

    # Get Experiment Datasets
    @get(path="/id/{experiment_id:str}/datasets")
    async def get_experiment_datasets(
        self, experiment_id: str
    ) -> List[DatasetOutput]:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_description="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            datasets = experiment.get_associated_datasets()
            if datasets is None:
                error = RESTAPIError(
                    error="No datasets found",
                    error_description="No datasets were found for the given experiment"
                )
                return Response(content=error, status_code=404)
            return datasets
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while retrieving the experiment datasets"
            )
            return Response(content=error, status_code=500)
        

    # Create Dataset for Experiment
    @post(path="/id/{experiment_id:str}/datasets")
    async def create_experiment_dataset(
        self, experiment_id: str, data: Annotated[ExperimentDatasetInput, Body]
    ) -> DatasetOutput:
        try:
            experiment = Experiment.get_by_id(id=experiment_id)
            if experiment is None:
                error = RESTAPIError(
                    error="Experiment not found",
                    error_descripion="No experiment was found with the given ID"
                )
                return Response(content=error, status_code=404)
            dataset = experiment.create_new_dataset(
                dataset_name=data.dataset_name,
                dataset_info=data.dataset_info,
                dataset_type=GEMINIDatasetType(data.dataset_type_id),
                collection_date=data.collection_date
            )
            if not dataset:
                error = RESTAPIError(
                    error="Dataset not created",
                    error_description="The dataset could not be created"
                )
                return Response(content=error, status_code=500)
            return dataset
        except Exception as e:
            error = RESTAPIError(
                error=str(e),
                error_description="An error occurred while creating the experiment dataset"
            )
            return Response(content=error, status_code=500)
            
        

    
        