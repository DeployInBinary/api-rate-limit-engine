import json
from pathlib import Path


class JSONStorage:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)

    def load(self) -> dict:
        if not self.filepath.exists():
            return {}

        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def save(self, data: dict):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)
