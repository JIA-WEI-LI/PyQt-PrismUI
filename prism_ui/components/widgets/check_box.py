from typing import Union, Callable
from PyQt5.QtWidgets import QCheckBox, QWidget, QStyleOptionButton, QStyle
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QSize, Qt, QRect

from .tool_tip import ToolTipMixin
from ...common.stylesheet_enum import PrismStyleSheet
from ...icon_manager.blender_icon import BlenderIcon
from ...utils.theme_manager import theme_manager

class CheckBox(QCheckBox, ToolTipMixin):
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
        if self.isEnabled():
            if self.isHover:
                color = theme_manager.get_current_variables("--ThemeColor_Text_Secondary")
            elif self.isPressed:
                color = theme_manager.get_current_variables("--ThemeColor_Text_Tertiary")
            else:
                color = theme_manager.get_current_variables("--ThemeColor_Text_Default")
        else:
            color = theme_manager.get_current_variables("--ThemeColor_Text_Disabled")
        return color
    
    def _get_indicator_icon_color(self):
        if self.isEnabled():
            if self.isHover:
                color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Secondary")
            elif self.isPressed:
                color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Tertiary")
            else:
                color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Default")
        else:
            color = theme_manager.get_current_variables("--ThemeColor_Text_On_Accent_Disabled")
        return color

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
                return QColor(theme_manager.get_current_variables('--ThemeColor_Control_Strong_Disabled'))
            elif self.isChecked():
                return QColor(theme_manager.get_current_variables('--ThemeColor_Accent_Default'))
            elif self.isHover:
                return QColor(theme_manager.get_current_variables('--ThemeColor_Control_Secondary'))
            else:
                return QColor(theme_manager.get_current_variables('--ThemeColor_Control_Default'))

        def _border_color():
            if not self.isEnabled():
                return QColor(theme_manager.get_current_variables('--ThemeColor_Text_Disabled'))
            elif self.isChecked():
                return QColor(theme_manager.get_current_variables('--ThemeColor_Text_On_Accent_Default'))
            elif self.isHover:
                return QColor(theme_manager.get_current_variables('--ThemeColor_Text_Secondary'))
            else:
                return QColor(theme_manager.get_current_variables('--ThemeColor_Text_Default'))

        painter.setBrush(_background_color())
        painter.setPen(QPen(_border_color(), 0.1))
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