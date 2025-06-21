"""M\u00f3dulo principal de Gesture2Macro."""

__version__ = "0.1.0"

__all__ = ["main"]


def main() -> None:
    """Ejecuci\u00f3n de la aplicaci\u00f3n gr\u00e1fica."""
    from .main import main as _main

    _main()
