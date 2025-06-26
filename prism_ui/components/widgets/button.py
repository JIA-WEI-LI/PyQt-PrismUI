from typing import Union, Optional, Callable
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QIcon, QPainter, QCursor, QDesktopServices, QMouseEvent
from PyQt5.QtCore import QSize, QRectF, Qt, QUrl, QEvent, QTimer

from prism_ui.common.stylesheet_enum import PrismStyleSheet
from prism_ui.utils.theme_manager import theme_manager

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
        self._icon_source = None

        self.setProperty("class", "PushButton")
        self.setIconSize(QSize(16, 16))

        if text: self.setText(text)
        if icon: self.setIcon(icon)
        else: self.setIcon(QIcon())

        # self._icon = self.icon()
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
        if self.isChecked():
            if self.isEnabled():
                if self.isHover: color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Default")
                elif self.isPressed: color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Tertiary")
                else: color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Default")
            elif not self.isEnabled():
                color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Disabled")
        else:
            if self.isEnabled():
                if self.isHover: color = theme_manager.get_current_variables("--ThemeColor_Text_Secondary")
                elif self.isPressed: color = theme_manager.get_current_variables("--ThemeColor_Text_Tertiary")
                else: color = theme_manager.get_current_variables("--ThemeColor_Text_Default")
            elif not self.isEnabled():
                color = theme_manager.get_current_variables("--ThemeColor_Text_Disabled")

        return color

    def updateIcon(self):
        if hasattr(self, "_icon_source") and callable(self._icon_source):
            try:
                color = self._get_icon_color()
                icon = self._icon_source(color)
                if icon:
                    super().setIcon(icon)
                    self._icon = icon
            except Exception as e:
                print(f"[PushButton] Failed to update icon: {e}")

# region Event
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
# endregion

    def showEvent(self, e):
        super().showEvent(e)
        self.updateIcon()

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setProperty("class", "PrimaryPushButton")

    def _get_icon_color(self) -> str:
        if self.isEnabled():
            if self.isHover: color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Secondary")
            elif self.isPressed: color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Tertiary")
            else: color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Default")
        elif not self.isEnabled():
            color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Disabled")

        return color

class ToggleButton(PushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._applyToggle()
        self.updateIcon()

class TransparentPushButton(PushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setProperty("class", "TransparentPushButton")

class TransparentToggleButton(ToggleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setProperty("class", "TransparentToggleButton")

class HyperlinkButton(PushButton):
    def __init__(self, *args, **kwargs):
        self._url = kwargs.pop("url", None)
        self.auto_prefix_http = kwargs.pop("auto_prefix_http", False)
        self.ctrl_click_enabled = kwargs.pop("ctrl_click_enabled", False)
        self.middle_click_enabled = kwargs.pop("middle_click_enabled", False)

        super().__init__(*args, **kwargs)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setProperty("class", "HyperlinkButton")

        if self._url:
            self.setToolTip(self._url)

        if self.ctrl_click_enabled:
            self.installEventFilter(self)

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
        if self.isEnabled():
            if self.isHover:
                return theme_manager.get_current_variables("--ThemeColor_Text_Accent_Secondary")
            elif self.isPressed:
                return theme_manager.get_current_variables("--ThemeColor_Text_Accent_Tertiary")
            else:
                return theme_manager.get_current_variables("--ThemeColor_Text_Accent_Default")
        else:
            return theme_manager.get_current_variables("--ThemeColor_Text_Accent_Disabled")

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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