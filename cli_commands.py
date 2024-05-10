
from asyncio import run as aiorun
import typer

import database

cli = typer.Typer()

@cli.command(name="create")
def create_database(): aiorun(database.create_all())
@cli.command(name="drop")
def drop_database(): aiorun(database.drop_all())
@cli.command(name="recreate")
def recreate_database(): aiorun(database.recreate_all())
