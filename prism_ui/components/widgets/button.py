from typing import Union, Callable
from PyQt5.QtWidgets import QPushButton, QWidget, QToolButton
from PyQt5.QtGui import QIcon, QPainter, QCursor, QDesktopServices, QMouseEvent
from PyQt5.QtCore import QSize, QRectF, Qt, QUrl, QEvent, QTimer

from .base_widget_mixin import BaseMixin
from ...common.stylesheet_enum import PrismStyleSheet
from ...utils.theme_manager import theme_manager

class PushButton(QPushButton, BaseMixin):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, parent=parent)
        self.isPressed = False
        self.isHover = False
        self._icon_cache = {}
        self._icon_source = None
        self._current_icon_color = None

        self.setProperty("class", "PushButton")
        self.setIconSize(QSize(16, 16))
        self.setText(text if text else "")
        self.setIcon(icon if icon else QIcon())

        PrismStyleSheet.BUTTON.apply(self)

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
        if not callable(getattr(self, "_icon_source", None)):
            return
        color = self._get_icon_color()
        if color == self._current_icon_color:
            return
        self._current_icon_color = color
        if color not in self._icon_cache:
            self._icon_cache[color] = self._icon_source(color)
        super().setIcon(self._icon_cache[color])
        self._icon = self._icon_cache[color]

    def enterEvent(self, e): self.isHover = True; self.updateIcon(); super().enterEvent(e)
    def leaveEvent(self, e): self.isHover = False; self.updateIcon(); super().leaveEvent(e)
    def mousePressEvent(self, e): self.isPressed = True; self.updateIcon(); super().mousePressEvent(e)
    def mouseReleaseEvent(self, e): self.isPressed = False; self.updateIcon(); super().mouseReleaseEvent(e)

    def showEvent(self, e):
        super().showEvent(e)
        self.updateIcon()

    def paintEvent(self, e):
        super().paintEvent(e)

        if self._icon.isNull():
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

        if self.layoutDirection() == Qt.LayoutDirection.RightToLeft:
            icon_x = self.width() - icon_x - icon_width

        rect = QRectF(icon_x, icon_y, icon_width, icon_height)
        self._icon.paint(painter, rect.toRect())

        painter.end()

class PrimaryButton(PushButton):
    """
    A primary styled button used in the UI.
    """
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "PrimaryButton")

    def _get_icon_color(self) -> str:
        if not self.isEnabled():
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_On_Accent_Disabled")
        elif self.isPressed:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_On_Accent_Pressed")
        elif self.isHover:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_On_Accent_Hovered")
        else:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_On_Accent_Default")


class ToggleButton(PushButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self._text_on = None
        self._text_off = None
        self._icon_on = None
        self._icon_off = None
        
        self._postInit()
        self.setProperty("class", "ToggleButton")
        
    def _postInit(self):
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self._on_toggle_state_changed)

    def setToggleIcons(self, icon_on: Union[QIcon, Callable], icon_off: Union[QIcon, Callable]):
        self._icon_on = icon_on
        self._icon_off = icon_off
        self._applyToggle()

    def setToggleText(self, text_on: str, text_off: str):
        self._text_on = text_on
        self._text_off = text_off
        self._applyToggle()

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._applyToggle()
        self.updateIcon()

    def _get_icon_color(self) -> str:
        if self.isChecked():
            if not self.isEnabled():
                return theme_manager.get_current_variables("--ThemeColor_Button_Text_On_Accent_Disabled")
            elif self.isPressed:
                return theme_manager.get_current_variables("--ThemeColor_Button_Text_On_Accent_Pressed")
            elif self.isHover:
                return theme_manager.get_current_variables("--ThemeColor_Button_Text_On_Accent_Hovered")
            else:
                return theme_manager.get_current_variables("--ThemeColor_Button_Text_On_Accent_Default")

        if not self.isEnabled():
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Disabled")
        elif self.isPressed:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Pressed")
        elif self.isHover:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Hovered")
        else:
            return theme_manager.get_current_variables("--ThemeColor_Button_Text_Default")

    def _applyToggle(self):
        if self._text_on and self._text_off:
            text = self._text_on if self.isChecked() else self._text_off
            self.setText(text)

        if self._icon_on and self._icon_off:
            icon = self._icon_on if self.isChecked() else self._icon_off
            if callable(icon):
                self.setIconSource(icon)
            else:
                self.setIcon(icon)

    def _on_toggle_state_changed(self, checked: bool):
        self._applyToggle()
        self.updateIcon()

