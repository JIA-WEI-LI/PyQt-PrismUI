from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class PushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        parent = kwargs.get("parent", None)
        text = None
        icon = None

        # 解析 args
        if args:
            if isinstance(args[0], QWidget):
                parent = args[0]
            elif isinstance(args[0], str):
                text = args[0]
                if len(args) > 1:
                    if isinstance(args[1], (QIcon, str)):
                        icon = args[1]
                    elif isinstance(args[1], QWidget):
                        parent = args[1]
                if len(args) > 2:
                    parent = args[2]
            elif isinstance(args[0], (QIcon, str)):
                icon = args[0]
                if len(args) > 1 and isinstance(args[1], str):
                    text = args[1]
                if len(args) > 2 and isinstance(args[2], QWidget):
                    parent = args[2]

        super().__init__(parent)

        self.setIconSize(QSize(24, 24))  # 改大點

        if text:
            self.setText(text)
        if icon:
            self.setIcon(icon)
        else:
            self.setIcon(QIcon())

        self._initStyle()

    def setIcon(self, icon):
        if isinstance(icon, str):
            icon = QIcon(icon)
        super().setIcon(icon)

    def _initStyle(self):
        self.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 5px;
                color: white;
                padding: 5px 12px;
                outline: none;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.08);
            }
            QPushButton:pressed {
                color: rgba(255, 255, 255, 0.78);
                background: rgba(255, 255, 255, 0.03);
            }
            QPushButton:disabled {
                color: rgba(255, 255, 255, 0.36);
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
        """)
