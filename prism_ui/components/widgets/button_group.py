from typing import Union, List, Optional, Tuple
from functools import partial
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from .button import PushButton, ToggleButton

# TODO: 按鈕QSS在位置上仍未實際套用(如：左側按鈕右邊仍有圓角)
class BaseButtonGroup(QWidget):

    buttonClicked = pyqtSignal(object)

    def __init__(
        self,
        labels,
        parent: Optional[QWidget] = None,
        buttonClass: type = QPushButton,
        useFlatId: bool = False,
    ):
        super().__init__(parent)

        self.buttonClass = buttonClass
        self._buttons = []
        self._buttonIdMap = {}
        self._idButtonMap = {}
        self.useFlatId = useFlatId
        self._disabledIds = set()
        self._nextId = 0

        self.setHorizontalSpacing(1)
        self.setVerticalSpacing(1)

        if isinstance(labels[0], list):
            self._isGrid = True
            self._gridLabels = labels
            self._cols = max(len(row) for row in labels)
        else:
            self._isGrid = False
            self._flatLabels = labels

        layout = self._setupLayout()
        self.setLayout(layout)

    def _cornerRadiusForIndex(self, index: int, total: int):
        if self._isGrid:
            rows = len(self._gridLabels)
            cols = max(len(row) for row in self._gridLabels)

            if rows == 1:
                return "left" if index == 0 else ("right" if index == cols - 1 else "center")
            if cols == 1:
                return "top" if index == 0 else ("bottom" if index == rows - 1 else "center")

            r = index // cols
            c = index % cols
            if r == 0:
                return "top-left" if c == 0 else ("top-right" if c == cols - 1 else "center")
            elif r == rows - 1:
                return "bottom-left" if c == 0 else ("bottom-right" if c == cols - 1 else "center")
            else:
                return "center"
        else:
            return "left" if index == 0 else ("right" if index == total - 1 else "center")
            
    def _setupLayout(self):
        if self._isGrid:
            layout = QGridLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setHorizontalSpacing(self._horizontalSpacing)
            layout.setVerticalSpacing(self._verticalSpacing)
            total = sum(len(row) for row in self._gridLabels)
            flat_idx = 0
            for r, row in enumerate(self._gridLabels):
                for c, text in enumerate(row):
                    btn_id = flat_idx if self.useFlatId else (r, c)
                    button: PushButton = self._createButton(text, btn_id)
                    print(f" [button_group.py] BaseButtonGroup._setupLayout(): -> self._createButton({text}, {btn_id})")
                    corner = self._cornerRadiusForIndex(flat_idx, total)
                    print(f" [button_group.py] BaseButtonGroup._setupLayout(): -> {corner} = self._cornerRadiusForIndex({flat_idx}, {total})")
                    button.setProperty("position", corner)
                    print(f" [button_group.py] BaseButtonGroup._setupLayout(): -> {[bytes(name).decode() for name in button.dynamicPropertyNames()]}")
                    layout.addWidget(button, r, c)
                    flat_idx += 1
        else:
            layout = QHBoxLayout()
            layout.setContentsMargins(0, self._verticalSpacing, 0, self._verticalSpacing)
            layout.setSpacing(self._horizontalSpacing)
            total = len(self._flatLabels)
            for idx, text in enumerate(self._flatLabels):
                button: PushButton = self._createButton(text, idx)
                print(f" [button_group.py] BaseButtonGroup._setupLayout(): -> self._createButton({text}, {idx})")
                corner = self._cornerRadiusForIndex(idx, total)
                print(f" [button_group.py] BaseButtonGroup._setupLayout(): -> {corner} = self._cornerRadiusForIndex({idx}, {total})")
                button.setProperty("position", corner)
                print(f" [button_group.py] BaseButtonGroup._setupLayout(): -> {[bytes(name).decode() for name in button.dynamicPropertyNames()]}")
                layout.addWidget(button)
        return layout
    
    def _createButton(self, text, btn_id: Union[int, tuple]):
        btn = self.buttonClass(text=text)
        self.addButton(btn, btn_id)
        btn.clicked.connect(partial(self._onButtonClicked, btn_id))
        self._buttons.append(btn)
        return btn
    
    def _onButtonClicked(self, btn_id):
        if btn_id in self._disabledIds:
            return
        self.buttonClicked.emit(self._convertIdForEmit(btn_id))

    def _convertIdForEmit(self, btn_id):
        if self.useFlatId:
            return self._coord_to_flat_id(btn_id) if isinstance(btn_id, tuple) else btn_id
        else:
            return self._flat_id_to_coord(btn_id) if isinstance(btn_id, int) else btn_id

    def _coord_to_flat_id(self, coord):
        row, col = coord
        return row * self._cols + col

    def _flat_id_to_coord(self, flat_id):
        return (flat_id // self._cols, flat_id % self._cols)

    def setHorizontalSpacing(self, value: int=1):
        self._horizontalSpacing = value

    def setVerticalSpacing(self, value: int=1):
        self._verticalSpacing = value

    def addButton(self, button: QPushButton, btn_id: Union[int, tuple]):
        if btn_id is None:
            btn_id = self._nextId
            self._nextId += 1
        self._buttonIdMap[button] = btn_id
        self._idButtonMap[btn_id] = button

    def setId(self, button: QPushButton, btn_id: Union[int, tuple]):
        old_id = self._buttonIdMap.get(button)
        if old_id is not None:
            del self._idButtonMap[old_id]
        self._buttonIdMap[button] = btn_id
        self._idButtonMap[btn_id] = button

    def id(self, button: QPushButton):
        return self._buttonIdMap.get(button, -1)

    def button(self, btn_id: Union[int, tuple]):
        return self._idButtonMap.get(btn_id, None)

    def buttons(self):
        return self._buttons

    def disableButton(self, btn_id: Union[int, tuple]):
        btn = self.button(btn_id)
        if btn:
            btn.setEnabled(False)
            self._disabledIds.add(btn_id)

    def enableButton(self, btn_id: Union[int, tuple]):
        btn = self.button(btn_id)
        if btn:
            btn.setEnabled(True)
            self._disabledIds.discard(btn_id)

    def setDisabledIds(self, ids: List[Union[int, tuple]]):
        for btn_id in ids:
            self.disableButton(btn_id)

    def setButtonSize(self, width: Optional[int] = None, height: Optional[int] = None):
        for btn in self._buttons:
            if width is not None:
                btn.setFixedWidth(width)
            if height is not None:
                btn.setFixedHeight(height)

    def refreshButtonStyle(self):
        for btn in self._buttons:
            if hasattr(btn, "refreshStyle"):
                btn.refreshStyle()
            else:
                btn.style().unpolish(btn)
                btn.style().polish(btn)
                btn.update()
    
class PushButtonGroup(BaseButtonGroup):
    def __init__(
        self,
        labels: List[Union[str, List[str]]],
        parent: Optional[QWidget] = None,
        useFlatId: bool = False,
    ):
        super().__init__(
            labels=labels,
            parent=parent,
            buttonClass=PushButton,
            useFlatId=useFlatId,
        )

class SegmentedButtonGroup(BaseButtonGroup):
    def __init__(
        self,
        labels: List[Union[str, List[str]]],
        parent=None,
        useFlatId: bool = False,
        defaultCheckedId: Optional[Union[int, tuple]] = None,
        **kwargs,
    ):
        super().__init__(
            labels=labels,
            parent=parent,
            buttonClass=ToggleButton,
            useFlatId=useFlatId,
            **kwargs,
        )

        if defaultCheckedId is None:
            defaultCheckedId = 0 if useFlatId else (0, 0)

        self._currentCheckedId = defaultCheckedId
        self._setChecked(defaultCheckedId, True)

        self.buttonClicked.connect(self._on_button_clicked)

    def _setChecked(self, btn_id: Union[int, tuple], checked: bool):
        btn = self.button(btn_id)
        if btn is not None:
            btn.setChecked(checked)

    def checkedButtonId(self):
        return self._currentCheckedId
    
    def setDefaultDisabledIds(self, disabledIds: Union[int, Tuple[int, int], List[int], List[Tuple[int, int]]]):
        if not isinstance(disabledIds, list):
            disabledIds = [disabledIds]

        for btn_id in disabledIds:
            self.disableButton(btn_id)

    @pyqtSlot(object)
    def _on_button_clicked(self, btn_id):
        if btn_id == self._currentCheckedId:
            self._setChecked(btn_id, True)
            return

        if self._currentCheckedId is not None:
            self._setChecked(self._currentCheckedId, False)

        self._setChecked(btn_id, True)
        self._currentCheckedId = btn_id
