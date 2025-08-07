from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QEvent

from ...common.stylesheet_enum import PrismStyleSheet
from ...utils.theme_manager import theme_manager

class ListView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.container = QWidget()
        self.VLayout = QVBoxLayout(self.container)
        self.VLayout.setContentsMargins(0, 0, 0, 0)
        self.VLayout.setSpacing(0)

        self.scroll.setWidget(self.container)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.scroll)
        self.setLayout(main_layout)

        PrismStyleSheet.LISTVIEW.apply(self)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)

    def addItem(self, item: QWidget):
        self.VLayout.addWidget(item)


class ListItem(QWidget):
    clicked = pyqtSignal()

    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self._is_hover = False
        self._is_selected = False

        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.label.setStyleSheet(f"""
            color: {theme_manager.get_current_variables("--ThemeColor_Text_Primary")};
            padding: 6px 12px;
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setFixedHeight(36)
        self.setMouseTracking(True)
        self.installEventFilter(self)

        self.updateStyle()

    def setSelected(self, selected: bool):
        self._is_selected = selected
        self.updateStyle()

    def isSelected(self) -> bool:
        return self._is_selected

    def updateStyle(self):
        bg_color = "--ThemeColor_ListItem_Background_Normal"
        if self._is_selected:
            bg_color = "--ThemeColor_ListItem_Background_Selected"
        elif self._is_hover:
            bg_color = "--ThemeColor_ListItem_Background_Hover"

        color = theme_manager.get_current_variables(bg_color)
        self.setStyleSheet(f"background-color: {color}; border-radius: 4px;")

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Enter:
            self._is_hover = True
            self.updateStyle()
        elif event.type() == QEvent.Type.Leave:
            self._is_hover = False
            self.updateStyle()
        return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
            self.setSelected(True)