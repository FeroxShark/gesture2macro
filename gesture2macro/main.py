"""Punto de entrada de la aplicaci\u00f3n."""
from __future__ import annotations
import cv2
from .camera import Camera
from .gesture_recognizer import GestureRecognizer
from .rules import load_rules
from .macro_manager import execute_macro
from .config import load_config
from .utils.image_tools import to_rgb
from .utils.logger import get_logger


def main() -> None:
    config = load_config()
    rules = load_rules("rules.yaml")
    logger = get_logger(__name__)
    cam = Camera(config.get("camera_index", 0))
    recognizer = GestureRecognizer()
    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                break
            rgb = to_rgb(frame)
            gesture = recognizer.recognize(rgb)
            if gesture:
                for rule in rules:
                    if rule.gesture == gesture:
                        logger.info("Ejecutando macro %s", rule.name)
                        execute_macro(rule.macro.type, rule.macro.params)
            cv2.imshow(config.get("window_title", "Gesture2Macro"), frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
