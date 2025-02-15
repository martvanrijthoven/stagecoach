import time
from pathlib import Path
from textwrap import dedent
from typing import Optional

from dicfg import ConfigReader
from dicfg import build_config as _run_stage
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
    stages: list[Path]
    output_folder: Path
    unlock: Optional[bool] = False

    def run(self) -> None:
        self.output_folder.mkdir(parents=True, exist_ok=True)
        logger = setup_logging(self.output_folder / LOG)
        print(self)
        try:
            with LockManager(name=NAME, folder=self.output_folder, unlock=self.unlock):
                for stage in self.stages:
                    config = self._initialize_config(stage)
                    logger.info(f"Config for stage {stage.stem}: {config}")
                    run_stage(stage_name=stage.stem, config=config[DEFAULT])
        except LockInUseError:
            print(f"StageCoach at: {self.output_folder} is locked. Skipping.")
        except Exception as e:
            logger.exception(e)
            raise

    def _initialize_config(self, stage: Path) -> dict:
        reader = ConfigReader(
            name=stage.stem,
            main_config_path=STAGE_CONFIG_PATH,
            presets=Path(stage).parent / PRESETS,
        )
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
