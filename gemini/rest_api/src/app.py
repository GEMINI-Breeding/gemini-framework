from litestar import Litestar, Router, get
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin, SwaggerRenderPlugin

from gemini.rest_api.controllers import controllers

import os

openapi_config = OpenAPIConfig(
    title="GEMINI REST API",
    version="1.0.0",
    description="REST API for the GEMINI project",
    render_plugins=[SwaggerRenderPlugin()],
)


@get(path="/api", sync_to_thread=False, tags=["GEMINI"])
def root_handler() -> dict:
    return {
        "message": "Welcome to the GEMINI API",
        "author": "Pranav Ghate",
        "version": "1.0.0",
        "email": "pghate@ucdavis.edu",
    }


# Create routers for each controller
routers = []
for key, value in controllers.items():
    router = Router(
        path=f"/api/{key}",
        route_handlers=[value],
        tags=[key.capitalize()],
    )
    routers.append(router)
app = Litestar(route_handlers=[root_handler, *routers], openapi_config=openapi_config)

# Create folder for upload
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Create folder for download
if not os.path.exists("downloads"):
    os.makedirs("downloads")
