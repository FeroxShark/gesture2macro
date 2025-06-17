"""Ventana principal b\u00e1sica."""
from __future__ import annotations
from PySide6 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gesture2Macro")
        label = QtWidgets.QLabel("Gesture2Macro en ejecuci\u00f3n")
        label.setAlignment(QtWidgets.Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)
