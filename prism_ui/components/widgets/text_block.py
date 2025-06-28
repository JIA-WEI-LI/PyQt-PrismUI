from typing import Optional
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor

from prism_ui.common.stylesheet_enum import PrismStyleSheet
from prism_ui.utils.theme_manager import theme_manager

class TextBlock(QLabel):
    def __init__(self, *text: str, **kwargs):
        full_text = " ".join(text)

        parent: Optional[QWidget] = kwargs.get("parent", None)
        alignment: Qt.Alignment = kwargs.get("alignment", Qt.AlignmentFlag.AlignLeft)
        font_family: Optional[str] = kwargs.get("font_family", "Segoe UI")
        font_size: Optional[int] = kwargs.get("font_size", 14)
        bold: bool = kwargs.get("bold", False)
        italic: bool = kwargs.get("italic", False)
        underline: bool = kwargs.get("underline", False)
        selectable: bool = kwargs.get("selectable", False)
    
        super().__init__(full_text, parent)

        self.setProperty("class", "TextBlock")
        self.setWordWrap(True)
        self.setAlignment(alignment)

        PrismStyleSheet.TEXT_BLOCK.apply(self)

        font = self.font()
        if font_family:
            font.setFamily(font_family)
        if font_size:
            font.setPointSize(font_size)
        if bold is not None:
            font.setBold(bold)
        if italic is not None:
            font.setItalic(italic)
        if underline is not None:
            font.setUnderline(underline)
        self.setFont(font)

        self.setSelectable(selectable)

    def setSelectable(self, selectable:bool):
        if selectable:
            self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            self.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        else:
            self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))