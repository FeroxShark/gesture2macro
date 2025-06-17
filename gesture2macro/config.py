"""Carga de configuraci\u00f3n global."""
from pathlib import Path
import yaml

DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "config.yaml"


def load_config(path: str | Path | None = None) -> dict:
    """Carga el archivo de configuraci\u00f3n YAML."""
    config_path = Path(path) if path else DEFAULT_CONFIG
    with open(config_path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}
