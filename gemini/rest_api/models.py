from pydantic import BaseModel, ValidationError, ConfigDict
from pydantic.types import UUID4
from pydantic.functional_validators import BeforeValidator
from litestar.datastructures import UploadFile
from typing import Any, List, Union, Optional
from typing_extensions import Annotated
from uuid import UUID
from datetime import datetime
import json

def str_to_dict(value: Any) -> dict:
    if isinstance(value, str):
        return json.loads(value)
    return value

JSONB = Annotated[Union[str, dict], BeforeValidator(str_to_dict)]
ID = Union[int, str, UUID]

# Base Model class for all litestar controllers
class RESTAPIBase(BaseModel):

    model_config = ConfigDict(
        protected_namespaces=(),
        arbitrary_types_allowed=True,
        from_attributes=True,
    )

# --------------------------------
# Error Classes
# --------------------------------
class RESTAPIError(RESTAPIBase):
    error: str
    error_description: str

    def to_html(self):
        return f"<h1>{self.error}</h1><p>{self.error_description}</p>"

# --------------------------------
# Paginated Response
# --------------------------------

class PaginatedResponseBase(RESTAPIBase):
    total_records: int
    total_pages: int
    current_page: int
    next_page: Optional[str] = None
    previous_page: Optional[str] = None

# --------------------------------
# File Handling
# --------------------------------

class URLResponse(RESTAPIBase):
    url: str

class FileInformation(RESTAPIBase):
    bucket_name: str
    object_name: str
    last_modified: datetime
    etag: str
    size: int
    content_type: str
    version_id: Optional[str] = None

# --------------------------------
# Experiment Classes
# --------------------------------

class ExperimentInput(RESTAPIBase):
    experiment_name: str
    experiment_info: Optional[JSONB] = {}
    experiment_start_date: Optional[datetime] = None
    experiment_end_date: Optional[datetime] = None

class ExperimentUpdate(RESTAPIBase):
    experiment_name: Optional[str] = None
    experiment_info: Optional[JSONB] = None
    experiment_start_date: Optional[datetime] = None
    experiment_end_date: Optional[datetime] = None

class ExperimentSearch(RESTAPIBase):
    experiment_name: Optional[str] = None
    experiment_info: Optional[JSONB] = None
    experiment_start_date: Optional[datetime] = None
    experiment_end_date: Optional[datetime] = None

class ExperimentOutput(RESTAPIBase):
    id: Optional[ID] = None
    experiment_name: str = None
    experiment_info: Optional[JSONB] = None
    experiment_start_date: Optional[datetime] = None
    experiment_end_date: Optional[datetime] = None



# --------------------------------
# Season Classes
# --------------------------------

class SeasonInput(RESTAPIBase):
    season_name: str
    season_info: Optional[JSONB] = {}
    season_start_date: Optional[datetime] = None
    season_end_date: Optional[datetime] = None
    experiment_name: Optional[str] = None

class SeasonUpdate(RESTAPIBase):
    season_name: Optional[str] = None
    season_info: Optional[JSONB] = None
    season_start_date: Optional[datetime] = None
    season_end_date: Optional[datetime] = None

class SeasonSearch(RESTAPIBase):
    season_name: Optional[str] = None
    season_info: Optional[JSONB] = None
    season_start_date: Optional[datetime] = None
    season_end_date: Optional[datetime] = None
    experiment_name: Optional[str] = None

class SeasonOutput(RESTAPIBase):
    id: Optional[ID] = None
    season_name: Optional[str] = None
    season_info: Optional[JSONB] = None
    season_start_date: Optional[datetime] = None
    season_end_date: Optional[datetime] = None
    experiment_id: Optional[ID] = None



# --------------------------------
# Site Classes
# --------------------------------

class SiteInput(RESTAPIBase):
    site_name: str
    site_city: Optional[str] = None
    site_state: Optional[str] = None
    site_country: Optional[str] = None
    site_info: Optional[JSONB] = {}
    experiment_name: Optional[str] = None

class SiteUpdate(RESTAPIBase):
    site_name: Optional[str] = None
    site_city: Optional[str] = None
    site_state: Optional[str] = None
    site_country: Optional[str] = None
    site_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None

class SiteSearch(RESTAPIBase):
    site_name: Optional[str] = None
    site_city: Optional[str] = None
    site_state: Optional[str] = None
    site_country: Optional[str] = None
    site_info: Optional[JSONB] = None

