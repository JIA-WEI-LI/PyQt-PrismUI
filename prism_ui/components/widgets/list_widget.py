from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import Qt

from ...common.stylesheet_enum import PrismStyleSheet, ThemeState

class ListWidget(QListWidget):
    def __init__(self):
        super().__init__(parent=None)

        self.setProperty("class", "ListWidget")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        PrismStyleSheet.LISTWIDGET.apply(self)

ListBox = ListWidget