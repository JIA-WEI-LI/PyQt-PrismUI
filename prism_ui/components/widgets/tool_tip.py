from enum import Enum
from typing import Union
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QGraphicsDropShadowEffect, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer, QPoint, QEvent, QRect

from ...common.stylesheet_enum import PrismStyleSheet

class ToolTipMixin:
    def init_tooltip(self, 
                     delay: int=1000):
        self._tooltip_delay = delay
        self._tooltip_timer = QTimer(self)
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self._tooltip_timer.timeout.connect(self._show_tooltip)

    def setTooltip(self, text: str):
        if not hasattr(self, "tooltip") or self.tooltip is None:
            self.tooltip = ToolTip(text, parent=None)
            self.init_tooltip()
        else:
            self.tooltip.setText(text)
            # self.init_tooltip()

    def setTooltipWithTitle(self, title: str, text: str):
        if not hasattr(self, "tooltip") or self.tooltip is None:
            self.tooltip = TooltipWithTitle(title, text, parent=None)
            self.init_tooltip()
        else:
            self.tooltip.setTitle(title)
            self.tooltip.setContent(text)
            # self.init_tooltip()

    def setToolTipDelay(self, delay_ms: int):
        self._tooltip_delay = delay_ms

    def eventFilter(self, obj, event):
        if obj is self:
            if event.type() == QEvent.Enter:
                self._tooltip_timer.start(self._tooltip_delay)
            elif event.type() == QEvent.Leave:
                self._tooltip_timer.stop()
                if hasattr(self, "_tooltip") and self.tooltip:
                    self.tooltip.hide()

        parent_event_filter = getattr(super(), "eventFilter", None)
        if callable(parent_event_filter):
            return parent_event_filter(obj, event)
        return False

    def _show_tooltip(self):
        if hasattr(self, "_tooltip") and self.tooltip:
            self.tooltip.adjustPos(self)
            self.tooltip.show()

class ToolTip(QFrame):
    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)
        self._text = text
        self._duration = 0

        self._placementRect: Union[QRect, None] = None
        self._verticalOffset = 0
        self._horizontalOffset = 0

        self.useMousePosAsOrigin = False

        self.container = self._createContainer()
        self.timer = QTimer(self)

        self.setLayout(QHBoxLayout())
        self.containerLayout = QHBoxLayout(self.container)
        self.label = QLabel(text, self)

        self.layout().setContentsMargins(12, 8, 12, 12)
        self.layout().addWidget(self.container)
        self.containerLayout.addWidget(self.label)
        self.containerLayout.setContentsMargins(8, 6, 8, 6)

        self.opacityAni = QPropertyAnimation(self, b'windowOpacity', self)
        self.opacityAni.setDuration(150)

        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(25)
        self.shadowEffect.setColor(QColor(0, 0, 0, 50))
        self.shadowEffect.setOffset(0, 5)
        self.container.setGraphicsEffect(self.shadowEffect)

        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)

        PrismStyleSheet.TOOLTIP.apply(self)

    def _createContainer(self) -> QFrame:
        frame = QFrame(self)
        frame.setObjectName("container")
        return frame
    
    def duration(self) -> int:
        return self._duration
    
    def text(self) -> str:
        return self._text

    def setDuration(self, duration: int):
        self._duration = duration

    def setText(self, text: str):
        self._text = text
        self.label.setText(text)
        self.container.adjustSize()
        self.adjustSize()

    def setPlacementRect(self, rect: QRect):
        self._placementRect = rect

    def setVerticalOffset(self, offset: int):
        self._verticalOffset = offset

    def setHorizontalOffset(self, offset: int):
        self._horizontalOffset = offset

    def setUseMousePosAsOrigin(self, use_mouse: bool):
        self.useMousePosAsOrigin = use_mouse

    def showEvent(self, event):
        self.opacityAni.setStartValue(0)
        self.opacityAni.setEndValue(1)
        self.opacityAni.start()

        self.timer.stop()
        if self.duration() > 0:
            self.timer.start(self._duration + self.opacityAni.duration())

        super().showEvent(event)

    def hideEvent(self, event):
        self.timer.stop()
        super().hideEvent(event)

    def adjustPos(self, widget):
        self.adjustSize()
        tooltip_size = self.size()

        if self.useMousePosAsOrigin:
            origin = QCursor.pos()
            pos = QPoint(
                origin.x() + self._horizontalOffset,
                origin.y() + self._verticalOffset,
            )
        else:
            if self._placementRect is None:
                topLeftGlobal = widget.mapToGlobal(QPoint(0, 0))
                placementRect = QRect(topLeftGlobal, widget.size())
            else:
                placementRect = self._placementRect
            
            pos = QPoint(
                placementRect.right() + self._horizontalOffset,
                placementRect.top() + (placementRect.height() - tooltip_size.height()) // 2 + self._verticalOffset
            )

        self.move(pos)

class TooltipWithTitle(ToolTip):
    def __init__(self, title="", text="", parent=None):
        super().__init__(text="", parent=parent)

        self.containerLayout.removeWidget(self.label)
        self.label.deleteLater()

        self.titleLabel = QLabel(title, self)
        self.titleLabel.setObjectName("titleLabel")
        self.textLabel = QLabel(text, self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.titleLabel)
        vbox.addWidget(self.textLabel)
        self.containerLayout.addLayout(vbox)

    def setTitle(self, title: str):
        self.titleLabel.setText(title)
        self.container.adjustSize()
        self.adjustSize()

    def setContent(self, text: str):
        self.textLabel.setText(text)
        self.container.adjustSize()
        self.adjustSize()
