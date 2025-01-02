from pathlib import Path
from typing import Optional
from pathlib import Path
from typing import Optional
import click

from stagecoach import Stages

@click.command()
@click.option(
    "--stage",
    "stages",
    multiple=True,
    type=str,
    help="One or more stages configurations to apply.",
)
@click.option(
    "--folder",
    type=click.Path(exists=True, dir_okay=True, readable=True),
    help="Path to folder",
)
@click.option(
    "--configs",
    "configs",
    multiple=True,
    type=str,
    help="One or more configurations to apply.",
)
@click.option(
    "--preset",
    "presets",
    multiple=True,
    type=str,
    help="One or more preset configurations to apply.",
)
@click.option(
    "--force-rerun",
    "force_rerun",
    is_flag=True,
    help="Force re-run of pipeline even if lock is present.",
)
def run_stages(
    stages: list[str],
    folder: Path,
    configs: Optional[tuple[str]] = (),
    presets: Optional[tuple[str]] = (),
    force_rerun: bool = False,
):
    Stages(
        stages=stages,
        output_folder=folder,
        configs=configs,
        presets=presets,
        force_rerun=force_rerun,
    ).run()


if __name__ == "__main__":
    run_stages()
