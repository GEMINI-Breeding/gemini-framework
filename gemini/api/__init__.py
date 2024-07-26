from gemini.api.data_type import DataType
from gemini.api.data_format import DataFormat
from gemini.api.dataset_type import DatasetType
from gemini.api.dataset import Dataset
from gemini.api.model_run import ModelRun
from gemini.api.model import Model
from gemini.api.cultivar import Cultivar
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.experiment import Experiment
from gemini.api.plant import Plant
from gemini.api.plot import Plot
from gemini.api.procedure import Procedure
from gemini.api.procedure_run import ProcedureRun
from gemini.api.resource import Resource
from gemini.api.script_run import ScriptRun
from gemini.api.script import Script
from gemini.api.sensor_platform import SensorPlatform
from gemini.api.sensor_type import SensorType
from gemini.api.sensor import Sensor
from gemini.api.trait_level import TraitLevel
from gemini.api.trait import Trait

from gemini.api.dataset_record import DatasetRecord
from gemini.api.model_record import ModelRecord
from gemini.api.procedure_record import ProcedureRecord
from gemini.api.script_record import ScriptRecord
from gemini.api.sensor_record import SensorRecord
from gemini.api.trait_record import TraitRecord

from gemini.api.enums import (
    GEMINIDataFormat,
    GEMINIDatasetType,
    GEMINIDataType,
    GEMINISensorType,
    GEMINITraitLevel,
)

models = {
    "cultivar": Cultivar,
    "experiment": Experiment,
    "data_format": DataFormat,
    "data_type": DataType,
    "dataset_type": DatasetType,
    "dataset": Dataset,
    "model_run": ModelRun,
    "model": Model,
    "season": Season,
    "site": Site,
    "plant": Plant,
    "plot": Plot,
    "procedure": Procedure,
    "procedure_run": ProcedureRun,
    "resource": Resource,
    "script_run": ScriptRun,
    "script": Script,
    "sensor_platform": SensorPlatform,
    "sensor_type": SensorType,
    "sensor": Sensor,
    "trait_level": TraitLevel,
    "trait": Trait,
    "dataset_record": DatasetRecord,
    "model_record": ModelRecord,
    "procedure_record": ProcedureRecord,
    "script_record": ScriptRecord,
    "sensor_record": SensorRecord,
    "trait_record": TraitRecord,
}

for model in models.values():
    model.model_rebuild()
    model.update_forward_refs()

