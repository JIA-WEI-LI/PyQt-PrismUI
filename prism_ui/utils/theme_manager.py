import os
import weakref
from enum import Enum
from typing import Optional
from PyQt5.QtCore import QObject, pyqtSignal, QFileSystemWatcher
from PyQt5.QtWidgets import QWidget

from prism_ui.resource.themes.winui.colors import LightThemeColors, DarkThemeColors

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

        self._variables = {}
        self.set_theme(self._theme)

    def register(self, widget: QWidget):
        if widget not in self._widgets:
            self._widgets.add(widget)
            self.apply_theme(widget)

    def deregister(self, widget: QWidget):
        if widget in self._widgets:
            self._widgets.remove(widget)

    def set_variables(self, variables: dict):
        self._variables = variables
        self._cache.clear()
        self.update_all_widgets()

    def set_theme(self, theme: Theme):
        if self._theme != theme:
            self._theme = theme
            self._cache.clear() 
            need_update = True
        else:
            need_update = False

        colors = DarkThemeColors if theme == Theme.DARK else LightThemeColors
        variables = {
            # Text
            '--ThemeColor_Text_Default': colors.TextFillColorPrimaryBrush,
            '--ThemeColor_Text_Secondary': colors.TextFillColorSecondaryBrush,
            '--ThemeColor_Text_Tertiary': colors.TextFillColorTertiaryBrush,
            '--ThemeColor_Text_Disabled': colors.TextFillColorDisabledBrush,
            '--ThemeColor_Text_Accent_Default': colors.AccentTextFillColorPrimaryBrush,
            '--ThemeColor_Text_Accent_Secondary': colors.AccentTextFillColorSecondaryBrush,
            '--ThemeColor_Text_Accent_Tertiary': colors.AccentTextFillColorTertiaryBrush,
            '--ThemeColor_Text_Accent_Disabled': colors.AccentTextFillColorDisabledBrush,
            '--ThemeColor_Text_On_Accent_Default': colors.TextOnAccentFillColorPrimaryBrush,
            '--ThemeColor_Text_On_Accent_Secondary': colors.TextOnAccentFillColorSecondaryBrush,
            '--ThemeColor_Text_On_Accent_Disabled': colors.TextOnAccentFillColorDisabledBrush,
            '--ThemeColor_Text_On_Accent_SelectedText': colors.TextOnAccentFillColorSelectedTextBrush,

            # Fill
            '--ThemeColor_Control_Default': colors.ControlFillColorDefaultBrush,
            '--ThemeColor_Control_Secondary': colors.ControlFillColorSecondaryBrush,
            '--ThemeColor_Control_Tertiary': colors.ControlFillColorTertiaryBrush,
            '--ThemeColor_Control_Quarternary': colors.ControlFillColorQuarternaryBrush,
            '--ThemeColor_Control_Disabled': colors.ControlFillColorDisabledBrush,
            '--ThemeColor_Control_Transparent': colors.ControlFillColorTransparentBrush,
            '--ThemeColor_Control_InputActive': colors.ControlFillColorInputActiveBrush,
            '--ThemeColor_ControlAlt_Transparent': colors.ControlAltFillColorTransparentBrush,
            '--ThemeColor_ControlAlt_Secondary': colors.ControlAltFillColorSecondaryBrush,
            '--ThemeColor_ControlAlt_Tertiary': colors.ControlAltFillColorTertiaryBrush,
            '--ThemeColor_ControlAlt_Quarternary': colors.ControlAltFillColorQuarternaryBrush,
            '--ThemeColor_ControlAlt_Disabled': colors.ControlAltFillColorDisabledBrush,
            '--ThemeColor_Control_Solid_Default': colors.ControlSolidFillColorDefaultBrush,
            '--ThemeColor_Control_Strong_Default': colors.ControlStrongFillColorDefaultBrush,
            '--ThemeColor_Control_Strong_Disabled': colors.ControlStrongFillColorDisabledBrush,
            '--ThemeColor_Subtle_Transparent': colors.SubtleFillColorTransparentBrush,
            '--ThemeColor_Subtle_Secondary': colors.SubtleFillColorSecondaryBrush,
            '--ThemeColor_Subtle_Tertiary': colors.SubtleFillColorTertiaryBrush,
            '--ThemeColor_Subtle_Disabled': colors.SubtleFillColorDisabledBrush,
            '--ThemeColor_ControlOnImage_Default': colors.ControlOnImageFillColorDefaultBrush,
            '--ThemeColor_ControlOnImage_Secondary': colors.ControlOnImageFillColorSecondaryBrush,
            '--ThemeColor_ControlOnImage_Tertiary': colors.ControlOnImageFillColorTertiaryBrush,
            '--ThemeColor_ControlOnImage_Disabled': colors.ControlOnImageFillColorDisabledBrush,
            '--ThemeColor_Accent_Default': colors.AccentFillColorDefaultBrush,
            '--ThemeColor_Accent_Secondary': colors.AccentFillColorSecondaryBrush,
            '--ThemeColor_Accent_Tertiary': colors.AccentFillColorTertiaryBrush,
            '--ThemeColor_Accent_Disabled': colors.AccentFillColorDisabledBrush,
            '--ThemeColor_Accent_SelectedTextBackground': colors.AccentFillColorSelectedTextBackgroundBrush,

            # Stroke
            '--ThemeColor_Card_Stroke_Default': colors.CardStrokeColorDefaultBrush,
            '--ThemeColor_Card_Stroke_Solid': colors.CardStrokeColorDefaultSolidBrush,
            '--ThemeColor_Control_ElevationBorder': colors.ControlElevationBorderBrush,
            '--ThemeColor_Circle_ElevationBorder': colors.CircleElevationBorderBrush,
            '--ThemeColor_TextControl_ElevationBorder': colors.TextControlElevationBorderBrush,
            '--ThemeColor_TextControl_ElevationBorder_Focused': colors.TextControlElevationBorderFocusedBrush,
            '--ThemeColor_AccentControl_ElevationBorder': colors.AccentControlElevationBorderBrush,
            '--ThemeColor_Control_Stroke_Default': colors.ControlStrokeColorDefaultBrush,
            '--ThemeColor_Control_Stroke_Secondary': colors.ControlStrokeColorSecondaryBrush,
            '--ThemeColor_ControlOnAccent_Stroke_Default': colors.ControlStrokeColorOnAccentDefaultBrush,
            '--ThemeColor_ControlOnAccent_Stroke_Secondary': colors.ControlStrokeColorOnAccentSecondaryBrush,
            '--ThemeColor_ControlOnAccent_Stroke_Tertiary': colors.ControlStrokeColorOnAccentTertiaryBrush,
            '--ThemeColor_ControlOnAccent_Stroke_Disabled': colors.ControlStrokeColorOnAccentDisabledBrush,
            '--ThemeColor_Control_StrongFillOnImage_Stroke': colors.ControlStrokeColorForStrongFillWhenOnImageBrush,
            '--ThemeColor_Control_Strong_Stroke_Default': colors.ControlStrongStrokeColorDefaultBrush,
            '--ThemeColor_Control_Strong_Stroke_Disabled': colors.ControlStrongStrokeColorDisabledBrush,
            '--ThemeColor_Surface_Stroke_Default': colors.SurfaceStrokeColorDefaultBrush,
            '--ThemeColor_Surface_Stroke_Flyout': colors.SurfaceStrokeColorFlyoutBrush,
            '--ThemeColor_Divider_Stroke_Default': colors.DividerStrokeColorDefaultBrush,
            '--ThemeColor_Focus_Stroke_Outer': colors.FocusStrokeColorOuterBrush,
            '--ThemeColor_Focus_Stroke_Inner': colors.FocusStrokeColorInnerBrush,
        }

        self.set_variables(variables)

        if need_update:
            self.theme_changed.emit(theme)

    def set_style(self, style_name: str):
        if self._style_name != style_name:
            self._style_name = style_name
            self.style_changed.emit(style_name)
            self.update_all_widgets()

    def get_current_variables(self, key: Optional[str] = None):
        colors = DarkThemeColors if self._theme == Theme.DARK else LightThemeColors

        variables = {
            # Text
            '--ThemeColor_Text_Default': colors.TextFillColorPrimaryBrush,
            '--ThemeColor_Text_Secondary': colors.TextFillColorSecondaryBrush,
            '--ThemeColor_Text_Tertiary': colors.TextFillColorTertiaryBrush,
            '--ThemeColor_Text_Disabled': colors.TextFillColorDisabledBrush,
            '--ThemeColor_Text_Accent_Default': colors.AccentTextFillColorPrimaryBrush,
            '--ThemeColor_Text_Accent_Secondary': colors.AccentTextFillColorSecondaryBrush,
            '--ThemeColor_Text_Accent_Tertiary': colors.AccentTextFillColorTertiaryBrush,
            '--ThemeColor_Text_Accent_Disabled': colors.AccentTextFillColorDisabledBrush,
            '--ThemeColor_Text_On_Accent_Default': colors.TextOnAccentFillColorPrimaryBrush,
            '--ThemeColor_Text_On_Accent_Secondary': colors.TextOnAccentFillColorSecondaryBrush,
            '--ThemeColor_Text_On_Accent_Disabled': colors.TextOnAccentFillColorDisabledBrush,
            '--ThemeColor_Text_On_Accent_SelectedText': colors.TextOnAccentFillColorSelectedTextBrush,

            # Fill
            '--ThemeColor_Control_Default': colors.ControlFillColorDefaultBrush,
            '--ThemeColor_Control_Secondary': colors.ControlFillColorSecondaryBrush,
            '--ThemeColor_Control_Tertiary': colors.ControlFillColorTertiaryBrush,
            '--ThemeColor_Control_Quarternary': colors.ControlFillColorQuarternaryBrush,
            '--ThemeColor_Control_Disabled': colors.ControlFillColorDisabledBrush,
            '--ThemeColor_Control_Transparent': colors.ControlFillColorTransparentBrush,
            '--ThemeColor_Control_InputActive': colors.ControlFillColorInputActiveBrush,
            '--ThemeColor_ControlAlt_Transparent': colors.ControlAltFillColorTransparentBrush,
            '--ThemeColor_ControlAlt_Secondary': colors.ControlAltFillColorSecondaryBrush,
            '--ThemeColor_ControlAlt_Tertiary': colors.ControlAltFillColorTertiaryBrush,
            '--ThemeColor_ControlAlt_Quarternary': colors.ControlAltFillColorQuarternaryBrush,
            '--ThemeColor_ControlAlt_Disabled': colors.ControlAltFillColorDisabledBrush,
            '--ThemeColor_Control_Solid_Default': colors.ControlSolidFillColorDefaultBrush,
            '--ThemeColor_Control_Strong_Default': colors.ControlStrongFillColorDefaultBrush,
            '--ThemeColor_Control_Strong_Disabled': colors.ControlStrongFillColorDisabledBrush,
            '--ThemeColor_Subtle_Transparent': colors.SubtleFillColorTransparentBrush,
            '--ThemeColor_Subtle_Secondary': colors.SubtleFillColorSecondaryBrush,
            '--ThemeColor_Subtle_Tertiary': colors.SubtleFillColorTertiaryBrush,
            '--ThemeColor_Subtle_Disabled': colors.SubtleFillColorDisabledBrush,
            '--ThemeColor_ControlOnImage_Default': colors.ControlOnImageFillColorDefaultBrush,
            '--ThemeColor_ControlOnImage_Secondary': colors.ControlOnImageFillColorSecondaryBrush,
            '--ThemeColor_ControlOnImage_Tertiary': colors.ControlOnImageFillColorTertiaryBrush,
            '--ThemeColor_ControlOnImage_Disabled': colors.ControlOnImageFillColorDisabledBrush,
            '--ThemeColor_Accent_Default': colors.AccentFillColorDefaultBrush,
            '--ThemeColor_Accent_Secondary': colors.AccentFillColorSecondaryBrush,
            '--ThemeColor_Accent_Tertiary': colors.AccentFillColorTertiaryBrush,
            '--ThemeColor_Accent_Disabled': colors.AccentFillColorDisabledBrush,
            '--ThemeColor_Accent_SelectedTextBackground': colors.AccentFillColorSelectedTextBackgroundBrush,

            # Stroke
            '--ThemeColor_Card_Stroke_Default': colors.CardStrokeColorDefaultBrush,
            '--ThemeColor_Card_Stroke_Solid': colors.CardStrokeColorDefaultSolidBrush,
            '--ThemeColor_Control_ElevationBorder': colors.ControlElevationBorderBrush,
            '--ThemeColor_Circle_ElevationBorder': colors.CircleElevationBorderBrush,
            '--ThemeColor_TextControl_ElevationBorder': colors.TextControlElevationBorderBrush,
            '--ThemeColor_TextControl_ElevationBorder_Focused': colors.TextControlElevationBorderFocusedBrush,
            '--ThemeColor_AccentControl_ElevationBorder': colors.AccentControlElevationBorderBrush,
            '--ThemeColor_Control_Stroke_Default': colors.ControlStrokeColorDefaultBrush,
            '--ThemeColor_Control_Stroke_Secondary': colors.ControlStrokeColorSecondaryBrush,
            '--ThemeColor_ControlOnAccent_Stroke_Default': colors.ControlStrokeColorOnAccentDefaultBrush,
            '--ThemeColor_ControlOnAccent_Stroke_Secondary': colors.ControlStrokeColorOnAccentSecondaryBrush,
            '--ThemeColor_ControlOnAccent_Stroke_Tertiary': colors.ControlStrokeColorOnAccentTertiaryBrush,
            '--ThemeColor_ControlOnAccent_Stroke_Disabled': colors.ControlStrokeColorOnAccentDisabledBrush,
            '--ThemeColor_Control_StrongFillOnImage_Stroke': colors.ControlStrokeColorForStrongFillWhenOnImageBrush,
            '--ThemeColor_Control_Strong_Stroke_Default': colors.ControlStrongStrokeColorDefaultBrush,
            '--ThemeColor_Control_Strong_Stroke_Disabled': colors.ControlStrongStrokeColorDisabledBrush,
            '--ThemeColor_Surface_Stroke_Default': colors.SurfaceStrokeColorDefaultBrush,
            '--ThemeColor_Surface_Stroke_Flyout': colors.SurfaceStrokeColorFlyoutBrush,
            '--ThemeColor_Divider_Stroke_Default': colors.DividerStrokeColorDefaultBrush,
            '--ThemeColor_Focus_Stroke_Outer': colors.FocusStrokeColorOuterBrush,
            '--ThemeColor_Focus_Stroke_Inner': colors.FocusStrokeColorInnerBrush,
        }
        if key is None:
            return variables
        return variables.get(key)

    def current_theme(self):
        return self._theme

    def _get_qss_path(self, widget: QWidget) -> str:
        name = widget.objectName()
        if not name:
            return ""
        return os.path.join(self._qss_root, "qss", f"{name}.qss")

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

            for key, value in self._variables.items():
                content = content.replace(key, value)

            self._cache[path] = content
            return content
        except Exception as e:
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
            if hasattr(widget, "updateIcon"):
                widget.updateIcon()

    def _on_qss_file_changed(self, path: str):
        if path in self._cache:
            del self._cache[path]
        self.update_all_widgets()

qss_root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resource")
theme_manager = ThemeManager(qss_root=qss_root_path)