from typing import Optional
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor

from .base_widget_mixin import BaseMixin
from ...common.stylesheet_enum import PrismStyleSheet

class TextBlock(QLabel, BaseMixin):
    def __init__(self, *text: str, **kwargs):
        full_text = " ".join(text)

        parent: Optional[QWidget] = kwargs.get("parent", None)
        typography: str = kwargs.get("typography", "body")
    
        super().__init__(full_text, parent)

        self.setProperty("class", "TextBlock")
        self.setProperty("typography", str(typography).lower())
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setWordWrap(True)

        self.setSelectable(False)

        PrismStyleSheet.TEXTBLOCK.apply(self)

        self.setStyle(self.style())

    def setSelectable(self, selectable:bool):
        if selectable:
            self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            self.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        else:
            self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))