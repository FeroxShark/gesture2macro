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

    dummy = Dummy()
    monkeypatch.setitem(sys.modules, "pyautogui", dummy)
    macro_manager.execute_macro("key_combo", {"sequence": ["ctrl+x"]})
    assert dummy.calls == [("hotkey", ("ctrl", "x"))]
