"""Ventana principal que muestra la c\u00e1mara y las reglas."""
from __future__ import annotations

import time
from typing import Dict

from PySide6 import QtCore, QtGui, QtWidgets
try:
    import mediapipe as mp  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    mp = None

from ..camera import Camera
from ..gesture_recognizer import GestureRecognizer
from ..macro_manager import execute_macro
from ..rules import Rule, load_rules
from ..utils.image_tools import to_rgb
from .macro_editor import MacroEditor
from ..utils.logger import get_logger


class MainWindow(QtWidgets.QMainWindow):
    """Interfaz gr\u00e1fica principal."""

    def __init__(self, config: dict, rules: list[Rule]):
        super().__init__()
        self.config = config
        self.rules = rules
        self.last_exec: Dict[str, float] = {}

        self.setWindowTitle(config.get("window_title", "Gesture2Macro"))

        self.logger = get_logger(__name__)

        self.camera = Camera(config.get("camera_index", 0))
        self.recognizer = GestureRecognizer(required_frames=3)
        self.statusBar().showMessage("Modelo listo")

        self._create_ui()
        self._apply_dark_theme()

        self.logger.info("Ventana principal iniciada")

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def _apply_dark_theme(self) -> None:
        """Aplica un tema oscuro sencillo."""
        app = QtWidgets.QApplication.instance()
        if app is None:
            return
        app.setStyle("Fusion")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white)
        palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor(25, 25, 25))
        palette.setColor(QtGui.QPalette.ColorRole.Text, QtCore.Qt.GlobalColor.white)
        palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ColorRole.ButtonText, QtCore.Qt.GlobalColor.white)
        app.setPalette(palette)

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
            self.logger.error("No se pudo leer de la cámara")
            return

        rgb = to_rgb(frame)
        gesture = self.recognizer.recognize(rgb)
        if gesture:
            self.logger.debug("Gesto reconocido: %s", gesture)
            self._handle_gesture(gesture)
        else:
            self.statusBar().showMessage("Sin gesto")

        if mp and self.recognizer.last_results and self.recognizer.last_results.multi_hand_landmarks:
            for hand_landmarks in self.recognizer.last_results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS,
                )

        h, w, ch = frame.shape
        img = QtGui.QImage(frame.data, w, h, w * ch, QtGui.QImage.Format_BGR888)
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(img))

    def _handle_gesture(self, gesture: str) -> None:
        now = time.time()
        for rule in self.rules:
            if rule.gesture == gesture:
                last = self.last_exec.get(rule.name, 0)
                if now - last >= rule.cooldown_ms / 1000:
                    self.logger.info(
                        "Ejecutando macro %s por gesto %s", rule.name, gesture
                    )
                    execute_macro(rule.macro.type, rule.macro.params)
                    QtWidgets.QApplication.beep()
                    self.statusBar().showMessage(f"{rule.name} ({gesture})")
                    self.last_exec[rule.name] = now

    # ------------------------------------------------------------- Qt Events ----
    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # type: ignore[override]
        self.timer.stop()
        self.camera.release()
        super().closeEvent(event)
