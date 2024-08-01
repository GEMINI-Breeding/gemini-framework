
from gemini.server.rest_api.controllers.experiment import ExperimentController
from gemini.server.rest_api.controllers.season import SeasonController
from gemini.server.rest_api.controllers.site import SiteController
from gemini.server.rest_api.controllers.cultivar import CultivarController
from gemini.server.rest_api.controllers.plot import PlotController
from gemini.server.rest_api.controllers.trait import TraitController
from gemini.server.rest_api.controllers.sensor import SensorController
from gemini.server.rest_api.controllers.sensor_platform import SensorPlatformController
from gemini.server.rest_api.controllers.sensor_record import SensorRecordController
# from gemini.server.rest_api.controllers.trait_record import TraitRecordController
# from gemini.rest_api.controllers.system import SystemController

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
    # "trait_records": TraitRecordController,
    # "system": SystemController
}