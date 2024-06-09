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

    id: Optional[ID] = None

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
    pass



# --------------------------------
# Season Classes
# --------------------------------
class SeasonBase(RESTAPIBase):
    season_name: str
    season_info: Optional[JSONB] = None
    season_start_date: Optional[date] = None
    season_end_date: Optional[date] = None

class SeasonInput(SeasonBase):
    experiment_name: Optional[str] = None

class SeasonSearch(SeasonBase):
    season_name: Optional[str] = None
    experiment_name: Optional[str] = None

class SeasonOutput(SeasonBase):
    pass

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
    experiment_name: Optional[str] = None

class SiteSearch(SiteBase):
    site_name: Optional[str] = None
    experiment_name: Optional[str] = None

class SiteOutput(SiteBase):
    pass

# --------------------------------
# Cultivar Classes
# --------------------------------
class CultivarBase(RESTAPIBase):
    cultivar_population: str
    cultivar_accession: Optional[str] = None
    cultivar_info: Optional[JSONB] = None

class CultivarInput(CultivarBase):
    experiment_name: Optional[str] = None

class CultivarSearch(CultivarBase):
    cultivar_population: Optional[str] = None
    experiment_name: Optional[str] = None

class CultivarOutput(CultivarBase):
    pass

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

class TraitInput(TraitBase):
    experiment_name: Optional[str] = None

class TraitSearch(TraitBase):
    trait_name: Optional[str] = None
    experiment_name: Optional[str] = None

class TraitOutput(TraitBase):
    pass

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
    experiment_name: Optional[str] = None
    sensor_platform_name: Optional[str] = None

class SensorSearch(SensorBase):
    sensor_name: Optional[str] = None
    experiment_name: Optional[str] = None
    sensor_platform_name: Optional[str] = None

class SensorOutput(SensorBase):
    pass

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
    pass

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
    resource_file: Optional[UploadFile] = None
    experiment_name: Optional[str] = None

class ResourceSearch(ResourceBase):
    resource_uri: Optional[str] = None
    resource_file_name: Optional[str] = None
    experiment_name: Optional[str] = None

class ResourceOutput(ResourceBase):
    pass


# --------------------------------
# Model Classes
# --------------------------------
class ModelBase(RESTAPIBase):
    model_name: str
    model_url: Optional[str] = None
    model_info: Optional[JSONB] = None

class ModelInput(ModelBase):
    experiment_name: Optional[str] = None

class ModelSearch(ModelBase):
    model_name: Optional[str] = None
    experiment_name: Optional[str] = None

class ModelOutput(ModelBase):
    pass

# --------------------------------
# Procedure Classes
# --------------------------------
class ProcedureBase(RESTAPIBase):
    procedure_name: str
    procedure_info: Optional[JSONB] = None

class ProcedureInput(ProcedureBase):
    experiment_name: Optional[str] = None

class ProcedureSearch(ProcedureBase):
    procedure_name: Optional[str] = None
    experiment_name: Optional[str] = None

class ProcedureOutput(ProcedureBase):
    pass

# --------------------------------
# Script Classes
# --------------------------------
class ScriptBase(RESTAPIBase):
    script_name: str
    script_url: Optional[str] = None
    script_extension: Optional[str] = None
    script_info: Optional[JSONB] = None

class ScriptInput(ScriptBase):
    experiment_name: Optional[str] = None

class ScriptSearch(ScriptBase):
    script_name: Optional[str] = None
    experiment_name: Optional[str] = None

class ScriptOutput(ScriptBase):
    pass

# --------------------------------
# Dataset Classes
# --------------------------------
class DatasetBase(RESTAPIBase):
    dataset_name: str
    collection_date: Optional[date] = None
    dataset_info: Optional[JSONB] = None
    dataset_type_id: Optional[ID] = None

class DatasetInput(DatasetBase):
    experiment_name: Optional[str] = None

class DatasetSearch(DatasetBase):
    dataset_name: Optional[str] = None
    experiment_name: Optional[str] = None

class DatasetOutput(DatasetBase):
    pass

# --------------------------------
# Record Classes
# --------------------------------
class RecordBase(RESTAPIBase):
    timestamp: datetime
    collection_date: Optional[date] = None
    dataset_name: Optional[str] = None
    experiment_name: Optional[str] = None
    season_name: Optional[str] = None
    site_name: Optional[str] = None
    plot_number: Optional[int] = None
    plot_row_number: Optional[int] = None
    plot_column_number: Optional[int] = None
    record_info: Optional[JSONB] = None

class RecordInput(RecordBase):



    file : Optional[UploadFile] = None

class RecordSearch(RecordBase):
    timestamp: Optional[datetime] = None

class RecordOutput(RecordBase):
    pass

# --------------------------------
# Dataset Record Classes
# --------------------------------

class DatasetRecordBase(RecordBase):
    dataset_data: JSONB

class DatasetRecordInput(RecordInput):
    dataset_data: Optional[JSONB] = None

class DatasetRecordSearch(RecordSearch):
    dataset_name: Optional[str] = None

class DatasetRecordOutput(RecordOutput):
    dataset_data: JSONB

# --------------------------------
# Sensor Record Classes
# --------------------------------
class SensorRecordBase(RecordBase):
    sensor_name: str
    sensor_data: JSONB

class SensorRecordInput(RecordInput):
    sensor_name: str
    sensor_data: Optional[JSONB] = None

class SensorRecordSearch(RecordSearch):
    sensor_name: Optional[str] = None

class SensorRecordOutput(RecordOutput):
    sensor_name: str
    sensor_data: JSONB


# --------------------------------
# Trait Record Classes
# --------------------------------
class TraitRecordBase(RecordBase):
    trait_name: str
    trait_data: JSONB

class TraitRecordInput(RecordInput):
    trait_name: str
    trait_data: Optional[JSONB] = None

class TraitRecordSearch(RecordSearch):
    trait_name: Optional[str] = None

class TraitRecordOutput(RecordOutput):
    trait_name: str
    trait_data: JSONB

# --------------------------------
# Procedure Record Classes
# --------------------------------
class ProcedureRecordBase(RecordBase):
    procedure_name: str
    procedure_data: JSONB

class ProcedureRecordInput(RecordInput):
    procedure_name: str
    procedure_data: Optional[JSONB] = None

class ProcedureRecordSearch(RecordSearch):
    procedure_name: Optional[str] = None

class ProcedureRecordOutput(RecordOutput):
    procedure_name: str
    procedure_data: JSONB

# --------------------------------
# Script Record Classes
# --------------------------------
class ScriptRecordBase(RecordBase):
    script_name: str
    script_data: JSONB

class ScriptRecordInput(RecordInput):
    script_name: str
    script_data: Optional[JSONB] = None

class ScriptRecordSearch(RecordSearch):
    script_name: Optional[str] = None

class ScriptRecordOutput(RecordOutput):
    script_name: str
    script_data: JSONB

# --------------------------------
# Model Record Classes
# --------------------------------
class ModelRecordBase(RecordBase):
    model_name: str
    model_data: JSONB

class ModelRecordInput(RecordInput):
    model_name: str
    model_data: Optional[JSONB] = None

class ModelRecordSearch(RecordSearch):
    model_name: Optional[str] = None

class ModelRecordOutput(RecordOutput):
    model_name: str
    model_data: JSONB
