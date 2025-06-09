import asyncio
import shutil
from pathlib import Path

import click
import uvicorn
from google.adk.cli.cli import run_cli
from google.adk.cli.fast_api import get_fast_api_app

from misstea import agent  # noqa: F401
from misstea.logger import configure_console_logging


@click.command()
@click.argument("command", default="web", nargs=1)
@click.option("-p", "--port", help="Port to run web interface on.", default=9876)
@click.option("-v", "--verbosity", help="Verbosity.", default=0, count=True)
def cli(command: str, port: int, verbosity: int) -> None:
    """Provide the main CLI entry point for MissTea."""
    configure_console_logging(verbosity)

    # Check is `*.egg-info` directory exists from running uv and delete
    egg_paths = [
        x
        for x in Path(__file__).parent.parent.iterdir()
        if x.is_dir() and x.name.endswith(".egg-info")
    ]
    if egg_paths != []:
        shutil.rmtree(egg_paths[0])

    if command == "web":
        app = get_fast_api_app(
            agent_dir=Path(__file__).parent.parent.absolute().__str__(), web=True
        )
        config = uvicorn.Config(
            app,
            host="127.0.0.1",
            port=port,
            reload=True,
        )
        server = uvicorn.Server(config)
        server.run()
    elif command == "run":
        asyncio.run(
            run_cli(
                agent_parent_dir=Path(__file__).parent.parent.absolute().__str__(),
                agent_folder_name=Path(__file__).parent.name,
                save_session=False,
            )
        )
