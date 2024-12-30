from typing import ClassVar
from pydantic import BaseModel, field_validator, model_validator
from pathlib import Path
from dicfg.addons.addons import TemplateAddon


class StageInput(TemplateAddon, BaseModel):
    NAME: ClassVar[str] = "input"

    path: Path

    @field_validator("path")
    def path_must_exist(cls, v):
        if not v.exists():
            raise ValueError(f"The input path {v} does not exist.")
        return v

    @classmethod
    def _data(cls):
        return {
            "path@validator(required)": "",
        }


class StageOutput(TemplateAddon, BaseModel):
    NAME: ClassVar = "output"

    path: Path
    overwrite: bool = True

    @model_validator(mode="before")
    def check_path(cls, values):
        path = Path(values.get("path"))
        overwrite = values.get("overwrite", True)
        if path and path.exists() and not overwrite:
            raise ValueError(
                f"The path {path} already exists. (Set overwrite to True to overwrite)"
            )
        return values

    @classmethod
    def _data(cls):
        return {
            "path@validator(required)": "",
            "overwrite": True,
        }