class SiteOutput(RESTAPIBase):
    id: Optional[ID] = None
    site_name: Optional[str] = None
    site_city: Optional[str] = None
    site_state: Optional[str] = None
    site_country: Optional[str] = None
    site_info: Optional[JSONB] = None

# --------------------------------
# Cultivar Classes
# --------------------------------

class CultivarInput(RESTAPIBase):
    cultivar_population: str
    cultivar_accession: Optional[str] = None
    cultivar_info: Optional[JSONB] = {}
    experiment_name: Optional[str] = None

class CultivarUpdate(RESTAPIBase):
    cultivar_population: Optional[str] = None
    cultivar_accession: Optional[str] = None
    cultivar_info: Optional[JSONB] = None

class CultivarSearch(RESTAPIBase):
    cultivar_population: Optional[str] = None
    cultivar_accession: Optional[str] = None
    cultivar_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None

class CultivarOutput(RESTAPIBase):
    id: Optional[ID] = None
    cultivar_population: Optional[str] = None
    cultivar_accession: Optional[str] = None
    cultivar_info: Optional[JSONB] = None



# --------------------------------
# Data Format Classes
# --------------------------------

class DataFormatInput(RESTAPIBase):
    data_format_name: str
    data_format_mime_type: Optional[str] = None
    data_format_info: Optional[JSONB] = {}

class DataFormatUpdate(RESTAPIBase):
    data_format_name: Optional[str] = None
    data_format_mime_type: Optional[str] = None
    data_format_info: Optional[JSONB] = None

class DataFormatSearch(RESTAPIBase):
    data_format_name: Optional[str] = None
    data_format_mime_type: Optional[str] = None
    data_format_info: Optional[JSONB] = None

class DataFormatOutput(RESTAPIBase):
    id: Optional[ID] = None
    data_format_name: Optional[str] = None
    data_format_mime_type: Optional[str] = None
    data_format_info: Optional[JSONB] = None



# --------------------------------
# Data Type Classes
# --------------------------------

class DataTypeInput(RESTAPIBase):
    data_type_name: str
    data_type_info: Optional[JSONB] = {}

class DataTypeUpdate(RESTAPIBase):
    data_type_name: Optional[str] = None
    data_type_info: Optional[JSONB] = None

class DataTypeSearch(RESTAPIBase):
    data_type_name: Optional[str] = None
    data_type_info: Optional[JSONB] = None

class DataTypeOutput(RESTAPIBase):
    id: Optional[ID] = None
    data_type_name: Optional[str] = None
    data_type_info: Optional[JSONB] = None


# --------------------------------
# Dataset Type Classes
# --------------------------------

class DatasetTypeInput(RESTAPIBase):
    dataset_type_name: str
    dataset_type_info: Optional[JSONB] = {}

class DatasetTypeUpdate(RESTAPIBase):
    dataset_type_name: Optional[str] = None
    dataset_type_info: Optional[JSONB] = None

class DatasetTypeSearch(RESTAPIBase):
    dataset_type_name: Optional[str] = None
    dataset_type_info: Optional[JSONB] = None

class DatasetTypeOutput(RESTAPIBase):
    id: Optional[ID] = None
    dataset_type_name: Optional[str] = None
    dataset_type_info: Optional[JSONB] = None


# ---------------------------------
# Dataset Classes
# ---------------------------------

class DatasetInput(RESTAPIBase):
    dataset_name: str
    collection_date: Optional[datetime] = None
    dataset_info: Optional[JSONB] = {}
    dataset_type_id: Optional[ID] = 0
    experiment_name: Optional[str] = None

class DatasetUpdate(RESTAPIBase):
    dataset_name: Optional[str] = None
    collection_date: Optional[datetime] = None
    dataset_info: Optional[JSONB] = None
    dataset_type_id: Optional[ID] = None

class DatasetSearch(RESTAPIBase):
    dataset_name: Optional[str] = None
    collection_date: Optional[datetime] = None
    dataset_info: Optional[JSONB] = None
    dataset_type_id: Optional[ID] = None
    experiment_name: Optional[str] = None

class DatasetOutput(RESTAPIBase):
    id: Optional[ID] = None
    dataset_name: Optional[str] = None
    collection_date: Optional[datetime] = None
    dataset_info: Optional[JSONB] = None
    dataset_type_id: Optional[ID] = None


# ---------------------------------
# Model Classes
# ---------------------------------

class ModelInput(RESTAPIBase):
    model_name: str
    model_url: Optional[str] = None
    model_info: Optional[JSONB] = {}
    experiment_name: Optional[str] = None

