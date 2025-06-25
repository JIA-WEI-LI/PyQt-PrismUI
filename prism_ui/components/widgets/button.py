from typing import Union, Optional
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import QSize, QRectF, Qt

from prism_ui.common.stylesheet_enum import PrismStyleSheet

class PushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        text = None
        icon = None
        parent = None

        for arg in args:
            if isinstance(arg, str) and text is None: text = arg
            elif isinstance(arg, (QIcon, str)) and icon is None: icon = arg
            elif isinstance(arg, QWidget) and parent is None: parent = arg

        parent = kwargs.get("parent", parent)
        text = kwargs.get("text", text)
        icon = kwargs.get("icon", icon)

        super().__init__(parent)
        self.isPressed = False
        self.isHover = False
        self.setIconSize(QSize(16, 16))

        if text: self.setText(text)
        if icon: self.setIcon(icon)
        else: self.setIcon(QIcon())

        self._icon = self.icon()
        PrismStyleSheet.BUTTON.apply(self)

    def setIcon(self, icon: Union[str, QIcon]):
        if isinstance(icon, str):
            icon = QIcon(icon)
        super().setIcon(icon)
        self._icon = icon

# region Event
    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

    def enterEvent(self, e):
        self.isHover = True
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.isHover = False
        self.update()
        super().leaveEvent(e)
# endregion

    def paintEvent(self, e):
        super().paintEvent(e)

        if self._icon.isNull():
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

class PrimaryPushButton(PushButton):
    """PrimaryPushButton"""