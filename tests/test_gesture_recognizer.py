from gesture2macro.gesture_recognizer import GestureRecognizer


def test_create_recognizer():
    gr = GestureRecognizer()
    assert gr is not None
