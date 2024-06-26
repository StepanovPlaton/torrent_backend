
from asyncio import run as aiorun
import typer

from database import Database

cli = typer.Typer()


@cli.command(name="create")
def create_database(): aiorun(Database.create_all())
@cli.command(name="drop")
def drop_database(): aiorun(Database.drop_all())
@cli.command(name="recreate")
def recreate_database(): aiorun(Database.recreate_all())
