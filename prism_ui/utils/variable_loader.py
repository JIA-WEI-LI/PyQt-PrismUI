import os
import yaml
from enum import Enum
from ..resource.themes.winui.colors import LightThemeColors, DarkThemeColors

class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"

def flatten_dict(d: dict, parent_key: str = "", sep: str = "_") -> dict:
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep))
        else:
            items[new_key] = v
    return items

def format_key(key: str) -> str:
    return "_".join([part.capitalize() for part in key.split("_")])

def get_variables(theme: Theme) -> dict:
    colors = DarkThemeColors if theme == Theme.DARK else LightThemeColors
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "resource", "themes", "winui", "variables.yaml")

    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = yaml.safe_load(f)

    flat_data = flatten_dict(raw_data)

    result = {}
    for key, value in flat_data.items():
        css_var = f"--ThemeColor_{format_key(key)}"
        if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
            color_attr = value.strip("{}")
            result[css_var] = getattr(colors, color_attr)
        else:
            result[css_var] = value

    return result