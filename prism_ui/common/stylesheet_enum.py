import os
from enum import Enum

from ..utils.theme_manager import theme_manager

class PrismStyleSheet(Enum):
    BUTTON = "button"
    CHECKBOX = "check_box"
    LISTVIEW = "list_view"
    RADIOBUTTON = "radio_button"
    TEXTBLOCK = "text_block"
    LINEEDIT = "line_edit"
    TOOLBUTTON = "tool_button" 
    TOOLTIP = "tool_tip"

    def apply(self, widget):
        widget.setObjectName(self.value)
        theme_manager.register(widget)