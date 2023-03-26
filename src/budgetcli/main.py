
import configparser

import typer


# init config parser
config = configparser.ConfigParser()

# init typer app
cli = typer.Typer()

@cli.command()
def init() -> None:
    """Initialize the application"""
    print("Init app")
    

@cli.command()
def run() -> None:
    """Run the application"""
    print("Run app")
