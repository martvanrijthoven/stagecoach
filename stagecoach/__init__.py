import time
from pathlib import Path
from textwrap import dedent
from typing import Any, ClassVar, Optional

from dicfg import ConfigReader
from dicfg import build_config as _run_stage
from dicfg.addons.addon import TemplateAddon
from pydantic import BaseModel
from stagecoach.configuration import STAGE_CONFIG_PATH
from stagecoach.io import *
from stagecoach.locking import LockInUseError, LockManager
from stagecoach.log import setup_logging
from stagecoach.validation import SkipStageError
from stagecoach.version import VERSION as __version__

LOG = "stagecoach.log"
LOCK = "stagecoach.lock"

NAME = "stagecoach"
DEFAULT = "default"
PRESETS = "presets"

OUTPUTS = "OUTPUTS"
OUTPUT_FOLDER = "output_folder"
PATH = "path"

STAGECOACH_ART = rf"""
  =====                              =====                              
 =       =====   ==    ====  ====== =     =  ====    ==    ====  =    = 
 =         =    =  =  =    = =      =       =    =  =  =  =    = =    = 
  {__version__}   =   =    = =      = MvR  =       =    = =    = =      {chr(169)} 2025
       =   =   ====== =  === =      =       =    = ====== =      =    = 
 =     =   =   =    = =    = =      =     = =    = =    = =    = =    = 
  =====    =   =    =  ====  ======  =====   ====  =    =  ====  =    = 
        """


def run_stage(stage_name: str, config: dict) -> None:
    print(f"\nStarting stage: {stage_name}")
    start = time.perf_counter()
    try:
        out = _run_stage(config)
    except SkipStageError:
        out = f"Skipping stage {stage_name}, all output paths exists"
    end = time.perf_counter()
    elapsed = end - start
    print(out)
    print(f"Executed in {elapsed:.4f} seconds")


class Stages(BaseModel):
    output_folder: Path
    stages: list[Path] | dict[str, dict]
    stage_configs: Optional[dict[str, dict] | list[Path]] = None
    unlock: Optional[bool] = False
    print_logo: Optional[bool] = False

    def run(self) -> None:
        if isinstance(self.stages, list):
            _stages = {s.stem: s for s in self.stages}
        else:
            _stages = self.stages

        self.output_folder.mkdir(parents=True, exist_ok=True)
        logger = setup_logging(self.output_folder / LOG)

        if self.print_logo:
            print(self)

        try:
            with LockManager(name=NAME, folder=self.output_folder, unlock=self.unlock):
                for stage_name, stage in _stages.items():
                    config = self._initialize_config(stage_name=stage_name, stage=stage)
                    logger.info(f"Config for stage {stage_name}: {config}")
                    run_stage(stage_name=stage_name, config=config[DEFAULT])
        except LockInUseError:
            print(f"StageCoach at: {self.output_folder} is locked. Skipping.")
        except Exception as e:
            logger.exception(e)
            raise

    def _initialize_config(self, stage_name: str, stage: Path) -> dict:
        reader = ConfigReader(
            name=stage_name,
            main_config_path=STAGE_CONFIG_PATH,
            presets=Path(stage).parent / PRESETS,
        )
        if self.stage_configs is not None:
            if isinstance(self.stage_configs, list):
                stage = [stage, *self.stage_configs]
            if stage_name in self.stage_configs:
                stage = [stage, {stage_name: self.stage_configs[stage_name]}]

        config = reader.read(stage)
        config[DEFAULT][OUTPUTS][OUTPUT_FOLDER][PATH] = str(self.output_folder)
        return config

    def __str__(self):
        template = dedent(
            """\
            {dashes}
            {art}
            {dashes}

            Stagecoach at: {folder}
            """
        )
        return template.format(
            dashes="-" * 72, art=STAGECOACH_ART, folder=self.output_folder
        )


class StageCoach(TemplateAddon, BaseModel):

    NAME: ClassVar[str] = "trails"

    output_folder: Path
    stages: list[str]
    trails: dict[str, Any]  # [name_of_trail (eg. image_name): [stage_name: config]]

    @classmethod
    def _data(cls):
        return {"stages!required": None, "trails!required": None}

    def __iter__(self):
        for name, trial in self.trails.items():
            yield (name, trial)


def run(stage_coach: StageCoach):
    for name, trail in iter(stage_coach):
        Stages(
            output_folder=stage_coach.output_folder / name,
            stages=stage_coach.stages,
            stage_configs=trail,
        ).run()
