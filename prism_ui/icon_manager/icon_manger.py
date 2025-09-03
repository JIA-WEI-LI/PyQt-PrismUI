import os
import importlib.util
import logging
from PyQt5.QtGui import QIcon

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "icons")  # theme 資料夾

class IconManager:
    def __init__(self, default_theme: str = None):
        self.themes = {}  # theme_name -> icon_class
        self._load_all_themes()
        if default_theme and default_theme.upper() in self.themes:
            self.default_theme = default_theme.upper()
        elif self.themes:
            self.default_theme = list(self.themes.keys())[0]
        else:
            self.default_theme = None
            logger.warning("No themes found in icons directory.")

    def _load_all_themes(self):
        if not os.path.isdir(ICONS_DIR):
            logger.error(f"Icons directory not found: {ICONS_DIR}")
            return

        for folder in os.listdir(ICONS_DIR):
            theme_path = os.path.join(ICONS_DIR, folder)
            if os.path.isdir(theme_path):
                theme_name = folder.upper()
                icon_py_path = os.path.join(BASE_DIR, f"{folder}_icon.py")
                if os.path.exists(icon_py_path):
                    icon_class = self._import_icon_class(icon_py_path, f"{folder}_icon", theme_name)
                    if icon_class:
                        self.themes[theme_name] = icon_class
                        logger.info(f"Loaded theme: {theme_name}")
                else:
                    logger.warning(f"Icon class file not found for theme '{theme_name}': {icon_py_path}")

    def _import_icon_class(self, path: str, module_name: str, theme_name: str):
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None:
            logger.error(f"Failed to create spec for {module_name}")
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls_name = f"{theme_name.capitalize()}Icon"
        icon_class = getattr(module, cls_name, None)
        if icon_class is None:
            logger.error(f"Icon class '{cls_name}' not found in {module_name}")
        return icon_class

    def get_icon(self, icon_name: str, theme: str = None, color: str = None, size=None) -> QIcon:
        theme_name = (theme or self.default_theme).upper()
        if theme_name not in self.themes:
            logger.error(f"Theme '{theme_name}' not found.")
            return QIcon()

        icon_class = self.themes[theme_name]
        icon_attr = getattr(icon_class, icon_name.upper(), None)
        if icon_attr is None:
            logger.warning(f"Icon '{icon_name}' not found in theme '{theme_name}'.")
            return QIcon()

        if callable(icon_attr):
            return icon_attr(color=color, size=size)
        else:
            return QIcon(icon_attr)

    def get_icon_path(self, icon_name: str, theme: str = None) -> str:
        theme_name = (theme or self.default_theme).upper()
        if theme_name not in self.themes:
            logger.error(f"Theme '{theme_name}' not found.")
            return ""

        icon_class = self.themes[theme_name]
        icon_attr = getattr(icon_class, icon_name.upper(), None)
        if icon_attr is None:
            logger.warning(f"Icon '{icon_name}' not found in theme '{theme_name}'.")
            return ""

        return str(icon_attr)