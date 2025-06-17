"""Reconocimiento b\u00e1sico de gestos con MediaPipe."""
from __future__ import annotations
import mediapipe as mp
import numpy as np
from typing import Optional


class GestureRecognizer:
    def __init__(self, min_detection_confidence: float = 0.5, min_tracking_confidence: float = 0.5):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def recognize(self, frame: np.ndarray) -> Optional[str]:
        results = self.hands.process(frame)
        if not results.multi_hand_landmarks:
            return None
        hand = results.multi_hand_landmarks[0]
        finger_states = self._fingers_extended(hand)
        if sum(finger_states) == 0:
            return "PU\u00d1O"
        if sum(finger_states) == 5:
            return "PALMA"
        if finger_states[0] and not any(finger_states[1:]):
            return "PULGAR_ARRIBA"
        return None

    @staticmethod
    def _fingers_extended(hand_landmarks) -> list[bool]:
        tips = [4, 8, 12, 16, 20]
        mcp = [2, 5, 9, 13, 17]
        extended = []
        for tip, base in zip(tips, mcp):
            extended.append(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base].y)
        return extended
