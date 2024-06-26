from pydantic import BaseModel, ValidationError, ConfigDict
from pydantic import validator
from pydantic.types import UUID4
from pydantic.functional_validators import AfterValidator, BeforeValidator

from litestar.datastructures import UploadFile
from litestar.response import Stream, File

from typing import Any, List, Union, Optional
from typing_extensions import Annotated

from uuid import UUID

import json
from datetime import datetime, date

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
    )

    

# --------------------------------
# Experiment Classes
# --------------------------------
class ExperimentBase(BaseModel):
    experiment_name: str
    experiment_info: Optional[JSONB] = None
    experiment_start_date: Optional[date] = None
    experiment_end_date: Optional[date] = None

class ExperimentInput(ExperimentBase):
    pass

class ExperimentSearch(ExperimentBase):
    experiment_name: Optional[str] = None

class ExperimentOutput(ExperimentBase):
    id: Optional[ID] = None


# --------------------------------
# Season Classes
# --------------------------------
class SeasonBase(RESTAPIBase):
    season_name: str
    season_info: Optional[JSONB] = None
    season_start_date: Optional[date] = None
    season_end_date: Optional[date] = None

class SeasonInput(SeasonBase):
    experiment_name: str = 'Default'

class SeasonSearch(SeasonBase):
    season_name: Optional[str] = None
    experiment_name: Optional[str] = None

class SeasonOutput(SeasonBase):
    id: Optional[ID] = None

# --------------------------------
# Site Classes
# --------------------------------
class SiteBase(RESTAPIBase):
    site_name: str
    site_city: Optional[str] = None
    site_state: Optional[str] = None
    site_country: Optional[str] = None
    site_info: Optional[JSONB] = None

class SiteInput(SiteBase):
    experiment_name: str = 'Default'
    
    
class SiteSearch(SiteBase):
    site_name: Optional[str] = None
    experiment_name: Optional[str] = None

class SiteOutput(SiteBase):
    id: Optional[ID] = None

# --------------------------------
# Cultivar Classes
# --------------------------------
class CultivarBase(RESTAPIBase):
    cultivar_population: str
    cultivar_accession: Optional[str] = None
    cultivar_info: Optional[JSONB] = None

class CultivarInput(CultivarBase):
    experiment_name: str = 'Default'

class CultivarSearch(CultivarBase):
    cultivar_population: Optional[str] = None
    experiment_name: Optional[str] = None

class CultivarOutput(CultivarBase):
    id: Optional[ID] = None

# --------------------------------
# Plot Classes
# --------------------------------
class PlotBase(RESTAPIBase):
    plot_number: int
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    plot_geometry_info: Optional[JSONB] = None
    plot_info: Optional[JSONB] = None

class PlotInput(PlotBase):
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    cultivar_accession: Optional[str] = None
    cultivar_population: Optional[str] = None
    

class PlotSearch(PlotBase):
    plot_number: Optional[int] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    cultivar_accession: Optional[str] = None
    cultivar_population: Optional[str] = None

class PlotOutput(PlotBase):
    id : Optional[ID] = None
    
    experiment_id: Optional[ID] = None
    season_id: Optional[ID] = None
    site_id: Optional[ID] = None

    experiment: Optional[ExperimentOutput] = None
    season: Optional[SeasonOutput] = None
    site: Optional[SiteOutput] = None


# --------------------------------
# Trait Classes
# --------------------------------
class TraitBase(RESTAPIBase):
    trait_name: str
    trait_units: Optional[str] = None
    trait_level_id: Optional[ID] = None
    trait_metrics: Optional[JSONB] = None
    trait_info: Optional[JSONB] = None

class TraitInput(TraitBase):
    experiment_name: str = 'Default'

class TraitSearch(TraitBase):
    trait_name: Optional[str] = None
    experiment_name: Optional[str] = None

class TraitOutput(TraitBase):
    id : Optional[ID] = None

# --------------------------------
# Sensor Classes
# --------------------------------
class SensorBase(RESTAPIBase):
    sensor_name: str
    sensor_platform_id: Optional[ID] = None
    sensor_type_id: Optional[ID] = None
    sensor_data_type_id: Optional[ID] = None
    sensor_data_format_id: Optional[ID] = None
    sensor_info: Optional[JSONB] = None

class SensorInput(SensorBase):
    experiment_name: str = 'Default'
    sensor_platform_name: str = 'Default'

class SensorSearch(SensorBase):
    sensor_name: Optional[str] = None
    experiment_name: Optional[str] = None
    sensor_platform_name: Optional[str] = None

class SensorOutput(SensorBase):
    id : Optional[ID] = None

# --------------------------------
# Sensor Platform Classes
# --------------------------------
class SensorPlatformBase(RESTAPIBase):
    sensor_platform_name: str
    sensor_platform_info: Optional[JSONB] = None

class SensorPlatformInput(SensorPlatformBase):
    pass

class SensorPlatformSearch(SensorPlatformBase):
    sensor_platform_name: Optional[str] = None

