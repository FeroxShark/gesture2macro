"""Icono de bandeja del sistema."""
from PySide6 import QtWidgets, QtGui


class SystemTray(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        icon = QtGui.QIcon()
        super().__init__(icon, parent)
        menu = QtWidgets.QMenu()
        exit_action = menu.addAction("Salir")
        exit_action.triggered.connect(QtWidgets.QApplication.quit)
        self.setContextMenu(menu)
