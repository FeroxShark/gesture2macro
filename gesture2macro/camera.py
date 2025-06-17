"""M\u00f3dulo de captura de video usando OpenCV."""
import cv2


class Camera:
    def __init__(self, index: int = 0):
        self.cap = cv2.VideoCapture(index)

    def read(self):
        ret, frame = self.cap.read()
        return ret, frame

    def release(self):
        self.cap.release()
