from PyQt5.QtWidgets import QAction, QWidget, QLineEdit, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt, QRectF, QEvent
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPen

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
        self._isClearButtonEnabled = True
        self._clearButtonAlwaysVisible = False
        self.setProperty("class", "LineEdit")

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(4, 4, 4, 4)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.clearButton = LineEditButton(BlenderIcon.CLOSE, self)
        self.hBoxLayout.addWidget(self.clearButton, 0, Qt.AlignmentFlag.AlignRight)
        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self._updateClearButtonVisibility)

        self._updateClearButtonVisibility()
        self._adjustTextMargins()

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

    def _updateClearButtonVisibility(self):
        should_be_visible = (self.hasFocus() and bool(self.text() and not self.isReadOnly()) and self.isClearButtonEnabled()) or self._clearButtonAlwaysVisible
        self.clearButton.setVisible(should_be_visible)

    def setClearButtonAlwaysVisible(self, always_visible: bool=True):
        self._clearButtonAlwaysVisible = always_visible
        self._updateClearButtonVisibility()

    def enterEvent(self, a0):
        self.setCursor(Qt.CursorShape.IBeamCursor)
        return super().enterEvent(a0)
    
    def focusInEvent(self, e):
        super().focusInEvent(e)
        self._updateClearButtonVisibility()

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self._updateClearButtonVisibility()

    def paintEvent(self, e):
        super().paintEvent(e)
        border_color = "--ThemeColor_Lineedit_Border_Default" if not self.hasFocus() else "--ThemeColor_Lineedit_Border_Focus"

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        m = self.contentsMargins()
        border_width  = self.width() - m.left() - m.right()
        border_height= self.height()

        path = QPainterPath()
        path.addRoundedRect(QRectF(m.left(), border_height - 10, border_width, 10), 5, 5)

        rectPath = QPainterPath()
        rectPath.addRect(m.left(), border_height - 10, border_width, 8)
        path = path.subtracted(rectPath)
        
        painter.fillPath(path, QColor(theme_manager.get_current_variables(border_color)))

class EditOverlay(QWidget):
    def __init__(self, parent_widget):
        super().__init__(parent_widget)
        self.parent_widget = parent_widget
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysStackOnTop)
        parent_widget.installEventFilter(self)
        self.resize(parent_widget.size())

    def eventFilter(self, obj, event: QEvent):
        if obj is self.parent() and event.type() == QEvent.Type.Resize:
            self.resize(event.size())

        return super().eventFilter(obj, event)

    def paintEvent(self, e):
        border_color = "--ThemeColor_Lineedit_Border_Default" if not self.parent_widget.hasFocus() else "--ThemeColor_Lineedit_Border_Focus"

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        m = self.contentsMargins()
        path = QPainterPath()
        w, h = self.width()-m.left()-m.right(), self.height()
        path.addRoundedRect(QRectF(m.left(), h-10, w, 10), 5, 5)

        rectPath = QPainterPath()
        rectPath.addRect(m.left(), h-10, w, 7.5)
        path = path.subtracted(rectPath)

        painter.fillPath(path, QColor(theme_manager.get_current_variables(border_color)))

class TextEdit(QTextEdit):
    def __init__(self, text: str="", parent=None):
        super().__init__(parent)
        self.layout = EditOverlay(self)

        self.setProperty("class", "TextEdit")
        PrismStyleSheet.LINEEDIT.apply(self)

class TextBox(QWidget):
    def __init__(self, text: str = "", accepts_return: bool = False, parent=None):
        super().__init__(parent)

        self._accept_return = accepts_return
        self._editor = QTextEdit(text, self) if self._accept_return else LineEdit(text, self)

        layout = QHBoxLayout(self)
        layout.addWidget(self._editor)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setProperty("class", "LineEdit")
        PrismStyleSheet.LINEEDIT.apply(self)

    def __getattr__(self, name):
        return getattr(self._editor, name)

    def setAcceptsReturn(self, accepts_return: bool=False):
        self._accept_return = accepts_return
        text = self._editor.text() if isinstance(self._editor, LineEdit) else self._editor.toPlainText()
        self._editor = QTextEdit(text, self) if self._accept_return else LineEdit(text, self)
        