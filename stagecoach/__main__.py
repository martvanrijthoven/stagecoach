from pathlib import Path

import click
from stagecoach import Stages


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@click.option(
    "--stage",
    "stages",
    multiple=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        path_type=Path,
        resolve_path=True,
    ),
    help="One or more stages configurations to apply.",
)
@click.option(
    "--output_folder",
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
        readable=True,
        writable=True,
        path_type=Path,
        resolve_path=True,
    ),
    help="Path to folder",
)
@click.option(
    "--unlock",
    "unlock",
    is_flag=True,
    help="unlock if lock is present.",
)
@click.argument("kwargs", nargs=-1, type=click.UNPROCESSED)
def run_stages(
    stages: list[Path],
    output_folder: Path,
    unlock: bool = False,
    **kwargs,
):
    Stages(
        stages=stages,
        output_folder=output_folder,
        unlock=unlock,
    ).run()


if __name__ == "__main__":
    run_stages()
