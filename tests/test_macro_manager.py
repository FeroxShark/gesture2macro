import sys
from gesture2macro import macro_manager


def test_execute_macro(monkeypatch):
    class Dummy:
        def __init__(self):
            self.calls = []

        def hotkey(self, *args):
            self.calls.append(("hotkey", args))

        def scroll(self, amount):
            self.calls.append(("scroll", amount))

        def click(self, button="left"):
            self.calls.append(("click", button))

        def write(self, text):
            self.calls.append(("write", text))

        def moveTo(self, x, y, duration=0):
            self.calls.append(("moveTo", (x, y, duration)))

    class DummySubprocess:
        def __init__(self, log):
            self.log = log

        def Popen(self, args):
            self.log.append(("Popen", args))

    dummy = Dummy()
    subproc = DummySubprocess(dummy.calls)
    monkeypatch.setitem(sys.modules, "pyautogui", dummy)
    monkeypatch.setitem(sys.modules, "subprocess", subproc)
    macro_manager.execute_macro("key_combo", {"sequence": ["ctrl+x"]})
    assert dummy.calls == [("hotkey", ("ctrl", "x"))]
    dummy.calls.clear()

    macro_manager.execute_macro("open_app", {"path": "calc.exe"})
    assert dummy.calls == [("Popen", ["calc.exe"])]
    dummy.calls.clear()

    macro_manager.execute_macro("write_text", {"text": "hola"})
    assert dummy.calls == [("write", "hola")]
    dummy.calls.clear()

    macro_manager.execute_macro("move_cursor", {"x": 10, "y": 20, "duration": 1})
    assert dummy.calls == [("moveTo", (10, 20, 1))]
