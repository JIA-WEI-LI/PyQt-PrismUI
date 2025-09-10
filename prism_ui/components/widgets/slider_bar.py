from typing import Union
from PyQt5.QtWidgets import QApplication, QProgressBar, QSizePolicy, QStyle, QStyleOption, QStyleOptionProgressBar, QWidget
from PyQt5.QtGui import QColor, QCursor, QFont, QMouseEvent, QPainter
from PyQt5.QtCore import QEvent, QPointF, Qt

from ...common.stylesheet_enum import PrismStyleSheet, ThemeState
from ...utils.theme_manager import theme_manager

class PrismSliderStyle(QStyle):
    def drawControl(
            self, 
            element: QStyle.ControlElement, 
            option: QStyleOption, 
            painter: QPainter, 
            background_color: str,
            sliderbar_color: str,
            widget: QWidget = None):
        self.widget = widget
        if element == QStyle.ControlElement.CE_ProgressBar:
            if isinstance(option, QStyleOptionProgressBar):
                self.drawProgressBar(option, painter, background_color, sliderbar_color)

    def drawProgressBar(
            self, 
            option: QStyleOptionProgressBar, 
            painter: QPainter, 
            background_color: str,
            sliderbar_color: str):
        background_rect = option.rect
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(background_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(background_rect, 5, 5)
        
        progress_rect = background_rect.adjusted(0, 0, 0, 0)
        progress_width = int(progress_rect.width() * (option.progress / 100.0))
        progress_rect.setWidth(progress_width)

        painter.setBrush(QColor(sliderbar_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(progress_rect, 5, 5)

class PrismSliderBar(QProgressBar):
    def __init__(self, text="Value", initial_value: Union[float, int]=0.5, parent=None, *args,
                 decimal_places:int=2, **kwargs):
        super().__init__(parent)
        self._text = text
        self._value = self.value()
        
        self._background_color = PrismStyleSheet.SLIDER.color("Background", ThemeState.DEFAULT)
        self._sliderbar_color = PrismStyleSheet.SLIDER.color("Sliderbar", ThemeState.DEFAULT)
        self.initial_value = initial_value
        self.decimal_places = decimal_places
        self.apply_style = False

        self.isHover = False
        self.isDragging = False
        self.isPressed = False

        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(50)
        self._setInitialValue(self.initial_value)

        PrismStyleSheet.SLIDER.apply(self)

    def _setInitialValue(self, initial_value: Union[float, int]):
        if isinstance(initial_value, float) and 0 <= initial_value <= 1:
            self.setValue(int(initial_value * 100))
        elif isinstance(initial_value, int) or isinstance(initial_value, float):
            self.setValue(initial_value)
        else: raise TypeError("initial_value must be a float or an integer")

    def mousePressEvent(self, event: QMouseEvent):
        self.isPressed = True
        self._getColor()
        if event.buttons() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            self.isDragging = True
            self.update()
            self.updateProgress(event)
            QApplication.setOverrideCursor(QCursor(Qt.CursorShape.BlankCursor))
    
    def mouseMoveEvent(self, event):
        if hasattr(self, 'isDragging') and self.isDragging:
            self.updateProgress(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.isPressed = False
        if hasattr(self, 'isDragging') and self.isDragging:
            self.isDragging = False
            QApplication.restoreOverrideCursor()
            self.update()
        else:
            super().mouseReleaseEvent(event)

    def enterEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.isHover = True
        self._getColor()
        self.update()

    def leaveEvent(self, event: QEvent) -> None:
        super().enterEvent(event)
        self.isHover = False
        self._getColor()
        self.update()

    def _getColor(self) -> str:
        if not self.isEnabled():
            self._background_color = PrismStyleSheet.SLIDER.color("Background", ThemeState.DISABLED)
            self._sliderbar_color = PrismStyleSheet.SLIDER.color("Sliderbar", ThemeState.DISABLED)
        elif self.isPressed:
            self._background_color = PrismStyleSheet.SLIDER.color("Background", ThemeState.PRESSED)
            self._sliderbar_color = PrismStyleSheet.SLIDER.color("Sliderbar", ThemeState.PRESSED)
        elif self.isHover:
            self._background_color = PrismStyleSheet.SLIDER.color("Background", ThemeState.HOVERED)
            self._sliderbar_color = PrismStyleSheet.SLIDER.color("Sliderbar", ThemeState.HOVERED)
        else:
            self._background_color = PrismStyleSheet.SLIDER.color("Background", ThemeState.DEFAULT)
            self._sliderbar_color = PrismStyleSheet.SLIDER.color("Sliderbar", ThemeState.DEFAULT)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        style = PrismSliderStyle()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        opt = QStyleOptionProgressBar()
        self.initStyleOption(opt)
        opt.rect = self.rect().adjusted(1, 1, -1, -1)
        opt.textVisible = self.isTextVisible()

        style.drawControl(QStyle.ControlElement.CE_ProgressBar, opt, painter, self._background_color, self._sliderbar_color, self)

        painter.setBackgroundMode(Qt.BGMode.TransparentMode)
        painter.setPen(QColor(Qt.GlobalColor.white))
        painter.drawText(QPointF(10, self.height() / 2 + 5), self._text)

        progress = self.value() * (self.maximum() - self.minimum()) / 100 + self.minimum()
        text = f"{progress:.{self.decimal_places}f}"
        text_rect = painter.boundingRect(self.rect(), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)
        text_rect.adjust(-5, 0, -5, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, text)

    def updateProgress(self, event):
        mouse_x = event.x()
        total_width = self.width()

        progress_percent = mouse_x / total_width
        if progress_percent < 0:
            self.setValue(0)
            return
        if progress_percent > 1:
            self.setValue(100)
            return
        self.setValue(int(progress_percent * 100))