import time
from pathlib import Path
from typing import Any, Optional

from dicfg import ConfigReader
from dicfg import build_config as _run_stage
from pydantic import BaseModel
from stagecoach.configuration import STAGE_CONFIG_PATH
from stagecoach.io import *
from stagecoach.trails import Trace as _
from stagecoach.trails import Trail, Trails
from stagecoach.validation import SkipStageError
from stagecoach.version import VERSION as __version__

DEFAULT = "default"
PRESETS = "presets"


def run_stage(stage_name: str, config: dict) -> None:
    print(f"\nStarting stage: {stage_name}")
    start = time.perf_counter()
    try:
        print(config)
        out = _run_stage(config)
    except SkipStageError:
        out = f"Skipping stage {stage_name}"
    end = time.perf_counter()
    elapsed = end - start
    print(out)
    print(f"Executed in {elapsed:.4f} seconds")


class Stages(BaseModel):
    stages: list[Path] | dict[str, dict]
    trail: Optional[Trail] = None

    def _initialize_config(self, stage_name: str, stage: Path | dict) -> dict: 
        presets = Path(stage).parent / PRESETS if isinstance(stage, Path) else PRESETS           
        reader = ConfigReader(
            name=stage_name,
            main_config_path=STAGE_CONFIG_PATH,
            presets=presets
        )
        if self.trail is None:
            return reader.read(stage)
        return reader.read([stage, {stage_name: self.trail.config.get(stage_name, {})}])

    def run(self) -> None:
        if isinstance(self.stages, list):
            stages = {stage.stem: stage for stage in self.stages}
        else:
            stages = self.stages

        for stage_name, stage in stages.items():            
            config = self._initialize_config(stage_name=stage_name, stage=stage)
            default_config = config.pop(DEFAULT, {})
            if not config:
                run_stage(stage_name=stage_name, config=default_config)
            else:
                for context in config.keys():
                    print("context=", context)
                    run_stage(stage_name=stage_name, config=config[context])


class StageCoach(TemplateAddon, BaseModel):
    NAME: ClassVar[str] = "stagecoach"

    stages: list[str|Path] | dict
    trails: Optional[Trails] = None  # [name_of_trail (eg. image_name): [stage_name: config]]

    def model_post_init(self, __context):
        self()

    @classmethod
    def _data(cls):
        return {"stages!required": None, "trails": None}

    def __call__(self):
        if self.trails is None:
            Stages(stages=self.stages).run()
        else:
            for trail in self.trails:
                print(f"\nStarting trail: {trail.name}")
                Stages(stages=self.stages, trail=trail).run()
