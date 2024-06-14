from gemini.rest_api.controllers.experiment import ExperimentController
from gemini.rest_api.controllers.season import SeasonController
from gemini.rest_api.controllers.site import SiteController
from gemini.rest_api.controllers.cultivar import CultivarController
from gemini.rest_api.controllers.plot import PlotController
from gemini.rest_api.controllers.trait import TraitController
from gemini.rest_api.controllers.sensor import SensorController
from gemini.rest_api.controllers.sensor_platform import SensorPlatformController
from gemini.rest_api.controllers.sensor_record import SensorRecordController
from gemini.rest_api.controllers.trait_record import TraitRecordController

controllers = {
    "experiments": ExperimentController,
    "cultivars": CultivarController,
    "seasons": SeasonController,
    "sites": SiteController,
    "plots": PlotController,
    "traits": TraitController,
    "sensors": SensorController,
    "sensor_platforms": SensorPlatformController,
    "sensor_records": SensorRecordController,
    "trait_records": TraitRecordController
}