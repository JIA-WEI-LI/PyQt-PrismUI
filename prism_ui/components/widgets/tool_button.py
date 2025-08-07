from typing import Union, Callable
from PyQt5.QtWidgets import QWidget, QToolButton
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import QSize, QRectF, Qt

from ...common.stylesheet_enum import PrismStyleSheet
from ...utils.theme_manager import theme_manager

class ToolButton(QToolButton):
    def __init__(self, *args, **kwargs):
        icon = None
        parent = None
        text = None

        for arg in args:
            if isinstance(arg, (QIcon, str)) and icon is None:
                icon = arg
            elif isinstance(arg, QWidget) and parent is None:
                parent = arg
            elif isinstance(arg, str) and text is None:
                text = arg

        parent = kwargs.get("parent", parent)
        icon = kwargs.get("icon", icon)
        text = kwargs.get("text", text)

        super().__init__(parent)
        self.isPressed = False
        self.isHover = False
        self._icon_source = None

        self.setProperty("class", "ToolButton")
        self.setIconSize(QSize(16, 16))

        if text:
            self.setText(text)
        if icon:
            self.setIcon(icon)
        else:
            self.setIcon(QIcon())

        PrismStyleSheet.TOOL_BUTTOON.apply(self)

    def setIcon(self, icon: Union[QIcon, Callable]):
        if callable(icon):
            self.setIconSource(icon)
        else:
            super().setIcon(icon)
            self._icon_source = None
            self._icon = icon

    def setIconSource(self, icon_accessor: Callable[[str], QIcon]):
        self._icon_source = icon_accessor
        self.updateIcon()

    def _get_icon_color(self) -> str:
        from prism_ui.utils.theme_manager import theme_manager  # 確保可用
        if not self.isEnabled():
            return theme_manager.get_current_variables("--ThemeColor_Text_Disabled")
        if self.isPressed:
            return theme_manager.get_current_variables("--ThemeColor_Text_Tertiary")
        if self.isHover:
            return theme_manager.get_current_variables("--ThemeColor_Text_Secondary")
        return theme_manager.get_current_variables("--ThemeColor_Text_Default")

    def updateIcon(self):
        if hasattr(self, "_icon_source") and callable(self._icon_source):
            try:
                color = self._get_icon_color()
                icon = self._icon_source(color)
                if icon:
                    super().setIcon(icon)
                    self._icon = icon
            except Exception as e:
                print(f"[ToolButton] Failed to update icon: {e}")

    def mousePressEvent(self, event):
        self.isPressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.isPressed = False
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        self.isHover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.isHover = False
        self.update()
        super().leaveEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        self.updateIcon()

    def paintEvent(self, event):
        super().paintEvent(event)

        if not hasattr(self, "_icon") or self._icon.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        if not self.isEnabled():
            painter.setOpacity(0.36)
        elif self.isPressed:
            painter.setOpacity(0.78)

        w = self.iconSize().width()
        h = self.iconSize().height()
        y = (self.height() - h) / 2

        text_width = self.fontMetrics().width(self.text()) if self.text() else 0
        spacing = 6

        total_width = w + spacing + text_width if text_width else w
        x = (self.width() - total_width) / 2

        if self.layoutDirection() == Qt.RightToLeft:
            x = self.width() - x - w

        rect = QRectF(x, y, w, h)
        self._icon.paint(painter, rect.toRect())

        painter.end()

class PrimaryToolButton(ToolButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setProperty("class", "PrimaryToolButton")

    def _get_icon_color(self) -> str:
        if self.isEnabled():
            if self.isHover: color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Secondary")
            elif self.isPressed: color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Tertiary")
            else: color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Default")
        elif not self.isEnabled():
            color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Disabled")
        return color
    
class ToggleToolButton(ToolButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._icon_on = None
        self._icon_off = None
        
        self._postInit()
        self.setProperty("class", "ToggleToolButton")
        
    def _postInit(self):
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self._on_toggle_state_changed)

    def setToggleIcons(self, icon_on: Union[QIcon, Callable], icon_off: Union[QIcon, Callable]):
        self._icon_on = icon_on
        self._icon_off = icon_off
        self._applyToggle()

    def _get_icon_color(self) -> str:
        if self.isChecked():
            if self.isEnabled():
                if self.isHover: color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Default")
                elif self.isPressed: color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Tertiary")
                else: color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Default")
            else:
                color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Disabled")
        else:
            if self.isEnabled():
                if self.isHover: color = theme_manager.get_current_variables("--ThemeColor_Text_Secondary")
                elif self.isPressed: color = theme_manager.get_current_variables("--ThemeColor_Text_Tertiary")
                else: color = theme_manager.get_current_variables("--ThemeColor_Text_Default")
            else:
                color = theme_manager.get_current_variables("--ThemeColor_Text_Disabled")
        return color

    def _applyToggle(self):
        if self._icon_on and self._icon_off:
            icon = self._icon_on if self.isChecked() else self._icon_off
            if callable(icon):
                self.setIconSource(icon)
            else:
                self.setIcon(icon)

    def _on_toggle_state_changed(self, checked: bool):
        self._applyToggle()
        self.updateIcon()

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._applyToggle()
        self.updateIcon()

class TransparentToolButton(ToolButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setProperty("class", "TransparentToolButton")

class TransparentToggleToolButton(ToggleToolButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setProperty("class", "TransparentToggleToolButton")