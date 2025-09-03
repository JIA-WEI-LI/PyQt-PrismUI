from PyQt5.QtCore import QTimer, QEvent

from .tool_tip import ToolTip, TooltipWithTitle

class BaseMixin:
    def __init__(self):
        self._icon_cache = {}
        self._current_icon_color = None
        self._icon_source = None

    def init_tooltip(self, 
                     delay: int=1000):
        self._tooltip_delay = delay
        self._tooltip_timer = QTimer(self)
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self._tooltip_timer.timeout.connect(self._show_tooltip)

    def setTooltip(self, text: str):
        if not hasattr(self, "tooltip") or self.tooltip is None:
            self.tooltip = ToolTip(text, parent=None)
            self.init_tooltip()
        else:
            self.tooltip.setText(text)

    def setTooltipWithTitle(self, title: str, text: str):
        if not hasattr(self, "tooltip") or self.tooltip is None:
            self.tooltip = TooltipWithTitle(title, text, parent=None)
            self.init_tooltip()
        else:
            self.tooltip.setTitle(title)
            self.tooltip.setContent(text)

    def setToolTipDelay(self, delay_ms: int):
        self._tooltip_delay = delay_ms

    def eventFilter(self, obj, event):
        if obj is self:
            if event.type() == QEvent.Enter:
                self._tooltip_timer.start(self._tooltip_delay)
            elif event.type() == QEvent.Leave:
                self._tooltip_timer.stop()
                if hasattr(self, "tooltip") and self.tooltip:
                    self.tooltip.hide()

        parent_event_filter = getattr(super(), "eventFilter", None)
        if callable(parent_event_filter):
            return parent_event_filter(obj, event)
        return False

    def _show_tooltip(self):
        if hasattr(self, "tooltip") and self.tooltip:
            self.tooltip.adjustPos(self)
            self.tooltip.show()