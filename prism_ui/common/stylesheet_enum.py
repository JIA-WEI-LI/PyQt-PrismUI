import os
from enum import Enum

from ..utils.font_value import FontValue
from ..utils.theme_manager import theme_manager

class ThemeState(Enum):
    DEFAULT = "Default"
    HOVERED = "Hovered"
    PRESSED = "Pressed"
    DISABLED = "Disabled"
    CHECKED = "Checked"
    FOCUS = "Focus"
    ON_ACCENT_DEFAULT = "On_Accent_Default"
    ON_ACCENT_HOVERED = "On_Accent_Hovered"
    ON_ACCENT_PRESSED = "On_Accent_Pressed"
    ON_ACCENT_DISABLED = "On_Accent_Disabled"
    INVERSE = "Inverse"

class ThemeFontType(Enum):
    FAMILY = "Family"
    SIZE = "Size"
    LINEHEIGHT = "Lightheight"
    WEIGHT = "Weight"

class PrismStyleSheet(Enum):
    BUTTON = "button"
    CHECKBOX = "checkbox"
    LISTVIEW = "listview"
    RADIOBUTTON = "radiobutton"
    TEXTBLOCK = "textblock"
    LINEEDIT = "lineedit"
    LISTWIDGET = "listwidget"
    SLIDER = "slider"
    TOOLBUTTON = "toolbutton" 
    TOOLTIP = "tooltip"

    def apply(self, widget):
        widget.setObjectName(self.value)
        theme_manager.register(widget)

    def color(self, part_name: str=None, state: ThemeState = ThemeState.DEFAULT):
        base = self.value.capitalize()
        state_name = str(state.value)
        if part_name:
            return theme_manager.get_current_variables(f"--ThemeColor_{base}_{part_name}_{state_name}")
        else:
            return theme_manager.get_current_variables(f"--ThemeColor_{base}_{state_name}")
        
    def font(self, part_name: str=None, font_type: ThemeFontType = ThemeFontType.FAMILY):
        base = self.value.capitalize()
        state_name = str(font_type.value)
        if part_name:
            value = theme_manager.get_current_variables(f"--ThemeFont_{base}_{part_name}_{state_name}")
        else:
            value = theme_manager.get_current_variables(f"--ThemeFont_{base}_{state_name}")
        
        return FontValue(value) if font_type == ThemeFontType.SIZE else value