class ModelUpdate(RESTAPIBase):
    model_name: Optional[str] = None
    model_url: Optional[str] = None
    model_info: Optional[JSONB] = None

class ModelSearch(RESTAPIBase):
    model_name: Optional[str] = None
    model_url: Optional[str] = None
    model_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None

class ModelOutput(RESTAPIBase):
    id: Optional[ID] = None
    model_name: Optional[str] = None
    model_url: Optional[str] = None
    model_info: Optional[JSONB] = None


# --------------------------------
# Model Run Classes
# --------------------------------

class ModelRunInput(RESTAPIBase):
    model_name: str
    model_run_info: Optional[JSONB] = {}

class ModelRunUpdate(RESTAPIBase):
    model_run_info: Optional[JSONB] = None

class ModelRunSearch(RESTAPIBase):
    model_name: Optional[str] = None
    model_run_info: Optional[JSONB] = None

class ModelRunOutput(RESTAPIBase):
    id: Optional[ID] = None
    model_name: Optional[str] = None
    model_run_info: Optional[JSONB] = None

# --------------------------------
# Plant Classes
# --------------------------------

class PlantInput(RESTAPIBase):
    plot_id: ID
    plant_number: int
    plant_info: Optional[JSONB] = {}
    cultivar_accession: Optional[str] = None
    cultivar_population: Optional[str] = None

class PlantUpdate(RESTAPIBase):
    plant_number: Optional[int] = None
    plant_info: Optional[JSONB] = None

class PlantSearch(RESTAPIBase):
    plot_id: Optional[ID] = None
    plant_number: Optional[int] = None
    cultivar_accession: Optional[str] = None
    cultivar_population: Optional[str] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None

class PlantOutput(RESTAPIBase):
    id: Optional[ID] = None
    plot_id: Optional[ID] = None
    cultivar_id: Optional[ID] = None
    plant_number: int
    plant_info: Optional[JSONB] = None

# --------------------------------
# Plot Classes
# --------------------------------

class PlotInput(RESTAPIBase):
    plot_number: int
    plot_row_number: int
    plot_column_number: int
    plot_info: Optional[JSONB] = {}
    plot_geometry_info: Optional[JSONB] = {}
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    cultivar_accession: Optional[str] = None
    cultivar_population: Optional[str] = None

class PlotUpdate(RESTAPIBase):
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    plot_info: Optional[JSONB] = None
    plot_geometry_info: Optional[JSONB] = None


class PlotSearch(RESTAPIBase):
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    plot_info: Optional[JSONB] = None
    plot_geometry_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None

class PlotOutput(RESTAPIBase):
    id: Optional[ID] = None
    experiment_id: Optional[ID] = None
    season_id: Optional[ID] = None
    site_id: Optional[ID] = None
    plot_number: int = None
    plot_row_number: int = None
    plot_column_number: int = None
    plot_info: Optional[JSONB] = None
    plot_geometry_info: Optional[JSONB] = None


# --------------------------------
# Procedure Classes
# --------------------------------

class ProcedureInput(RESTAPIBase):
    procedure_name: str
    procedure_info: Optional[JSONB] = {}
    experiment_name: Optional[str] = None

class ProcedureUpdate(RESTAPIBase):
    procedure_info: Optional[JSONB] = None
    procedure_name: Optional[str] = None

class ProcedureSearch(RESTAPIBase):
    procedure_name: Optional[str] = None
    procedure_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None

class ProcedureOutput(RESTAPIBase):
    id: Optional[ID] = None
    procedure_name: str = None
    procedure_info: Optional[JSONB] = None


# --------------------------------
# Procedure Run Classes
# --------------------------------

class ProcedureRunInput(RESTAPIBase):
    procedure_name: str
    procedure_run_info: Optional[JSONB] = {}

class ProcedureRunUpdate(RESTAPIBase):
    procedure_run_info: Optional[JSONB] = None

class ProcedureRunSearch(RESTAPIBase):
    procedure_name: Optional[str] = None
    procedure_run_info: Optional[JSONB] = None

class ProcedureRunOutput(RESTAPIBase):
    id: Optional[ID] = None
    procedure_name: str = None
    procedure_run_info: Optional[JSONB] = None


# --------------------------------
# Script Classes
# --------------------------------

class ScriptInput(RESTAPIBase):
    script_name: str
    script_url: Optional[str] = None
    script_extension: Optional[str] = None
    script_info: Optional[JSONB] = {}
    experiment_name: Optional[str] = None

