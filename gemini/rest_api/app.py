from litestar import Litestar, Router, get
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import StoplightRenderPlugin
from litestar import Litestar
from litestar.config.cors import CORSConfig
from gemini.rest_api.controllers import controllers
# from gemini.rest_api.controllers.files import file_route_handlers
from gemini.config.settings import GEMINISettings

cors_config = CORSConfig(allow_origins=["*"])

openapi_config = OpenAPIConfig(
    title="GEMINI REST API",
    version="1.0.0",
    description="REST API for the GEMINI project",
    render_plugins=[StoplightRenderPlugin()]
)

@get(path="/" , sync_to_thread=False, tags=["GEMINI"])
def root_handler() -> dict:
    return {
        "message": "Welcome to the GEMINI API",
        "author": "Pranav Ghate",
        "version": "1.0.0",
        "email": "pghate@ucdavis.edu"
    }

@get(path="/settings", sync_to_thread=False, tags=["GEMINI"])
def settings_handler() -> dict:
    return GEMINISettings().model_dump()

routers = []
for key, value in controllers.items():
    router = Router(
        path=f"/api/{key}",
        route_handlers=[value],
        tags=[key.replace("_", " ").title()]
    )
    routers.append(router)


# Entry point for the application
app = Litestar(route_handlers=[root_handler, settings_handler ] + routers, openapi_config=openapi_config, cors_config=cors_config)
