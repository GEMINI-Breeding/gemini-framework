import click
from pathlib import Path

from gemini.config.settings import GEMINISettings

SCRIPT_DIR = Path(__file__).parent
PIPELINE_DIR = SCRIPT_DIR.parent / "pipeline"

@click.group()
def pipeline():
    pass

@pipeline.command()
def build():
    pass

@pipeline.command()
def start():
    pass

@pipeline.command()
def stop():
    pass

@pipeline.command()
def clean():
    pass

@pipeline.command()
def setup():
    click.echo(click.style("Setting up the pipeline", fg="green"))
    # Ask for the variables
    vars = environment_setup()
    # Write the variables to the .env file
    vars.create_env_file(f"{PIPELINE_DIR}/.env")
    # 
    




def environment_setup() -> GEMINISettings:

    settings = GEMINISettings()

    # Asking user for database configuration
    # GEMINI Database Configuration
    click.echo(click.style("GEMINI Database Configuration", fg="green"))
    settings.GEMINI_DB_USER = click.prompt("Enter the database user", default="gemini")
    settings.GEMINI_DB_PASSWORD = click.prompt("Enter the database password", default="gemini")
    settings.GEMINI_DB_NAME = click.prompt("Enter the database name", default="gemini")

    # GEMINI Logger Configuration
    click.echo(click.style("GEMINI Logger Configuration", fg="green"))
    settings.GEMINI_LOGGER_PASSWORD = click.prompt("Enter the logger password", default="gemini")

    # GEMINI File Store
    click.echo(click.style("GEMINI File Store", fg="green"))
    settings.GEMINI_STORAGE_ROOT_USER = click.prompt("Enter the storage root user", default="gemini_root")
    settings.GEMINI_STORAGE_ROOT_PASSWORD = click.prompt("Enter the storage root password", default="gemini_root")
    settings.GEMINI_STORAGE_ACCESS_KEY = click.prompt("Enter the storage access key", default="gemini_storage_user")
    settings.GEMINI_STORAGE_SECRET_KEY = click.prompt("Enter the storage secret", default="gemini_secret")

    return settings


# # GEMINI Database Configuration
# GEMINI_DB_CONTAINER_NAME=gemini-db
# GEMINI_DB_IMAGE_NAME=gemini/db
# GEMINI_DB_USER=gemini
# GEMINI_DB_PASSWORD=gemini
# GEMINI_DB_HOSTNAME=gemini-db
# GEMINI_DB_NAME=gemini
# GEMINI_DB_PORT=5432

# # GEMINI Logger Configuration
# GEMINI_LOGGER_CONTAINER_NAME=gemini-logger
# GEMINI_LOGGER_IMAGE_NAME=gemini/logger
# GEMINI_LOGGER_HOSTNAME=gemini-logger
# GEMINI_LOGGER_PORT=6379
# GEMINI_LOGGER_PASSWORD=gemini

# # GEMINI File Store
# GEMINI_STORAGE_CONTAINER_NAME=gemini-storage
# GEMINI_STORAGE_IMAGE_NAME=gemini/storage
# GEMINI_STORAGE_HOSTNAME=gemini-storage
# GEMINI_STORAGE_PORT=9000
# GEMINI_STORAGE_API_PORT=9001
# GEMINI_STORAGE_ROOT_USER=gemini_root
# GEMINI_STORAGE_ROOT_PASSWORD=gemini_root
# GEMINI_STORAGE_ACCESS_KEY=gemini_storage_user
# GEMINI_STORAGE_SECRET_KEY=gemini_secret
# GEMINI_STORAGE_BUCKET_NAME=gemini

