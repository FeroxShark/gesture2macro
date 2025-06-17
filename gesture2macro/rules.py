"""Lectura de reglas de gestos a macros."""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List
import yaml


@dataclass
class Macro:
    type: str
    params: Dict[str, Any]


@dataclass
class Rule:
    name: str
    gesture: str
    macro: Macro
    cooldown_ms: int = 0


def load_rules(path: str | Path) -> List[Rule]:
    """Carga el archivo YAML de reglas."""
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or []
    rules: List[Rule] = []
    for item in data:
        macro = Macro(
            type=item["macro"]["type"],
            params={k: v for k, v in item["macro"].items() if k != "type"},
        )
        rules.append(
            Rule(
                name=item["name"],
                gesture=item["gesture"],
                macro=macro,
                cooldown_ms=item.get("cooldown_ms", 0),
            )
        )
    return rules
