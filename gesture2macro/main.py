"""Punto de entrada de la aplicaci\u00f3n."""
from __future__ import annotations

from PySide6 import QtWidgets

from .config import load_config
from .rules import load_rules
from .ui.main_window import MainWindow
from .utils.logger import get_logger


def main() -> None:
    config = load_config()
    rules = load_rules("rules.yaml")
    logger = get_logger(__name__)

    logger.info("Iniciando Gesture2Macro en modo gr\u00e1fico")

    app = QtWidgets.QApplication([])
    window = MainWindow(config, rules)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