class ScriptUpdate(RESTAPIBase):
    script_name: Optional[str] = None
    script_url: Optional[str] = None
    script_extension: Optional[str] = None
    script_info: Optional[JSONB] = None

class ScriptSearch(RESTAPIBase):
    script_name: Optional[str] = None
    script_url: Optional[str] = None
    script_extension: Optional[str] = None
    script_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None

class ScriptOutput(RESTAPIBase):
    id: Optional[ID] = None
    script_name: str = None
    script_url: Optional[str] = None
    script_extension: Optional[str] = None
    script_info: Optional[JSONB] = None


# --------------------------------
# Script Run Classes
# --------------------------------

class ScriptRunInput(RESTAPIBase):
    script_name: str
    script_run_info: Optional[JSONB] = {}

class ScriptRunUpdate(RESTAPIBase):
    script_run_info: Optional[JSONB] = None

class ScriptRunSearch(RESTAPIBase):
    script_name: Optional[str] = None
    script_run_info: Optional[JSONB] = None

class ScriptRunOutput(RESTAPIBase):
    id: Optional[ID] = None
    script_name: str = None
    script_run_info: Optional[JSONB] = None

# --------------------------------
# Sensor Platform Classes
# --------------------------------

class SensorPlatformInput(RESTAPIBase):
    sensor_platform_name: str
    sensor_platform_info: Optional[JSONB] = {}
    experiment_name: Optional[str] = None

class SensorPlatformUpdate(RESTAPIBase):
    sensor_platform_name: Optional[str] = None
    sensor_platform_info: Optional[JSONB] = None

class SensorPlatformSearch(RESTAPIBase):
    sensor_platform_name: Optional[str] = None
    sensor_platform_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None

class SensorPlatformOutput(RESTAPIBase):
    id: Optional[ID] = None
    sensor_platform_name: str = None
    sensor_platform_info: Optional[JSONB] = None


# --------------------------------
# Sensor Type Classes
# --------------------------------

class SensorTypeInput(RESTAPIBase):
    sensor_type_name: str
    sensor_type_info: Optional[JSONB] = {}

class SensorTypeUpdate(RESTAPIBase):
    sensor_type_name: Optional[str] = None
    sensor_type_info: Optional[JSONB] = None

class SensorTypeSearch(RESTAPIBase):
    sensor_type_name: Optional[str] = None
    sensor_type_info: Optional[JSONB] = None

class SensorTypeOutput(RESTAPIBase):
    id: Optional[ID] = None
    sensor_type_name: str = None
    sensor_type_info: Optional[JSONB] = None

# --------------------------------
# Sensor Classes
# --------------------------------

class SensorInput(RESTAPIBase):
    sensor_name: str
    sensor_type_id: ID = 0
    sensor_data_type_id: ID = 0 
    sensor_data_format_id: ID = 0
    sensor_info: Optional[JSONB] = {}
    experiment_name: Optional[str] = None
    sensor_platform_name: Optional[str] = None

class SensorUpdate(RESTAPIBase):
    sensor_name: Optional[str] = None
    sensor_type_id: Optional[ID] = None
    sensor_data_type_id: Optional[ID] = None
    sensor_data_format_id: Optional[ID] = None
    sensor_info: Optional[JSONB] = None

class SensorSearch(RESTAPIBase):
    sensor_name: Optional[str] = None
    sensor_type_id: Optional[ID] = None
    sensor_data_type_id: Optional[ID] = None
    sensor_data_format_id: Optional[ID] = None
    sensor_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None
    sensor_platform_name: Optional[str] = None

class SensorOutput(RESTAPIBase):
    id: Optional[ID] = None
    sensor_name: str = None
    sensor_type_id: ID = None
    sensor_data_type_id: ID = None
    sensor_data_format_id: ID = None
    sensor_info: Optional[JSONB] = None

# --------------------------------
# Trait Level Classes
# --------------------------------

class TraitLevelInput(RESTAPIBase):
    trait_level_name: str
    trait_level_info: Optional[JSONB] = {}

class TraitLevelUpdate(RESTAPIBase):
    trait_level_name: Optional[str] = None
    trait_level_info: Optional[JSONB] = None

class TraitLevelSearch(RESTAPIBase):
    trait_level_name: Optional[str] = None
    trait_level_info: Optional[JSONB] = None

