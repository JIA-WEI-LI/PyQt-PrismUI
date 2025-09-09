import os
import weakref
from enum import Enum
from typing import Optional
from PyQt5.QtCore import QObject, pyqtSignal, QFileSystemWatcher
from PyQt5.QtWidgets import QWidget

from .theme_loader import ThemeLoader

class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"

class ThemeManager(QObject):
    theme_changed = pyqtSignal(Theme)
    style_changed = pyqtSignal(str)

    def __init__(self, base_path: str, style_name: str = "winui", default_theme=Theme.DARK):
        super().__init__()
        self._theme = default_theme
        self._style_name = style_name
        self._base_path = base_path
        self._widgets = weakref.WeakSet()
        self._cache = {}
        self._watcher = QFileSystemWatcher()
        self._watcher.fileChanged.connect(self._on_qss_file_changed)

        self._flattened_cache = None

        self.loader = ThemeLoader(base_path)
        self._variables = {}
        self.set_theme(self._theme)

    @property
    def theme(self):
        return self._theme

    def set_theme(self, theme: Theme):
        if self._theme != theme:
            self._theme = theme
            self._cache.clear()
            need_update = True
        else:
            need_update = False

        ns = self.loader.load(self._theme.value)
        self._variables = ns

        if need_update:
            self.theme_changed.emit(theme)
            self.update_all_widgets()

    def get_current_variables(self, key: Optional[str] = None):
        if key is None:
            return self._flatten_namespace(self._variables)

        flat = self._flatten_namespace(self._variables)
        return flat.get(key)

    def _flatten_namespace(self, ns, prefix="--Theme"):
        result = {}
        for attr in dir(ns):
            if attr.startswith("_"):
                continue
            value = getattr(ns, attr)
            if isinstance(value, type(ns)):
                result.update(self._flatten_namespace(value, f"{prefix}{attr.capitalize()}_"))
            else:
                key_parts = [part.capitalize() for part in attr.split("_")]
                key = prefix + "_".join(key_parts)
                result[key] = value

        self._flattened_cache = result
        return result

    def register(self, widget: QWidget):
        if widget not in self._widgets:
            self._widgets.add(widget)
            self.apply_theme(widget)

    def deregister(self, widget: QWidget):
        if widget in self._widgets:
            self._widgets.remove(widget)

    def apply_theme(self, widget: QWidget):
        qss_path = self._get_qss_path(widget)
        if not qss_path:
            return

        if qss_path in self._cache:
            widget.setStyleSheet(self._cache[qss_path])
            return

        qss = self._load_qss(qss_path)
        if qss:
            widget.setStyleSheet(qss)
            self._cache[qss_path] = qss

    def _get_qss_path(self, widget: QWidget) -> str:
        name = widget.objectName()
        if not name:
            return ""
        return os.path.join(self._base_path, "qss", f"{name}.qss")

    def _load_qss(self, path: str) -> str:
        if not os.path.isfile(path):
            return ""
        if path not in self._watcher.files():
            self._watcher.addPath(path)
        if path in self._cache:
            return self._cache[path]

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            for key, value in self._flatten_namespace(self._variables).items():
                content = content.replace(key, str(value))
            self._cache[path] = content
            return content
        except Exception:
            return ""

    def update_all_widgets(self):
        for widget in list(self._widgets):
            if widget is not None:
                self.apply_theme(widget)
            if hasattr(widget, "updateIcon"):
                widget.updateIcon()

    def _on_qss_file_changed(self, path: str):
        if path in self._cache:
            del self._cache[path]
        self.update_all_widgets()

qss_root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resource")
theme_manager = ThemeManager(qss_root_path)
