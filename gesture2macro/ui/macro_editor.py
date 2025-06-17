"""Editor de macros sencillo."""
from PySide6 import QtWidgets


class MacroEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Editor de macros"))