class TraitLevelOutput(RESTAPIBase):
    id: Optional[ID] = None
    trait_level_name: str = None
    trait_level_info: Optional[JSONB] = None


# --------------------------------
# Trait Classes
# --------------------------------

class TraitInput(RESTAPIBase):
    trait_name: str
    trait_units: Optional[str] = None
    trait_level_id: ID = 0
    trait_metrics: Optional[JSONB] = None
    trait_info: Optional[JSONB] = {}
    experiment_name: Optional[str] = None

class TraitUpdate(RESTAPIBase):
    trait_name: Optional[str] = None
    trait_units: Optional[str] = None
    trait_level_id: Optional[ID] = None
    trait_metrics: Optional[JSONB] = None
    trait_info: Optional[JSONB] = None

class TraitSearch(RESTAPIBase):
    trait_name: Optional[str] = None
    trait_units: Optional[str] = None
    trait_level_id: Optional[ID] = None
    trait_metrics: Optional[JSONB] = None
    trait_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None

class TraitOutput(RESTAPIBase):
    id: Optional[ID] = None
    trait_name: str = None
    trait_units: Optional[str] = None
    trait_level_id: ID = None
    trait_metrics: Optional[JSONB] = None
    trait_info: Optional[JSONB] = None


# --------------------------------
# Dataset Record Classes
# --------------------------------

class DatasetRecordInput(RESTAPIBase):
    timestamp: datetime
    dataset_name: str
    dataset_data: JSONB
    collection_date: Optional[datetime] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    record_file: Optional[UploadFile] = None
    record_info: Optional[JSONB] = {}

class DatasetRecordSearch(RESTAPIBase):
    dataset_name: Optional[str] = None
    dataset_data: Optional[JSONB] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    collection_date: Optional[datetime] = None
    record_info: Optional[JSONB] = None

class DatasetRecordUpdate(RESTAPIBase):
    dataset_data: Optional[JSONB] = None
    record_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None

class DatasetRecordOutput(RESTAPIBase):
    id: Optional[ID] = None
    timestamp: datetime = None
    collection_date: Optional[datetime] = None
    dataset_id: ID = None
    dataset_name: str = None
    dataset_data: JSONB = None
    experiment_id: Optional[ID] = None
    experiment_name: Optional[str] = None
    season_id: Optional[ID] = None
    season_name: Optional[str] = None
    site_id: Optional[ID] = None
    site_name: Optional[str] = None
    record_file: Optional[str] = None
    record_info: Optional[JSONB] = None


# --------------------------------
# Model Record Classes
# --------------------------------

class ModelRecordInput(RESTAPIBase):
    timestamp: datetime
    dataset_name: str
    model_name: str
    model_data: JSONB
    collection_date: Optional[datetime] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    record_file: Optional[UploadFile] = None
    record_info: Optional[JSONB] = {}

class ModelRecordSearch(RESTAPIBase):
    model_name: Optional[str] = None
    model_data: Optional[JSONB] = None
    dataset_name: Optional[str] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    collection_date: Optional[datetime] = None
    record_info: Optional[JSONB] = None

class ModelRecordUpdate(RESTAPIBase):
    model_data: Optional[JSONB] = None
    record_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None


class ModelRecordOutput(RESTAPIBase):
    id: Optional[ID] = None
    timestamp: datetime = None
    collection_date: Optional[datetime] = None
    dataset_id: ID = None
    dataset_name: str = None
    model_id: ID = None
    model_name: str = None
    model_data: JSONB = None
    experiment_id: Optional[ID] = None
    experiment_name: Optional[str] = None
    season_id: Optional[ID] = None
    season_name: Optional[str] = None
    site_id: Optional[ID] = None
    site_name: Optional[str] = None
    record_file: Optional[str] = None
    record_info: Optional[JSONB] = None


# --------------------------------
# Procedure Record Classes
# --------------------------------

class ProcedureRecordInput(RESTAPIBase):
    timestamp: datetime
    dataset_name: str 
    procedure_name: str
    procedure_data: JSONB
    collection_date: Optional[datetime] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    record_file: Optional[UploadFile] = None
    record_info: Optional[JSONB] = {}

class ProcedureRecordSearch(RESTAPIBase):
    procedure_name: Optional[str] = None
    procedure_data: Optional[JSONB] = None
    dataset_name: Optional[str] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    collection_date: Optional[datetime] = None
    record_info: Optional[JSONB] = None

class ProcedureRecordUpdate(RESTAPIBase):
    procedure_data: Optional[JSONB] = None
    record_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None

