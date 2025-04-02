from prefect import flow

from gemini.scheduler.tasks.settings import get_settings

@flow(
    name="get_settings",
    description="Get GEMINI settings",
    retries=3,
    log_prints=True,
)
def get_settings_flow() -> dict:
    return get_settings() 

settings_flow_deployments = [
    get_settings_flow.to_deployment(
        name="get_settings_flow",
        description="Get GEMINI settings",
        tags=["settings"],
    ),
]