"""Ejecuci\u00f3n de macros mediante pyautogui."""
from __future__ import annotations
from typing import Any, Dict


def execute_macro(macro_type: str, params: Dict[str, Any]) -> None:
    import pyautogui  # Import din\u00e1mico para evitar problemas en entornos sin GUI

    if macro_type == "key_combo":
        for combo in params.get("sequence", []):
            keys = combo.split("+")
            pyautogui.hotkey(*keys)
    elif macro_type == "scroll":
        direction = params.get("direction", "down")
        amount = params.get("amount", 1)
        scroll_amt = -amount if direction == "down" else amount
        pyautogui.scroll(scroll_amt)
    elif macro_type == "click":
        button = params.get("button", "left")
        pyautogui.click(button=button)
