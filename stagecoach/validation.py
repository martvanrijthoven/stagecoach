from pydantic import BaseModel
from stagecoach.io import StageOutput


class SkipStageError(Exception):
    """"""

class StageValidator(BaseModel):

    outputs: dict[str, StageOutput]
    skippable: bool = True

    def model_post_init(self, __context):
        if self._skip_stage():
            raise SkipStageError()

    def _skip_stage(self) -> bool:
        return self.skippable and self._all_exist()

    def _all_exist(self):
        return all([output.path.exists() for output in self.outputs.values()])