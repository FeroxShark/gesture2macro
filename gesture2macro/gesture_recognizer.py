"""Reconocimiento b\u00e1sico de gestos con MediaPipe."""
from __future__ import annotations
try:
    import mediapipe as mp  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    mp = None
import numpy as np
from typing import Optional


class GestureRecognizer:
    def __init__(
        self,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
        required_frames: int = 1,
    ) -> None:
        if mp is None:
            self.hands = None
        else:
            self.hands = mp.solutions.hands.Hands(
                max_num_hands=2,
                min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence,
            )

        self.required_frames = max(1, required_frames)
        self._last_gesture: Optional[str] = None
        self._stable_count = 0
        self.last_results = None

    def recognize(self, frame: np.ndarray) -> Optional[str]:
        if self.hands is None:
            return None

        results = self.hands.process(frame)
        self.last_results = results
        if not results.multi_hand_landmarks:
            gesture = None
        else:
            hand = results.multi_hand_landmarks[0]
            finger_states = self._fingers_extended(hand)
            if sum(finger_states) == 0:
                gesture = "PU\u00d1O"
            elif sum(finger_states) == 5:
                gesture = "PALMA"
            elif finger_states[0] and not any(finger_states[1:]):
                gesture = "PULGAR_ARRIBA"
            else:
                gesture = None

        return self._apply_stability(gesture)

    def _apply_stability(self, gesture: Optional[str]) -> Optional[str]:
        """Return gesture only if stable across required_frames."""
        if gesture is None:
            self._stable_count = 0
            self._last_gesture = None
            return None

        if gesture == self._last_gesture:
            self._stable_count += 1
        else:
            self._last_gesture = gesture
            self._stable_count = 1

        if self._stable_count >= self.required_frames:
            return gesture
        return None

    @staticmethod
    def _fingers_extended(hand_landmarks) -> list[bool]:
        tips = [4, 8, 12, 16, 20]
        mcp = [2, 5, 9, 13, 17]
        extended = []
        for tip, base in zip(tips, mcp):
            extended.append(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base].y)
        return extended
