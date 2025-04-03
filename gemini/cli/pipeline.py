import click
import os, subprocess
from pathlib import Path
from gemini.config.settings import GEMINISettings
from gemini.manager import GEMINIManager

class PipelineCLIContext:
    def __init__(self) -> None:
        self.manager = GEMINIManager()
        self.script_dir = Path(__file__).parent
        self.pipeline_dir = self.script_dir.parent / "pipeline"
        
@click.group()
@click.pass_context
def pipeline(ctx):
    """Pipeline commands"""
    # Initialize the GEMINIManager once and share it across commands
    ctx.obj = PipelineCLIContext()
    print("Pipeline CLI Contact")

@pipeline.command()
@click.pass_obj
def build(pipeline : PipelineCLIContext):
    manager = pipeline.manager
    click.echo(click.style("Building the pipeline", fg="blue"))
    manager.build_pipeline()
    click.echo(click.style("Pipeline built", fg="blue"))

@pipeline.command()
@click.pass_obj
def start(pipeline : PipelineCLIContext):
    manager = pipeline.manager
    click.echo(click.style("Starting the pipeline", fg="blue"))
    manager.start_pipeline()
    click.echo(click.style("Pipeline started", fg="blue"))

@pipeline.command()
@click.pass_obj
def stop(pipeline : PipelineCLIContext):
    manager = pipeline.manager
    click.echo(click.style("Stopping the pipeline", fg="blue"))
    manager.stop_pipeline()
    click.echo(click.style("Pipeline stopped", fg="blue"))

@pipeline.command()
@click.pass_obj
def clean(pipeline : PipelineCLIContext):
    manager = pipeline.manager
    click.echo(click.style("Cleaning the pipeline", fg="blue"))
    manager.clean_pipeline()
    click.echo(click.style("Pipeline cleaned", fg="blue"))


@pipeline.command()
@click.pass_obj
def reset(pipeline : PipelineCLIContext):
    manager = pipeline.manager
    click.echo(click.style("Resetting the pipeline", fg="blue"))
    manager.stop_pipeline()
    click.echo(click.style("Pipeline reset", fg="blue"))
    manager.clean_pipeline()
    manager.start_pipeline()
    click.echo(click.style("Pipeline started", fg="blue"))

@pipeline.command()
@click.option('--force-rebuild', is_flag=True, help="Force rebuild the pipeline")
@click.pass_obj
def restart(pipeline : PipelineCLIContext, force_rebuild: bool = False):

    manager = pipeline.manager
    click.echo(click.style("Restarting the pipeline", fg="blue"))
    manager.stop_pipeline()
    if force_rebuild:
        manager.rebuild_pipeline()
    click.echo(click.style("Pipeline stopped", fg="blue"))
    manager.start_pipeline()
    click.echo(click.style("Pipeline started", fg="blue"))



@pipeline.command()
@click.pass_obj
def status(pipeline : PipelineCLIContext):
    manager = pipeline.manager
    status = manager.get_status()
    click.echo(click.style(f"Pipeline status: {status}", fg="blue"))
    

@pipeline.command()
@click.option('--default', is_flag=True, help="Use default settings")
@click.pass_obj
def setup(pipeline : PipelineCLIContext, default: bool = False):
    manager = pipeline.manager
    click.echo(click.style("Setting up the pipeline", fg="blue"))

    # Ask for the variables
    vars = environment_setup(default=default)

    # Write the variables to the .env file
    vars.create_env_file(f"{pipeline.pipeline_dir}/.env")
    click.echo(click.style(f"Environment variables written to {pipeline.pipeline_dir}/.env", fg="blue"))

    # Apply the settings
    manager.apply_settings(vars)
    click.echo(click.style("Settings applied", fg="blue"))

    # Build the pipeline
    manager.build_pipeline()

    click.echo(click.style("Pipeline setup complete", fg="blue"))


@pipeline.command()
@click.argument('domain')
@click.pass_obj
def set_domain(pipeline : PipelineCLIContext, domain: str):
    manager = pipeline.manager
    click.echo(click.style(f"Setting domain to {domain}", fg="blue"))
    
    # Load current settings from env file
    current_settings = GEMINISettings.from_env_file(f"{pipeline.pipeline_dir}/.env")

    # Change the domain in the settings
    current_settings.GEMINI_DOMAIN = domain

    # Write the updated settings back to the env file
    current_settings.create_env_file(f"{pipeline.pipeline_dir}/.env")

    # Apply the settings
    manager.apply_settings(current_settings)
    click.echo(click.style("Domain updated", fg="blue"))

    # Restart the pipeline with the new domain and force rebuild
    manager.rebuild_pipeline()
    manager.start_pipeline()

    click.echo(click.style("Pipeline restarted with new domain", fg="blue"))

def environment_setup(default: bool = False) -> GEMINISettings:
    """Collect environment settings interactively."""
    
    settings = GEMINISettings()
    if default:
        return settings

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

    # GEMINI REST API
    click.echo(click.style("GEMINI REST API Configuration", fg="green"))
    settings.GEMINI_REST_API_PORT = click.prompt("Enter the REST API port", default=7777)

    # GEMINI Domain
    click.echo(click.style("GEMINI Domain", fg="green"))
    settings.GEMINI_DOMAIN = click.prompt("Enter the domain", default="localhost")

    return settings
