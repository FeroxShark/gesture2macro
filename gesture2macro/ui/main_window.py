"""Ventana principal que muestra la c\u00e1mara y las reglas."""
from __future__ import annotations

import time
from typing import Dict

from PySide6 import QtCore, QtGui, QtWidgets

from ..camera import Camera
from ..gesture_recognizer import GestureRecognizer
from ..macro_manager import execute_macro
from ..rules import Rule, load_rules
from ..utils.image_tools import to_rgb
from .macro_editor import MacroEditor


class MainWindow(QtWidgets.QMainWindow):
    """Interfaz gr\u00e1fica principal."""

    def __init__(self, config: dict, rules: list[Rule]):
        super().__init__()
        self.config = config
        self.rules = rules
        self.last_exec: Dict[str, float] = {}

        self.setWindowTitle(config.get("window_title", "Gesture2Macro"))

        self.camera = Camera(config.get("camera_index", 0))
        self.recognizer = GestureRecognizer()

        self._create_ui()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    # ------------------------------------------------------------------ UI ----
    def _create_ui(self) -> None:
        self.video_label = QtWidgets.QLabel()
        self.video_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.video_label)

        # Menu for editing rules
        menu = self.menuBar().addMenu("Archivo")
        edit_rules = menu.addAction("Editar reglas...")
        edit_rules.triggered.connect(self.edit_rules)

    # --------------------------------------------------------------- Actions ----
    def edit_rules(self) -> None:
        dialog = MacroEditor("rules.yaml", self)
        if dialog.exec():
            self.rules = load_rules("rules.yaml")
            self.last_exec.clear()

    def update_frame(self) -> None:
        ret, frame = self.camera.read()
        if not ret:
            return

        rgb = to_rgb(frame)
        gesture = self.recognizer.recognize(rgb)
        if gesture:
            self._handle_gesture(gesture)

        h, w, ch = frame.shape
        img = QtGui.QImage(frame.data, w, h, w * ch, QtGui.QImage.Format_BGR888)
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(img))

    def _handle_gesture(self, gesture: str) -> None:
        now = time.time()
        for rule in self.rules:
            if rule.gesture == gesture:
                last = self.last_exec.get(rule.name, 0)
                if now - last >= rule.cooldown_ms / 1000:
                    execute_macro(rule.macro.type, rule.macro.params)
                    self.statusBar().showMessage(f"{rule.name} ({gesture})")
                    self.last_exec[rule.name] = now

    # ------------------------------------------------------------- Qt Events ----
    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # type: ignore[override]
        self.timer.stop()
        self.camera.release()
        super().closeEvent(event)
