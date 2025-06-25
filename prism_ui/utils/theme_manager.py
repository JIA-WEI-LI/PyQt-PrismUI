import os
import weakref
from enum import Enum
from PyQt5.QtCore import QObject, pyqtSignal, QFileSystemWatcher
from PyQt5.QtWidgets import QWidget

class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"

class ThemeManager(QObject):
    theme_changed = pyqtSignal(Theme)
    style_changed = pyqtSignal(str)

    def __init__(self, qss_root: str, style_name: str = "winui", default_theme=Theme.DARK):
        super().__init__()
        self._theme = default_theme
        self._style_name = style_name
        self._qss_root = qss_root
        self._widgets = weakref.WeakSet()
        self._cache = {}
        self._watcher = QFileSystemWatcher()
        self._watcher.fileChanged.connect(self._on_qss_file_changed)

    def register(self, widget: QWidget):
        if widget not in self._widgets:
            self._widgets.add(widget)
            self.apply_theme(widget)

    def deregister(self, widget: QWidget):
        if widget in self._widgets:
            self._widgets.remove(widget)

    def set_theme(self, theme: Theme):
        if self._theme != theme:
            self._theme = theme
            self.theme_changed.emit(theme)
            self.update_all_widgets()

    def set_style(self, style_name: str):
        if self._style_name != style_name:
            self._style_name = style_name
            self.style_changed.emit(style_name)
            self.update_all_widgets()

    def current_theme(self):
        return self._theme

    def _get_qss_path(self, widget: QWidget) -> str:
        name = widget.objectName()
        if not name:
            return ""
        return os.path.join(self._qss_root, self._style_name, self._theme.value, f"{name}.qss")

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
            self._cache[path] = content
            return content
        except Exception:
            return ""

    def apply_theme(self, widget: QWidget):
        qss_path = self._get_qss_path(widget)
        qss = self._load_qss(qss_path)
        if qss:
            widget.setStyleSheet(qss)
        else:
            widget.setStyleSheet("")

    def update_all_widgets(self):
        for widget in list(self._widgets):
            if widget is not None:
                self.apply_theme(widget)

    def _on_qss_file_changed(self, path: str):
        if path in self._cache:
            del self._cache[path]
        self.update_all_widgets()

qss_root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resource", "themes")
theme_manager = ThemeManager(qss_root=qss_root_path)