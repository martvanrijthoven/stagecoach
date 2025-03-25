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
@click.argument("kwargs", nargs=-1, type=click.UNPROCESSED)
def run_stages(stages: list[Path], **kwargs):
    Stages(stages=stages).run()


if __name__ == "__main__":
    run_stages()
