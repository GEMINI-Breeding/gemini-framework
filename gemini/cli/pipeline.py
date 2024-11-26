import click
import os, subprocess
from pathlib import Path
from gemini.config.settings import GEMINISettings
from gemini.manager import GEMINIManager

class PipelineCLIContact:
    def __init__(self) -> None:
        self.manager = GEMINIManager()
        self.script_dir = Path(__file__).parent
        self.pipeline_dir = self.script_dir.parent / "pipeline"
        
@click.group()
@click.pass_context
def pipeline(ctx):
    """Pipeline commands"""
    # Initialize the GEMINIManager once and share it across commands
    ctx.obj = PipelineCLIContact()
    print("Pipeline CLI Contact")

@pipeline.command()
@click.pass_obj
def build(pipeline : PipelineCLIContact):
    manager = pipeline.manager
    click.echo(click.style("Building the pipeline", fg="blue"))
    manager.build_pipeline()
    click.echo(click.style("Pipeline built", fg="blue"))

@pipeline.command()
@click.pass_obj
def start(pipeline : PipelineCLIContact):
    manager = pipeline.manager
    click.echo(click.style("Starting the pipeline", fg="blue"))
    manager.start_pipeline()
    click.echo(click.style("Pipeline started", fg="blue"))

@pipeline.command()
@click.pass_obj
def stop(pipeline : PipelineCLIContact):
    manager = pipeline.manager
    click.echo(click.style("Stopping the pipeline", fg="blue"))
    manager.stop_pipeline()
    click.echo(click.style("Pipeline stopped", fg="blue"))

@pipeline.command()
@click.pass_obj
def clean(pipeline : PipelineCLIContact):
    manager = pipeline.manager
    click.echo(click.style("Cleaning the pipeline", fg="blue"))
    manager.clean_pipeline()
    click.echo(click.style("Pipeline cleaned", fg="blue"))


@pipeline.command()
@click.pass_obj
def status(pipeline : PipelineCLIContact):
    manager = pipeline.manager
    click.echo(click.style("Pipeline Status", fg="blue"))
    click.echo(click.style(f"Status: {manager.status}", fg="blue"))

@pipeline.command()
@click.pass_obj
def setup(pipeline : PipelineCLIContact):
    manager = pipeline.manager
    click.echo(click.style("Setting up the pipeline", fg="blue"))

    # Ask for the variables
    vars = environment_setup()

    # Write the variables to the .env file
    vars.create_env_file(f"{pipeline.pipeline_dir}/.env")
    click.echo(click.style(f"Environment variables written to {pipeline.pipeline_dir}/.env", fg="blue"))

    # Apply the settings
    manager.apply_settings(vars)
    click.echo(click.style("Settings applied", fg="blue"))

    # Build the pipeline
    manager.build_pipeline()

    # Start the pipeline
    manager.start_pipeline()

    click.echo(click.style("Pipeline setup complete", fg="blue"))

def environment_setup() -> GEMINISettings:
    """Collect environment settings interactively."""
    settings = GEMINISettings()

    # Asking user for database configuration
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





# @pipeline.command()
# @click.pass_obj
# def start(ctx):
#     manager = ctx.obj["manager"]
#     click.echo(click.style("Starting the pipeline", fg="blue"))
#     manager.start_pipeline()
#     click.echo(click.style("Pipeline started", fg="blue"))

# @pipeline.command()
# @click.pass_obj
# def stop(ctx):
#     manager = ctx.obj["manager"]
#     click.echo(click.style("Stopping the pipeline", fg="blue"))
#     manager.stop_pipeline()
#     click.echo(click.style("Pipeline stopped", fg="blue"))

# @pipeline.command()
# @click.pass_obj
# def clean(ctx):
#     manager = ctx.obj["manager"]
#     click.echo(click.style("Cleaning the pipeline", fg="blue"))
#     manager.clean_pipeline()
#     click.echo(click.style("Pipeline cleaned", fg="blue"))

# @pipeline.command()
# @click.pass_obj
# def setup(ctx):
#     manager = ctx.obj["manager"]
#     click.echo(click.style("Setting up the pipeline", fg="blue"))

#     # Ask for the variables
#     vars = environment_setup()

#     # Write the variables to the .env file
#     vars.create_env_file(f"{PIPELINE_DIR}/.env")
#     click.echo(click.style(f"Environment variables written to {PIPELINE_DIR}/.env", fg="blue"))

#     # Apply the settings
#     manager.apply_settings(vars)
#     click.echo(click.style("Settings applied", fg="blue"))

#     # Build the pipeline
#     manager.build_pipeline()

#     # Start the pipeline
#     manager.start_pipeline()

#     click.echo(click.style("Pipeline setup complete", fg="blue"))

def environment_setup() -> GEMINISettings:
    """Collect environment settings interactively."""
    settings = GEMINISettings()

    # Asking user for database configuration
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

