from PyQt5.QtWidgets import QAction, QToolButton, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QRectF, Qt

from .tool_button import TransparentToolButton
from ...icon_manager.blender_icon import BlenderIcon
from ...common.stylesheet_enum import PrismStyleSheet
from ...utils.theme_manager import theme_manager

class LineEditButton(TransparentToolButton):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.isPressed = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(23, 23)

    def action(self):
        return self._action

    def setAction(self, action: QAction):
        self._action = action
        self._onActionChanged()
        self.clicked.connect(action.trigger)
        action.toggled.connect(self.setChecked)
        action.changed.connect(self._onActionChanged)

    def _onActionChanged(self):
        action = self.action()
        self.setEnabled(action.isEnabled())
        self.setVisible(action.isVisible())
        self.setCheckable(action.isCheckable())
        self.setChecked(action.isChecked())

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

class LineEdit(QLineEdit):
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.leftButtons = []
        self.rightButtons = []
        self._isClearButtonEnabled = False
        self.setProperty("class", "LineEdit")

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(4, 4, 4, 4)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        PrismStyleSheet.LINEEDIT.apply(self)

    def addAction(self, action: QAction, position: QLineEdit.ActionPosition = QLineEdit.ActionPosition.TrailingPosition):
        button = LineEditButton(action.icon(), self)
        button.setAction(action)

        if position == QLineEdit.ActionPosition.LeadingPosition:
            self.hBoxLayout.insertWidget(len(self.leftButtons), button, 0, Qt.AlignmentFlag.AlignLeading)
            if not self.leftButtons:
                self.hBoxLayout.insertStretch(1, 1)
            self.leftButtons.append(button)
        else:
            insert_index = len(self.hBoxLayout) - len(self.rightButtons)
            self.hBoxLayout.insertWidget(insert_index, button, 0, Qt.AlignmentFlag.AlignRight)
            self.rightButtons.append(button)

        self._adjustTextMargins()

    def isClearButtonEnabled(self) -> bool:
        return self._isClearButtonEnabled

    def _adjustTextMargins(self):
        left = len(self.leftButtons) * 30
        right = len(self.rightButtons) * 30
        if self.isClearButtonEnabled():
             right += 28
        m = self.textMargins()
        self.setTextMargins(left, m.top(), right, m.bottom())

    def enterEvent(self, a0):
        self.setCursor(Qt.CursorShape.IBeamCursor)
        return super().enterEvent(a0)

class TextBox(LineEdit):
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self._isClearButtonEnabled = True
        self._alwaysVisible = False

        self.clearButton = LineEditButton(BlenderIcon.CLOSE, self)
        self.hBoxLayout.addWidget(self.clearButton, 0, Qt.AlignmentFlag.AlignRight)

        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self._updateClearButtonVisibility)
        
        self._updateClearButtonVisibility()
        self._adjustTextMargins()

    def _updateClearButtonVisibility(self):
        should_be_visible = (self.hasFocus() and bool(self.text()) and self.isClearButtonEnabled()) or self._alwaysVisible
        self.clearButton.setVisible(should_be_visible)

    def setClearButtonAlwaysVisible(self, always_visible: bool=True):
        self._alwaysVisible = always_visible
        self._updateClearButtonVisibility()

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self._updateClearButtonVisibility()

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self._updateClearButtonVisibility()