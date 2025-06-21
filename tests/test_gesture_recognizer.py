from gesture2macro.gesture_recognizer import GestureRecognizer


def test_create_recognizer():
    gr = GestureRecognizer()
    assert gr is not None


def test_stable_recognition():
    gr = GestureRecognizer(required_frames=2)
    # first appearance should not trigger
    assert gr._apply_stability("PALMA") is None
    # second consecutive appearance should return the gesture
    assert gr._apply_stability("PALMA") == "PALMA"