class ProcedureRecordOutput(RESTAPIBase):
    id: Optional[ID] = None
    timestamp: datetime = None
    collection_date: Optional[datetime] = None
    dataset_id: ID = None
    dataset_name: str = None
    procedure_id: ID = None
    procedure_name: str = None
    procedure_data: JSONB = None
    experiment_id: Optional[ID] = None
    experiment_name: Optional[str] = None
    season_id: Optional[ID] = None
    season_name: Optional[str] = None
    site_id: Optional[ID] = None
    site_name: Optional[str] = None
    record_file: Optional[str] = None
    record_info: Optional[JSONB] = None

# --------------------------------
# Script Record Classes
# --------------------------------

class ScriptRecordInput(RESTAPIBase):
    timestamp: datetime
    dataset_name: str
    script_name: str
    script_data: JSONB
    collection_date: Optional[datetime] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    record_file: Optional[UploadFile] = None
    record_info: Optional[JSONB] = {}

class ScriptRecordSearch(RESTAPIBase):
    script_name: Optional[str] = None
    script_data: Optional[JSONB] = None
    dataset_name: Optional[str] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    collection_date: Optional[datetime] = None
    record_info: Optional[JSONB] = None

class ScriptRecordUpdate(RESTAPIBase):
    script_data: Optional[JSONB] = None
    record_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None

class ScriptRecordOutput(RESTAPIBase):
    id: Optional[ID] = None
    timestamp: datetime = None
    collection_date: Optional[datetime] = None
    dataset_id: ID = None
    dataset_name: str = None
    script_id: ID = None
    script_name: str = None
    script_data: JSONB = None
    experiment_id: Optional[ID] = None
    experiment_name: Optional[str] = None
    season_id: Optional[ID] = None
    season_name: Optional[str] = None
    site_id: Optional[ID] = None
    site_name: Optional[str] = None
    record_file: Optional[str] = None
    record_info: Optional[JSONB] = None


# --------------------------------
# Sensor Record Classes
# --------------------------------

class SensorRecordInput(RESTAPIBase):
    timestamp: datetime
    sensor_name: str
    sensor_data: JSONB
    collection_date: Optional[datetime] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    record_file: Optional[UploadFile] = None
    record_info: Optional[JSONB] = {}

class SensorRecordSearch(RESTAPIBase):
    sensor_name: Optional[str] = None
    sensor_data: Optional[JSONB] = None
    dataset_name: Optional[str] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    collection_date: Optional[datetime] = None
    record_info: Optional[JSONB] = None

class SensorRecordUpdate(RESTAPIBase):
    sensor_data: Optional[JSONB] = None
    record_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None

class SensorRecordOutput(RESTAPIBase):
    id: Optional[ID] = None
    timestamp: datetime = None
    collection_date: Optional[datetime] = None
    sensor_id: ID = None
    sensor_name: str = None
    sensor_data: JSONB = None
    experiment_id: Optional[ID] = None
    experiment_name: Optional[str] = None
    season_id: Optional[ID] = None
    season_name: Optional[str] = None
    site_id: Optional[ID] = None
    site_name: Optional[str] = None
    plot_id: Optional[ID] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    record_file: Optional[str] = None
    record_info: Optional[JSONB] = None


# --------------------------------
# Trait Record Classes
# --------------------------------

class TraitRecordInput(RESTAPIBase):
    timestamp: datetime
    trait_name: str
    trait_value: float
    collection_date: Optional[datetime] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    record_info: Optional[JSONB] = {}

class TraitRecordSearch(RESTAPIBase):
    trait_name: Optional[str] = None
    trait_value: Optional[float] = None
    dataset_name: Optional[str] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    collection_date: Optional[datetime] = None
    record_info: Optional[JSONB] = None

class TraitRecordUpdate(RESTAPIBase):
    trait_value: Optional[float] = None
    record_info: Optional[JSONB] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None

class TraitRecordOutput(RESTAPIBase):
    id: Optional[ID] = None
    timestamp: datetime = None
    collection_date: Optional[datetime] = None
    trait_id: ID = None
    trait_name: str = None
    trait_value: float = None
    experiment_id: Optional[ID] = None
    experiment_name: Optional[str] = None
    season_id: Optional[ID] = None
    season_name: Optional[str] = None
    site_id: Optional[ID] = None
    site_name: Optional[str] = None
    plot_id: Optional[ID] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    record_info: Optional[JSONB] = None

