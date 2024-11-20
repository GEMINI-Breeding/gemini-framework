import click

@click.group()
def cli():
    pass

@cli.command()
def init():
    click.echo('Initialized logger')