class SensorPlatformOutput(SensorPlatformBase):
    id : Optional[ID] = None

# --------------------------------
# Resource Classes
# --------------------------------
class ResourceBase(RESTAPIBase):
    resource_uri: str
    resource_file_name: Optional[str] = None
    is_external: Optional[bool] = None
    resource_info: Optional[JSONB] = None
    resource_data_format_id: Optional[ID] = None
    resource_experiment_id: Optional[ID] = None

class ResourceInput(ResourceBase):
    experiment_name: str = 'Default'
    resource_file: Optional[UploadFile] = None

class ResourceSearch(ResourceBase):
    resource_uri: Optional[str] = None
    resource_file_name: Optional[str] = None
    experiment_name: Optional[str] = None

class ResourceOutput(ResourceBase):
    id : Optional[ID] = None


# --------------------------------
# Model Classes
# --------------------------------
class ModelBase(RESTAPIBase):
    model_name: str
    model_url: Optional[str] = None
    model_info: Optional[JSONB] = None

class ModelInput(ModelBase):
    experiment_name: str = 'Default'

class ModelSearch(ModelBase):
    model_name: Optional[str] = None
    experiment_name: Optional[str] = None

class ModelOutput(ModelBase):
    id : Optional[ID] = None

# --------------------------------
# Procedure Classes
# --------------------------------
class ProcedureBase(RESTAPIBase):
    procedure_name: str
    procedure_info: Optional[JSONB] = None

class ProcedureInput(ProcedureBase):
    experiment_name: str = 'Default'

class ProcedureSearch(ProcedureBase):
    procedure_name: Optional[str] = None
    experiment_name: Optional[str] = None

class ProcedureOutput(ProcedureBase):
    id : Optional[ID] = None

# --------------------------------
# Script Classes
# --------------------------------
class ScriptBase(RESTAPIBase):
    script_name: str
    script_url: Optional[str] = None
    script_extension: Optional[str] = None
    script_info: Optional[JSONB] = None

class ScriptInput(ScriptBase):
    experiment_name: str = 'Default'

class ScriptSearch(ScriptBase):
    script_name: Optional[str] = None
    experiment_name: Optional[str] = None

class ScriptOutput(ScriptBase):
    id : Optional[ID] = None

# --------------------------------
# Dataset Classes
# --------------------------------
class DatasetBase(RESTAPIBase):
    dataset_name: str
    collection_date: Optional[date] = None
    dataset_info: Optional[JSONB] = None
    dataset_type_id: Optional[ID] = None

class DatasetInput(DatasetBase):
    experiment_name: str = 'Default'

class DatasetSearch(DatasetBase):
    dataset_name: Optional[str] = None
    experiment_name: Optional[str] = None

class DatasetOutput(DatasetBase):
    id: Optional[ID] = None

# --------------------------------
# Record Classes
# --------------------------------

class RecordBase(RESTAPIBase):
    timestamp: datetime
    collection_date: Optional[date] = None
    record_info: Optional[JSONB] = None
    
class RecordInput(RecordBase):
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    
class RecordSearch(RecordBase):
    timestamp: Optional[datetime] = None
    collection_date: Optional[date] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    record_info: Optional[JSONB] = None
    
class RecordOutput(RecordBase):
    id: Optional[ID] = None

# --------------------------------
# Dataset Record Classes
# --------------------------------

class DatasetRecordBase(RecordBase):

    dataset_id: ID
    dataset_name: str
    dataset_data: JSONB
    
class DatasetRecordInput(RecordInput):
    dataset_name: str
    dataset_data: JSONB
    
class DatasetRecordSearch(RecordSearch):
    dataset_id: Optional[ID] = None
    dataset_name: Optional[str] = None
    
class DatasetRecordOutput(DatasetRecordBase):
    id: Optional[ID] = None

# --------------------------------
# Sensor Record Classes
# --------------------------------

class SensorRecordBase(RecordBase):
    sensor_id: ID
    sensor_name: str
    sensor_data: JSONB
    
class SensorRecordInput(RecordInput):
    sensor_name: str
    sensor_data: Optional[JSONB] = None
    dataset_name: Optional[str] = None
    file: Optional[UploadFile] = None
    
class SensorRecordSearch(RecordSearch):
    sensor_id: Optional[ID] = None
    sensor_name: Optional[str] = None
    dataset_name: Optional[str] = None
    
class SensorRecordOutput(SensorRecordBase):
    id: Optional[ID] = None

# --------------------------------
# Trait Record Classes
# --------------------------------

class TraitRecordBase(RecordBase):
    trait_id: ID
    trait_name: str
    trait_value: float
    
class TraitRecordInput(RecordInput):
    trait_name: str
    trait_value: float
    dataset_name: Optional[str] = None
    
class TraitRecordSearch(RecordSearch):
    trait_id: Optional[ID] = None
    trait_name: Optional[str] = None
    dataset_name: Optional[str] = None
    
class TraitRecordOutput(TraitRecordBase):
    id: Optional[ID] = None
