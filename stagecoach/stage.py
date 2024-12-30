from typing import ClassVar
from pydantic import BaseModel
from stagecoach.io import StageOutput
from dicfg.addons.addons import TemplateAddon


class SkipStageError(Exception):
    """"""

class StageCheck(TemplateAddon, BaseModel):
    NAME: ClassVar[str] = "stagecheck"

    outputs: dict[str, StageOutput]
    skippable: bool = True

    def model_post_init(self, __context):
        if self._skip_stage():
            raise SkipStageError()

    def _skip_stage(self) -> bool:
        return self.skippable and self.all_exist()

    def all_exist(self):
        return all([output.path.exists() for output in self.outputs.values()])


    @classmethod
    def _data(cls):
        return {
            "outputs": r"${OUTPUTS}",
            "skippable": r"${SKIPPABLE}",
        }