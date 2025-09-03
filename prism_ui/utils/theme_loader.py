import os
import yaml
from types import SimpleNamespace

class ThemeLoader:
    def __init__(self, base_path: str):
        self.base_path = base_path  # e.g., resource/themes

    def load(self, style: str, theme: str) -> SimpleNamespace:
        file_path = os.path.join(self.base_path, style, f"{theme}.yaml")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Theme file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return self.dict_to_namespace(data)

    def dict_to_namespace(self, d: dict):
        if isinstance(d, dict):
            return SimpleNamespace(**{k: self.dict_to_namespace(v) for k, v in d.items()})
        return d