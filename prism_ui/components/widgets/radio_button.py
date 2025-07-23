from typing import Union, Callable
from PyQt5.QtWidgets import QWidget, QRadioButton
from PyQt5.QtGui import QIcon, QPainter, QColor
from PyQt5.QtCore import QSize, QRectF, Qt

from ...common.stylesheet_enum import PrismStyleSheet
from ...utils.theme_manager import theme_manager

class RadioButton(QRadioButton):
    def __init__(self, *args, **kwargs):
        icon = None
        parent = None
        text = None

        for arg in args:
            if isinstance(arg, str) and text is None: text = arg
            elif isinstance(arg, (QIcon, str)) and icon is None: icon = arg
            elif isinstance(arg, QWidget) and parent is None: parent = arg

        parent = kwargs.get("parent", parent)
        icon = kwargs.get("icon", icon)
        text = kwargs.get("text", text)

        super().__init__(parent)
        self.isPressed = False
        self.isHover = False
        self._icon_source = None

        self.setProperty("class", "RadioButton")
        self.setIconSize(QSize(16, 16))

        if text: self.setText(text)
        if icon: self.setIcon(icon)
        else: self.setIcon(QIcon())

        PrismStyleSheet.RADIO_BUTTON.apply(self)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)    # macOS

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
        if self.isEnabled():
            if self.isHover:
                return theme_manager.get_current_variables("--ThemeColor_Text_Secondary")
            elif self.isPressed:
                return theme_manager.get_current_variables("--ThemeColor_Text_Tertiary")
            else:
                return theme_manager.get_current_variables("--ThemeColor_Text_Default")
        else:
            return theme_manager.get_current_variables("--ThemeColor_Text_Disabled")

    def updateIcon(self):
        if hasattr(self, "_icon_source") and callable(self._icon_source):
            try:
                color = self._get_icon_color()
                icon = self._icon_source(color)
                if icon:
                    super().setIcon(icon)
                    self._icon = icon
            except Exception as e:
                print(f"[RadioButton] Failed to update icon: {e}")

    # region Events
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

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        self._drawIndicator(painter)
        painter.end()

    def _drawIndicator(self, painter: QPainter):
        size = 16
        cx = 4
        cy = (self.height() - size) // 2
        outer_rect = QRectF(cx, cy, size, size)

        is_checked = self.isChecked()
        is_enabled = self.isEnabled()
        is_hover = self.isHover
        is_pressed = self.isPressed

        border_color = QColor(theme_manager.get_current_variables("--ThemeColor_Text_Disabled"))
        fill_color = Qt.GlobalColor.transparent
        dot_color = Qt.GlobalColor.transparent

        if is_checked:
            if is_enabled:
                border_color = QColor(Qt.GlobalColor.transparent)
                if is_hover: fill_color = QColor(theme_manager.get_current_variables("--ThemeColor_Accent_Secondary"))
                elif is_pressed: fill_color = QColor(theme_manager.get_current_variables("--ThemeColor_Accent_Tertiary"))
                else: fill_color = QColor(theme_manager.get_current_variables("--ThemeColor_Accent_Default"))
            else:
                border_color = QColor(theme_manager.get_current_variables("--ThemeColor_Control_Strong_Disabled"))
                fill_color = QColor(theme_manager.get_current_variables("--ThemeColor_Accent_Disabled"))
            dot_color = QColor(theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Default"))
        else:
            if is_enabled: border_color = QColor(theme_manager.get_current_variables("--ThemeColor_Control_Strong_Default"))
            else: border_color = QColor(theme_manager.get_current_variables("--ThemeColor_Control_Strong_Disabled"))

        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(border_color)
        painter.setBrush(fill_color)
        painter.drawEllipse(outer_rect)

        if is_checked:
            inner_size = size * 0.5
            inner_offset = (size - inner_size) / 2
            inner_rect = QRectF(cx + inner_offset, cy + inner_offset, inner_size, inner_size)
            painter.setBrush(dot_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(inner_rect)