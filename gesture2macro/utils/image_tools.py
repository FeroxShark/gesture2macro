"""Herramientas para procesamiento de imagen."""
import cv2
import numpy as np


def to_rgb(frame: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
