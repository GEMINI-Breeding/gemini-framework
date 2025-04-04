
import click
import os, subprocess
from pathlib import Path

from gemini.config.settings import GEMINISettings
from gemini.manager import GEMINIManager

class GEMINICLIContext:
    def __init__(self) -> None:
        self.manager = GEMINIManager()
        self.script_dir = Path(__file__).parent
        self.pipeline_dir = self.script_dir.parent / "pipeline"

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = GEMINICLIContext()

@cli.command()
@click.pass_obj
def build(ctx: GEMINICLIContext):
    click.echo(click.style("Building GEMINI pipeline", fg="blue"))
    ctx.manager.build()
    click.echo(click.style("GEMINI pipeline built", fg="blue"))

@cli.command()
@click.pass_obj
def start(ctx: GEMINICLIContext):
    click.echo(click.style("Starting GEMINI pipeline", fg="blue"))
    ctx.manager.start()
    click.echo(click.style("GEMINI pipeline started", fg="blue"))

@cli.command()
@click.pass_obj
def stop(ctx: GEMINICLIContext):
    click.echo(click.style("Stopping GEMINI pipeline", fg="blue"))
    ctx.manager.stop()
    click.echo(click.style("GEMINI pipeline stopped", fg="blue"))

@cli.command()
@click.pass_obj
def clean(ctx: GEMINICLIContext):
    click.echo(click.style("Cleaning GEMINI pipeline", fg="blue"))
    ctx.manager.clean()
    click.echo(click.style("GEMINI pipeline cleaned", fg="blue"))

@cli.command()
@click.pass_obj
def reset(ctx: GEMINICLIContext):
    click.echo(click.style("Resetting GEMINI pipeline", fg="blue"))
    ctx.manager.reset()
    click.echo(click.style("GEMINI pipeline reset", fg="blue"))

@cli.command()
@click.option('--default', is_flag=True, help="Use default settings")
@click.pass_obj
def setup(ctx: GEMINICLIContext, default: bool = False):
    click.echo(click.style("Setting up GEMINI pipeline", fg="blue"))
    settings = environment_setup(default=default)
    ctx.manager.save_settings(settings)
    click.echo(click.style("GEMINI pipeline setup complete", fg="blue"))

@cli.command()
@click.argument('domain')
@click.pass_obj
def set_domain(ctx: GEMINICLIContext, domain: str):
    click.echo(click.style(f"Setting domain to {domain}", fg="blue"))
    ctx.manager.set_domain(domain)
    click.echo(click.style("GEMINI domain updated", fg="blue"))

def environment_setup(default: bool = False) -> GEMINISettings:
    settings = GEMINISettings()
    if default:
        return settings

    click.echo(click.style("GEMINI Database Configuration", fg="green"))
    settings.GEMINI_DB_USER = click.prompt("Enter the database user", default="gemini")
    settings.GEMINI_DB_PASSWORD = click.prompt("Enter the database password", default="gemini")
    settings.GEMINI_DB_NAME = click.prompt("Enter the database name", default="gemini")

    click.echo(click.style("GEMINI Logger Configuration", fg="green"))
    settings.GEMINI_LOGGER_PASSWORD = click.prompt("Enter the logger password", default="gemini")

    click.echo(click.style("GEMINI File Store", fg="green"))
    settings.GEMINI_STORAGE_ROOT_USER = click.prompt("Enter the storage root user", default="gemini_root")
    settings.GEMINI_STORAGE_ROOT_PASSWORD = click.prompt("Enter the storage root password", default="gemini_root")
    settings.GEMINI_STORAGE_ACCESS_KEY = click.prompt("Enter the storage access key", default="gemini_storage_user")
    settings.GEMINI_STORAGE_SECRET_KEY = click.prompt("Enter the storage secret", default="gemini_secret")

    click.echo(click.style("GEMINI REST API Configuration", fg="green"))
    settings.GEMINI_REST_API_PORT = click.prompt("Enter the REST API port", default=7777)

    click.echo(click.style("GEMINI Domain", fg="green"))
    settings.GEMINI_DOMAIN = click.prompt("Enter the domain", default="localhost")

    return settings
