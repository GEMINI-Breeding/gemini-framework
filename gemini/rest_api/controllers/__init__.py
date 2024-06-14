from gemini.rest_api.controllers.experiment import ExperimentController
from gemini.rest_api.controllers.season import SeasonController
from gemini.rest_api.controllers.site import SiteController
from gemini.rest_api.controllers.cultivar import CultivarController
from gemini.rest_api.controllers.plot import PlotController
from gemini.rest_api.controllers.trait import TraitController
from gemini.rest_api.controllers.sensor import SensorController

controllers = {
    "experiments": ExperimentController,
    "cultivars": CultivarController,
    "seasons": SeasonController,
    "sites": SiteController,
    "plots": PlotController,
    "traits": TraitController,
    "sensors": SensorController
    # "seasons": SeasonController,
    # "sites": SiteController,
    # "cultivars": CultivarController,
    # "plots": PlotController,
    # "datasets": DatasetController
}