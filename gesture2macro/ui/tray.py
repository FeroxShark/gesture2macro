"""Icono de bandeja del sistema."""
from PySide6 import QtWidgets, QtGui


class SystemTray(QtWidgets.QSystemTrayIcon):
    """Sencillo icono de bandeja con opciones b\u00e1sicas."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        icon = QtGui.QIcon.fromTheme("applications-system")
        if icon.isNull():
            icon = QtGui.QIcon()
        super().__init__(icon, parent)
        self._parent = parent

        menu = QtWidgets.QMenu(parent)
        show_action = menu.addAction("Mostrar")
        show_action.triggered.connect(self._show_parent)
        exit_action = menu.addAction("Salir")
        if parent and hasattr(parent, "force_quit"):
            exit_action.triggered.connect(parent.force_quit)
        else:
            exit_action.triggered.connect(QtWidgets.QApplication.quit)
        self.setContextMenu(menu)

    # ------------------------------------------------------------------ slots
    def _show_parent(self) -> None:
        if self._parent:
            self._parent.showNormal()
            self._parent.activateWindow()
