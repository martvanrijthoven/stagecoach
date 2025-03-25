import abc
from typing import ClassVar, Iterable, Iterator
from dicfg.addons.addon import TemplateAddon
from pydantic import BaseModel


class Trail(BaseModel):
    name: str
    config: dict


class Trace(TemplateAddon, BaseModel):
    NAME: ClassVar = "trace"

    name: str
    config: dict

    def create_trail(self, stage_names: list[str], context_keys: list[str]) -> Trail:
        return Trail(
            name=self.name,
            config={
                stage: {context: self.config.copy() for context in context_keys}
                for stage in stage_names
            },
        )


class Trails(TemplateAddon, BaseModel):
    NAME: ClassVar = "trails"
    traces: dict

    @classmethod
    def _data(cls):
        return {
            "traces!required": None,
        }

    def __iter__(self) -> Iterator[Trail]:
        for name, config in self.traces.items():
            yield Trail(name=name, config=config)


class TrailsCreator(TemplateAddon, BaseModel):
    NAME: ClassVar = "trailscreator"
    traces: Iterable[Trace]
    stage_names: list[str]
    context_keys: list[str] = ["default"]

    @classmethod
    def _data(cls):
        return {
            "traces!required": None,
        }

    def __iter__(self) -> Iterator[Trail]:
        for trace in self.traces:
            yield trace.create_trail(self.stage_names, self.context_keys)


class Traces(BaseModel, Iterable[Trace]):
    @abc.abstractmethod
    def __iter__(self) -> Iterator[Trace]:
        """
        Returns an iterator of Traces
        """