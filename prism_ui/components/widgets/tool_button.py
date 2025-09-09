from typing import Union, Callable
from PyQt5.QtWidgets import QWidget, QToolButton
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import QSize, QRectF, Qt

from .base_widget_mixin import BaseMixin
from .button import PushButton
from ...common.stylesheet_enum import PrismStyleSheet
from ...utils.theme_manager import theme_manager

class ToolButton(QToolButton, BaseMixin):
    def __init__(self, icon: QIcon = None, parent: QWidget = None):
        super().__init__(parent=parent)
        self.isPressed = False
        self.isHover = False
        self._icon_source = None

        self.setProperty("class", "ToolButton")
        self.setIconSize(QSize(16, 16))
        self.setIcon(icon if icon else QIcon())
        self.adjustToSquare()

        PrismStyleSheet.TOOLBUTTON.apply(self)

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

    def adjustToSquare(self, padding: int = 8):
        size = self.iconSize()
        side = max(size.width(), size.height()) + padding
        self.setFixedSize(side, side)

    def _get_icon_color(self) -> str:
        if not self.isEnabled():
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Disabled")
        elif self.isPressed:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Pressed")
        elif self.isHover:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Hovered")
        else:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Default")

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
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        if not self.isEnabled():
            painter.setOpacity(0.36)
        elif self.isPressed:
            painter.setOpacity(0.78)

        icon_width = self.iconSize().width()
        icon_height = self.iconSize().height()
        icon_y = (self.height() - icon_height) / 2

        text_width = self.fontMetrics().width(self.text()) if self.text() else 0
        spacing = 6

        total_width = icon_width + spacing + text_width if text_width else icon_width
        icon_x = (self.width() - total_width) / 2

        if self.layoutDirection() == Qt.RightToLeft:
            icon_x = self.width() - icon_x - icon_width

        rect = QRectF(icon_x, icon_y, icon_width, icon_height)
        self._icon.paint(painter, rect.toRect())

        painter.end()

class PrimaryToolButton(ToolButton):
    def __init__(self, icon: QIcon = None, parent: QWidget = None):
        super().__init__(icon=icon, parent=parent)
        self.setProperty("class", "PrimaryToolButton")

    def _get_icon_color(self) -> str:
        if not self.isEnabled():
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_On_Accent_Disabled")
        elif self.isPressed:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Inverse")
        elif self.isHover:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Inverse")
        else:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Inverse")
    
class ToggleToolButton(ToolButton):
    def __init__(self, icon: QIcon = None, parent: QWidget = None):
        super().__init__(icon=icon, parent=parent)
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
            if not self.isEnabled():
                return theme_manager.get_current_variables("--ThemeColor_Button_Text_On_Accent_Disabled")
            elif self.isPressed:
                return theme_manager.get_current_variables("--ThemeColor_Button_Text_Inverse")
            elif self.isHover:
                return theme_manager.get_current_variables("--ThemeColor_Button_Text_Inverse")
            else:
                return theme_manager.get_current_variables("--ThemeColor_Button_Text_Inverse")

        if not self.isEnabled():
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Disabled")
        elif self.isPressed:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Pressed")
        elif self.isHover:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Hovered")
        else:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Default")

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
    def __init__(self, icon: QIcon = None, parent: QWidget = None):
        super().__init__(icon=icon, parent=parent)
        self.setProperty("class", "TransparentToolButton")

class TransparentToggleToolButton(ToggleToolButton):
    def __init__(self, icon: QIcon = None, parent: QWidget = None):
        super().__init__(icon=icon, parent=parent)
        self.setProperty("class", "TransparentToggleToolButton")