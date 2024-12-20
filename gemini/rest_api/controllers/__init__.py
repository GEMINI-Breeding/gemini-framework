from gemini.rest_api.controllers.cultivar import CultivarController
from gemini.rest_api.controllers.data_format import DataFormatController
from gemini.rest_api.controllers.data_type import DataTypeController
from gemini.rest_api.controllers.dataset_type import DatasetTypeController

controllers = {
    "cultivars": CultivarController,
    "data_formats": DataFormatController,
    "data_types": DataTypeController,
    "dataset_types": DatasetTypeController,
}

