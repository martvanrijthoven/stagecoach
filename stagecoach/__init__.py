import time
from typing import Optional

from dicfg import ConfigReader
from stagecoach.io import *
from stagecoach.locking import LockInUseError, LockManager
from stagecoach.logging import setup_logging
from stagecoach.validation import SkipStageError
from dicfg import ConfigReader, build_config as _run_stage
from stagecoach.configuration import STAGE_CONFIG_PATH
from stagecoach.version import VERSION as __version__

STAGE_LOG = "stagecoach.log"
STAGE_LOCK = "stagecoach.lock"
DEFAULT_KEY = "default"

def print_stage(stage_name: str, config: dict) -> None:
    print(f"\n\tStarting stage: {stage_name}")
    # pprint(config, indent=1, depth=2,sort_dicts=False, compact=False)
    # print()


def run_stage(stage_name: str, config: dict) -> None:
    print_stage(stage_name, config)
    start = time.perf_counter()
    try:
        _run_stage(config)
    except SkipStageError:
        print(f"\tSkipping stage {stage_name}, all output paths already exist")
    end = time.perf_counter()
    elapsed = end - start
    print(f"\tExecuted in {elapsed:.4f} seconds")


class Stages(BaseModel):
    stages: list[str]
    output_folder: Path
    configs: Optional[list[str]] = None
    presets: Optional[list[str]] = None
    force_rerun: Optional[bool] = False

    def run(self) -> None:  # library: Path
        if self.configs is None:
            self.configs = []

        if self.presets is None:
            self.presets = ()

        self.output_folder.mkdir(parents=True, exist_ok=True)
        logger = setup_logging(self.output_folder / STAGE_LOG)

        # Stagecoach ASCII art (feel free to modify):
        stagecoach_art = rf"""
  =====                              =====                              
 =       =====   ==    ====  ====== =     =  ====    ==    ====  =    = 
 =         =    =  =  =    = =      =       =    =  =  =  =    = =    = 
  {__version__}   =   =    = =      = MvR  =       =    = =    = =      {chr(169)} 2025
       =   =   ====== =  === =      =       =    = ====== =      =    = 
 =     =   =   =    = =    = =      =     = =    = =    = =    = =    = 
  =====    =   =    =  ====  ======  =====   ====  =    =  ====  =    = 
        """

        print(f"\n{'-'*72}")
        print(f"{stagecoach_art}")
        print(f"{'-'*72}")
        print(f"\n\nStagecoach running in: {self.output_folder}\n")
        if self.force_rerun:
            (self.output_folder / STAGE_LOCK).unlink(missing_ok=True)
        try:
            with LockManager(name="stagecoach", folder=self.output_folder, force=self.force_rerun):
                for stage in self.stages:
                    stage_name = Path(stage).stem
                    presets_folder = Path(stage).parent / "presets"
                    reader = ConfigReader(name=stage_name, main_config_path=STAGE_CONFIG_PATH, presets=presets_folder)
                    config = reader.read((stage, *self.configs), presets=self.presets)
                    run_stage(stage_name=stage_name, config=config[DEFAULT_KEY])
        except LockInUseError:
            print(
                f"\tStageCoach for {self.output_folder} is already running/locked. Skipping."
            )
        except Exception as e:
            logger.exception(e)
            raise e
        