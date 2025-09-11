from typing import Union, Callable
from PyQt5.QtWidgets import QCheckBox, QWidget, QStyleOptionButton, QStyle
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QSize, Qt, QRect

from .base_widget_mixin import BaseMixin
from ...common.stylesheet_enum import PrismStyleSheet, ThemeState
from ...icon_manager.blender_icon import BlenderIcon

class CheckBox(QCheckBox, BaseMixin):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text, parent)
        self.isPressed = False
        self.isHover = False
        self._icon_source = None

        self.setProperty("class", "CheckBox")
        self.setIconSize(QSize(16, 16))

        if text: self.setText(text)
        if icon: self.setIcon(icon)
        else: self.setIcon(QIcon())
        self.setIndicatorIconSource(BlenderIcon.CHECK)

        PrismStyleSheet.CHECKBOX.apply(self)

    def setIcon(self, icon: Union[QIcon, Callable]):
        if callable(icon):
            self.setIconSource(icon)
        else:
            super().setIcon(icon)
            self._icon_source = None
            self._icon = icon

    def setIconSource(self, icon_accessor):
        self._icon_source = icon_accessor
        self.updateIcon()

    def setIndicatorIconSource(self, accessor: Callable[[str], QIcon]):
        self._indicator_icon_source = accessor
        self.update()

    def _get_icon_color(self) -> str:
        if not self.isEnabled():
            return PrismStyleSheet.CHECKBOX.color("Text", ThemeState.DISABLED)
        elif self.isPressed:
            return PrismStyleSheet.CHECKBOX.color("Text", ThemeState.PRESSED)
        elif self.isHover:
            return PrismStyleSheet.CHECKBOX.color("Text", ThemeState.HOVERED)
        else:
            return PrismStyleSheet.CHECKBOX.color("Text", ThemeState.DEFAULT)
    
    def _get_indicator_icon_color(self):
        if not self.isEnabled():
            return PrismStyleSheet.CHECKBOX.color("Text", ThemeState.ON_ACCENT_DISABLED)
        elif self.isPressed:
            return PrismStyleSheet.CHECKBOX.color("Text", ThemeState.ON_ACCENT_PRESSED)
        elif self.isHover:
            return PrismStyleSheet.CHECKBOX.color("Text", ThemeState.ON_ACCENT_HOVERED)
        else:
            return PrismStyleSheet.CHECKBOX.color("Text", ThemeState.ON_ACCENT_DEFAULT)

    def updateIcon(self):
        if hasattr(self, "_icon_source") and callable(self._icon_source):
            try:
                color = self._get_icon_color()
                icon = self._icon_source(color)
                if icon:
                    super().setIcon(icon)
                    self._icon = icon
                    self.update()
            except Exception as e:
                print(f"[CheckBox] Failed to update icon: {e}")

    def enterEvent(self, event):
        self.isHover = True
        super().enterEvent(event)
        self.update()

    def leaveEvent(self, event):
        self.isHover = False
        super().leaveEvent(event)
        self.update()

    def mousePressEvent(self, event):
        self.isPressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.isPressed = False
        super().mouseReleaseEvent(event)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        opt = QStyleOptionButton()
        self.initStyleOption(opt)
        rect = self.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, opt, self)

        def _background_color():
            if not self.isEnabled():
                return PrismStyleSheet.CHECKBOX.color("Background", ThemeState.DISABLED)
            elif self.isChecked() and self.isHover:
                return PrismStyleSheet.CHECKBOX.color("Background", ThemeState.ON_ACCENT_HOVERED)
            elif self.isChecked():
                return PrismStyleSheet.CHECKBOX.color("Background", ThemeState.CHECKED)
            elif self.isHover:
                return PrismStyleSheet.CHECKBOX.color("Background", ThemeState.HOVERED)
            else:
                return PrismStyleSheet.CHECKBOX.color("Background", ThemeState.DEFAULT)

        def _border_color():
            if not self.isEnabled():
                return PrismStyleSheet.CHECKBOX.color("Border", ThemeState.DISABLED)
            elif self.isChecked():
                return PrismStyleSheet.CHECKBOX.color("Border", ThemeState.CHECKED)
            elif self.isHover:
                return PrismStyleSheet.CHECKBOX.color("Border", ThemeState.HOVERED)
            else:
                return PrismStyleSheet.CHECKBOX.color("Border", ThemeState.DEFAULT)

        painter.setBrush(QColor(_background_color()))
        painter.setPen(QPen(QColor(_border_color()), 0.1))
        painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), 5, 5)

        color = self._get_indicator_icon_color()
        indicator_icon = None

        if self.checkState() in (Qt.CheckState.Checked, Qt.CheckState.PartiallyChecked):
            if hasattr(self, "_indicator_icon_source") and callable(self._indicator_icon_source):
                try:
                    indicator_icon = self._indicator_icon_source(color)
                except Exception as e:
                    print(f"[CheckBox] Failed to get themed indicator icon: {e}")
            else:
                if self.checkState() == Qt.CheckState.Checked:
                    indicator_icon = QIcon(BlenderIcon.CHECK) if isinstance(BlenderIcon.CHECK, str) else BlenderIcon.CHECK
                elif self.checkState() == Qt.CheckState.PartiallyChecked:
                    indicator_icon = QIcon(BlenderIcon.PARTICLES) if isinstance(BlenderIcon.PARTICLES, str) else BlenderIcon.PARTICLES

        if isinstance(indicator_icon, QIcon):
            pixmap = indicator_icon.pixmap(rect.size(), QIcon.Mode.Normal if self.isEnabled() else QIcon.Mode.Disabled)
            painter.drawPixmap(rect, pixmap)

        painter.end()