import os
import yaml
import logging
logger = logging.getLogger(__name__)
from enum import Enum

from ..resource.themes.winui.colors import LightTheme, DarkTheme

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

def get_variables(
        theme:Theme = Theme.DARK,  
        yaml_file:str="variables.yaml") -> dict:

    theme_type = DarkTheme if theme == Theme.DARK else LightTheme
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "resource", "yaml", yaml_file)
    format_kwarg = f"--Theme{yaml_file.split('.')[0].capitalize()}_"
    print(f"[variable_loader] >> Loading variables from: {file_path} with prefix: {format_kwarg}")

    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = yaml.safe_load(f)

    flat_data = flatten_dict(raw_data)

    result = {}
    for key, value in flat_data.items():
        css_var = f"{format_kwarg}{format_key(key)}"
        if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
            var_attr = value.strip("{}")
            result[css_var] = getattr(theme_type, var_attr)
        else:
            result[css_var] = value

    return result