from __future__ import annotations

from pathlib import Path
from typing import List

from PySide6 import QtWidgets
import yaml

from ..rules import Rule, Macro, load_rules, save_rules


class RuleEditorDialog(QtWidgets.QDialog):
    """Dialogo simple para editar una regla."""

    def __init__(self, rule: Rule | None = None, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Editar regla" if rule else "Nueva regla")
        self._rule = rule

        layout = QtWidgets.QFormLayout(self)

        self.name_edit = QtWidgets.QLineEdit(self)
        self.gesture_edit = QtWidgets.QLineEdit(self)
        self.macro_combo = QtWidgets.QComboBox(self)
        self.macro_combo.addItems(
            [
                "key_combo",
                "scroll",
                "click",
                "open_app",
                "write_text",
                "move_cursor",
            ]
        )
        self.params_edit = QtWidgets.QPlainTextEdit(self)
        self.cooldown_spin = QtWidgets.QSpinBox(self)
        self.cooldown_spin.setRange(0, 10000)

        layout.addRow("Nombre", self.name_edit)
        layout.addRow("Gesto", self.gesture_edit)
        layout.addRow("Tipo de macro", self.macro_combo)
        layout.addRow("Par\xC3\xA1metros YAML", self.params_edit)
        layout.addRow("Cooldown ms", self.cooldown_spin)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            parent=self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        if rule:
            self.name_edit.setText(rule.name)
            self.gesture_edit.setText(rule.gesture)
            self.macro_combo.setCurrentText(rule.macro.type)
            self.params_edit.setPlainText(
                yaml.safe_dump(rule.macro.params, allow_unicode=True, sort_keys=False)
            )
            self.cooldown_spin.setValue(rule.cooldown_ms)

    def get_rule(self) -> Rule:
        params = yaml.safe_load(self.params_edit.toPlainText()) or {}
        return Rule(
            name=self.name_edit.text(),
            gesture=self.gesture_edit.text(),
            macro=Macro(type=self.macro_combo.currentText(), params=params),
            cooldown_ms=self.cooldown_spin.value(),
        )


class RuleManager(QtWidgets.QDialog):
    """Ventana para administrar reglas en forma de tabla."""

    def __init__(self, path: str | Path, parent=None) -> None:
        super().__init__(parent)
        self.path = Path(path)
        self.rules: List[Rule] = load_rules(self.path)
        self.setWindowTitle("Reglas de gestos")

        layout = QtWidgets.QVBoxLayout(self)

        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Nombre",
            "Gesto",
            "Macro",
            "Cooldown",
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

        btns = QtWidgets.QHBoxLayout()
        add_btn = QtWidgets.QPushButton("Agregar", self)
        edit_btn = QtWidgets.QPushButton("Editar", self)
        del_btn = QtWidgets.QPushButton("Eliminar", self)
        btns.addWidget(add_btn)
        btns.addWidget(edit_btn)
        btns.addWidget(del_btn)
        layout.addLayout(btns)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel,
            parent=self,
        )
        layout.addWidget(buttons)

        add_btn.clicked.connect(self.add_rule)
        edit_btn.clicked.connect(self.edit_rule)
        del_btn.clicked.connect(self.del_rule)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)

        self.refresh()

    # ----------------------------------------------------------------- actions
    def refresh(self) -> None:
        self.table.setRowCount(len(self.rules))
        for row, rule in enumerate(self.rules):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(rule.name))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(rule.gesture))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(rule.macro.type))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(rule.cooldown_ms)))
        self.table.resizeColumnsToContents()

    def _selected_row(self) -> int:
        items = self.table.selectionModel().selectedRows()
        return items[0].row() if items else -1

    def add_rule(self) -> None:
        dialog = RuleEditorDialog(parent=self)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            self.rules.append(dialog.get_rule())
            self.refresh()

    def edit_rule(self) -> None:
        idx = self._selected_row()
        if idx < 0:
            return
        dialog = RuleEditorDialog(self.rules[idx], parent=self)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            self.rules[idx] = dialog.get_rule()
            self.refresh()

    def del_rule(self) -> None:
        idx = self._selected_row()
        if idx >= 0:
            self.rules.pop(idx)
            self.refresh()

    def save(self) -> None:
        save_rules(self.path, self.rules)
        self.accept()
