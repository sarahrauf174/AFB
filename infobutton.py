from PySide6.QtWidgets import QPushButton

class InfoButton(QPushButton):
    def __init__(self, tooltip_text: str, parent=None):
        super().__init__("i", parent)
        self.setFixedSize(16, 16)
        self.setToolTip(tooltip_text)
        self.setStyleSheet("""
            border-radius: 8px;
            border: 1px solid white;
            background-color: #424952;
        """)
        