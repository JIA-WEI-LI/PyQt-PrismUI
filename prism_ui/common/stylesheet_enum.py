import os
from enum import Enum
from prism_ui.utils.theme_manager import theme_manager

class PrismStyleSheet(Enum):
    BUTTON = "button"

    def apply(self, widget):
        widget.setObjectName(self.value)
        theme_manager.register(widget)