from gemini.config.settings import GEMINISettings

from prefect import task

@task(  
    name="get_settings",
    description="Get GEMINI settings",
    tags=["settings"],
    retries=3,
    log_prints=True,
)
def get_settings() -> dict:
    settings = GEMINISettings()
    settings = settings.model_dump()
    print(f"Settings: {settings}")
    return settings