"""Entry point for both package and frozen execution."""

# When running the module as a script (e.g. the PyInstaller generated
# executable) ``__package__`` is ``None`` and relative imports fail.  Using an
# absolute import works in both scenarios: ``python -m gesture2macro`` and the
# bundled executable.
from gesture2macro.main import main

if __name__ == "__main__":
    main()
