from gemini.rest_api.controllers.experiment import ExperimentController
from gemini.rest_api.controllers.cultivar import CultivarController
from gemini.rest_api.controllers.plot import PlotController
from gemini.rest_api.controllers.dataset import DatasetController
from gemini.rest_api.controllers.model import ModelController
from gemini.rest_api.controllers.procedure import ProcedureController
from gemini.rest_api.controllers.script import ScriptController
from gemini.rest_api.controllers.season import SeasonController
from gemini.rest_api.controllers.sensor import SensorController
from gemini.rest_api.controllers.site import SiteController
from gemini.rest_api.controllers.trait import TraitController
from gemini.rest_api.controllers.resource import ResourceController

controllers = {
    "experiments": ExperimentController,
    "cultivars": CultivarController,
    "plots": PlotController,
    "datasets": DatasetController,
    "models": ModelController,
    "procedures": ProcedureController,
    "scripts": ScriptController,
    "seasons": SeasonController,
    "sensors": SensorController,
    "sites": SiteController,
    "traits": TraitController,
    "resources": ResourceController,
}
