from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class WidgetTemplate(QWidget):
    actionRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loading = False
        self.error_message = ""
        self._build_ui()
        self.render_state()

    def _build_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(8)

        self.title_label = QLabel("Widget title")
        self.state_label = QLabel("")
        self.action_btn = QPushButton("Run action")
        self.action_btn.clicked.connect(self.actionRequested.emit)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.state_label)
        self.layout.addWidget(self.action_btn)
        self.layout.addStretch(1)

    def set_loading(self, value):
        self.loading = bool(value)
        self.render_state()

    def set_error(self, message):
        self.error_message = message or ""
        self.render_state()

    def render_state(self):
        if self.loading:
            self.state_label.setText("Loading...")
            self.action_btn.setEnabled(False)
            return
        if self.error_message:
            self.state_label.setText(f"Error: {self.error_message}")
            self.action_btn.setEnabled(True)
            return
        self.state_label.setText("Ready")
        self.action_btn.setEnabled(True)
