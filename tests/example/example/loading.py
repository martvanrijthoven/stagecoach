import json
from pathlib import Path


def load_data(file_path: Path):
    with open(file_path, "r") as f:
        return json.load(f)