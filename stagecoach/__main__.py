from pathlib import Path
from typing import Optional

import click
from stagecoach import Stages
from stagecoach.configuration import STAGE_COACH_CONFIG_PATH

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
    "--stage-config",
    "stage_configs",
    multiple=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        path_type=Path,
        resolve_path=True,
    ),
    help="One or more configurations to apply.",
)

@click.option(
    "--output-folder",
    "output_folder",
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
    output_folder: Path,
    stages: Optional[list[Path]],
    stage_configs: Optional[list[Path]| dict] = None,
    unlock: bool = False,
    **kwargs,
):
    if not stages:
        stages = [STAGE_COACH_CONFIG_PATH]

    print(stage_configs)
    Stages(
        stages=stages,
        stage_configs=stage_configs,
        output_folder=output_folder,
        unlock=unlock,
    ).run()


if __name__ == "__main__":
    run_stages()
