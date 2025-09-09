import os
import yaml
from types import SimpleNamespace

class ThemeLoader:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def load(self, theme: str) -> SimpleNamespace:
        theme_file = os.path.join(self.base_path, "yaml", f"{theme}.yaml")
        theme_vars = self.yaml_to_dict(theme_file)

        color_file = os.path.join(self.base_path, "yaml", "color.yaml")
        font_file  = os.path.join(self.base_path, "yaml", "font.yaml")

        components_color = self.yaml_to_namespace(color_file)
        components_font  = self.yaml_to_namespace(font_file)

        self.resolve_refs(components_color, theme_vars)
        self.resolve_refs(components_font, theme_vars)

        result = SimpleNamespace(
            color=components_color,
            font=components_font,
        )
        return result
    
    def yaml_to_dict(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def yaml_to_namespace(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return self.dict_to_namespace(data)

    def dict_to_namespace(self, d):
        if isinstance(d, dict):
            return SimpleNamespace(**{k: self.dict_to_namespace(v) for k, v in d.items()})
        return d
    
    def resolve_refs(self, ns: SimpleNamespace, theme_vars: dict):
        def flatten_theme_vars(theme_vars):
            flat = {}

            def _flatten(obj):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if isinstance(v, (dict, SimpleNamespace)):
                            _flatten(v)
                        else:
                            flat[k] = v
                elif isinstance(obj, SimpleNamespace):
                    for k in dir(obj):
                        if k.startswith("_"):
                            continue
                        v = getattr(obj, k)
                        if isinstance(v, (dict, SimpleNamespace)):
                            _flatten(v)
                        else:
                            flat[k] = v
                else:
                    pass

            _flatten(theme_vars)
            return flat
        
        flat_theme = flatten_theme_vars(theme_vars)
        
        for attr in dir(ns):
            if attr.startswith("_"):
                continue
            value = getattr(ns, attr)
            if isinstance(value, type(ns)):
                self.resolve_refs(value, flat_theme)
            elif isinstance(value, str) and value.startswith("{") and value.endswith("}"):
                key = value[1:-1]
                if key in flat_theme:
                    setattr(ns, attr, flat_theme[key])
                else:
                    print(f"[theme_loader] WARNING: variable {key} not found")