"""Widget para listar gestos."""
from PySide6 import QtWidgets


class GestureList(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