class TransparentPushButton(PushButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "TransparentPushButton")

class TransparentToggleButton(ToggleButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "TransparentToggleButton")

class HyperlinkButton(PushButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None, *args, **kwargs):
        self._url = kwargs.pop("url", None)
        self.auto_prefix_http = kwargs.pop("auto_prefix_http", False)
        self.ctrl_click_enabled = kwargs.pop("ctrl_click_enabled", False)
        self.middle_click_enabled = kwargs.pop("middle_click_enabled", False)

        super().__init__(text=text, icon=icon, parent=parent)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setProperty("class", "HyperlinkButton")

        if self.ctrl_click_enabled:
            self.installEventFilter(self)

        if self._url:
            self.setToolTip(self._url)

    def setUrl(self, url: str):
        self._url = url
        self.setToolTip(url)

    def url(self) -> str:
        return self._url

    def _normalize_url(self, url: str) -> QUrl:
        if self.auto_prefix_http and not url.lower().startswith(("http://", "https://")):
            url = "http://" + url
        return QUrl(url)

    def _open_url(self):
        if self._url:
            QDesktopServices.openUrl(self._normalize_url(self._url))

    def _get_icon_color(self) -> str:
        if not self.isEnabled():
            return theme_manager.get_current_variables("--ThemeColor_Button_Hyper_Disabled")
        elif self.isPressed:
            return theme_manager.get_current_variables("--ThemeColor_Button_Hyper_Pressed")
        elif self.isHover:
            return theme_manager.get_current_variables("--ThemeColor_Button_Hyper_Hovered")
        else:
            return theme_manager.get_current_variables("--ThemeColor_Button_Hyper_Default")

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.MiddleButton and self.middle_click_enabled:
            self._open_url()
        elif event.button() == Qt.MouseButton.LeftButton:
            if self.ctrl_click_enabled:
                if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                    self._open_url()
                return
            else:
                self._open_url()
        super().mouseReleaseEvent(event)

    def eventFilter(self, obj, event):
        if obj is self and event.type() == QEvent.Type.MouseButtonRelease:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                return True
        return super().eventFilter(obj, event)

class RepeatButton(PushButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None, *args, **kwargs):
        super().__init__(text=text, icon=icon, parent=parent)

        self.setAutoRepeat(False)
        self._repeat_delay = kwargs.pop("repeat_delay", 400)
        self._repeat_interval = kwargs.pop("repeat_interval", 100)

        self._repeat_timer = QTimer(self)
        self._repeat_timer.timeout.connect(self._on_repeat_timeout)

        self.pressed.connect(self._start_repeat)
        self.released.connect(self._stop_repeat)
        self.setProperty("class", "PushButton")

    def _start_repeat(self):
        self._repeat_timer.start(self._repeat_delay)

    def _stop_repeat(self):
        self._repeat_timer.stop()

    def _on_repeat_timeout(self):
        self.click()
        self._repeat_timer.setInterval(self._repeat_interval)

    def setRepeatDelay(self, delay_ms: int):
        self._repeat_delay = delay_ms

    def setRepeatInterval(self, interval_ms: int):
        self._repeat_interval = interval_ms

    def repeatDelay(self) -> int:
        return self._repeat_delay

    def repeatInterval(self) -> int:
        return self._repeat_interval
    
class SegmentedButton(ToggleButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "SegmentedButton")