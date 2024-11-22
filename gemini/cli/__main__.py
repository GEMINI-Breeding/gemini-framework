import click
from gemini.cli.pipeline import pipeline

@click.group()
def cli():
    pass

cli.add_command(pipeline)

