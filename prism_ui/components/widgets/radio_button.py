from typing import Union, Callable
from PyQt5.QtWidgets import QWidget, QRadioButton
from PyQt5.QtGui import QIcon, QPainter, QColor
from PyQt5.QtCore import QSize, QRectF, Qt

from .base_widget_mixin import BaseMixin
from ...common.stylesheet_enum import PrismStyleSheet, ThemeState

class RadioButton(QRadioButton, BaseMixin):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, parent=parent)
        self.isPressed = False
        self.isHover = False
        self._icon_source = None

        self.setProperty("class", "RadioButton")
        self.setIconSize(QSize(16, 16))

        if text: self.setText(text)
        if icon: self.setIcon(icon)
        else: self.setIcon(QIcon())

        PrismStyleSheet.RADIOBUTTON.apply(self)
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
        if not self.isEnabled():
            return PrismStyleSheet.RADIOBUTTON.color("Text", ThemeState.DISABLED)
        elif self.isPressed:
            return PrismStyleSheet.RADIOBUTTON.color("Text", ThemeState.PRESSED)
        elif self.isHover:
            return PrismStyleSheet.RADIOBUTTON.color("Text", ThemeState.HOVERED)
        else:
            return PrismStyleSheet.RADIOBUTTON.color("Text", ThemeState.DEFAULT)

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

        border_color = QColor(PrismStyleSheet.RADIOBUTTON.color("Text", ThemeState.DISABLED))
        fill_color = Qt.GlobalColor.transparent
        dot_color = Qt.GlobalColor.transparent

        if self.isChecked():
            dot_color = QColor(PrismStyleSheet.RADIOBUTTON.color("Text", ThemeState.ON_ACCENT_DEFAULT))

            if self.isEnabled():
                border_color = QColor(Qt.GlobalColor.transparent)
                if self.isPressed:
                    fill_color = QColor(PrismStyleSheet.RADIOBUTTON.color("Border", ThemeState.ON_ACCENT_PRESSED))
                elif self.isHover:
                    fill_color = QColor(PrismStyleSheet.RADIOBUTTON.color("Border", ThemeState.ON_ACCENT_HOVERED))
                else:
                    fill_color = QColor(PrismStyleSheet.RADIOBUTTON.color("Border", ThemeState.ON_ACCENT_DEFAULT))
            else:
                border_color = QColor(PrismStyleSheet.RADIOBUTTON.color("Border", ThemeState.ON_ACCENT_DISABLED))
                fill_color = QColor(PrismStyleSheet.RADIOBUTTON.color("Border", ThemeState.ON_ACCENT_DISABLED))
        else:
            if self.isEnabled(): 
                border_color = QColor(PrismStyleSheet.RADIOBUTTON.color("Border", ThemeState.DEFAULT))
            else: 
                border_color = QColor(PrismStyleSheet.RADIOBUTTON.color("Border", ThemeState.DISABLED))

        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(border_color)
        painter.setBrush(fill_color)
        painter.drawEllipse(outer_rect)

        if self.isChecked():
            inner_size = size * 0.5
            inner_offset = (size - inner_size) / 2
            inner_rect = QRectF(cx + inner_offset, cy + inner_offset, inner_size, inner_size)
            painter.setBrush(dot_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(inner_rect)