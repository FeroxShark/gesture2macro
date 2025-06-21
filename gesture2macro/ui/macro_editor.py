"""Editor de reglas en formato YAML."""
from __future__ import annotations

from pathlib import Path
from PySide6 import QtWidgets


class MacroEditor(QtWidgets.QDialog):
    """Peque\u00f1o editor de texto para las reglas de gestos."""

    def __init__(self, rules_path: str | Path, parent=None) -> None:
        super().__init__(parent)
        self.rules_path = Path(rules_path)
        self.setWindowTitle("Editar reglas")

        layout = QtWidgets.QVBoxLayout(self)
        self.text = QtWidgets.QPlainTextEdit(self)
        layout.addWidget(self.text)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel,
            parent=self,
        )
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.load()

    def load(self) -> None:
        """Carga el archivo YAML en el editor."""
        if self.rules_path.exists():
            self.text.setPlainText(self.rules_path.read_text(encoding="utf-8"))

    def save(self) -> None:
        """Guarda el contenido del editor en el archivo."""
        self.rules_path.write_text(self.text.toPlainText(), encoding="utf-8")
        self.accept()
