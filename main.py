from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import typer

import cli_commands
from routes import *

app = FastAPI()
app.include_router(startup_router)
app.include_router(games_router)
app.include_router(files_router)
app.mount("/content", StaticFiles(directory="content"), name="content")

cli = typer.Typer()
cli.add_typer(cli_commands.cli, name="database")

if (__name__ == "__main__"):
    cli()
