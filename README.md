# Gesture2Macro

Gesture2Macro es una aplicaci\u00f3n que permite ejecutar macros en Windows mediante gestos de mano detectados por la webcam. Todo el procesamiento se realiza de forma local sin enviar ning\u00fan dato al exterior.

El proyecto est\u00e1 dise\u00f1ado para ser modular y f\u00e1cil de extender. Incluye detecci\u00f3n de mano con MediaPipe, ejecuci\u00f3n de macros con `pyautogui` y una interfaz b\u00e1sica basada en PySide6.

## Requisitos
- Python 3.11
- Las dependencias listadas en `requirements.txt`

## Uso
Instala las dependencias y ejecuta:
```bash
python -m gesture2macro
```
Esto lanzar\u00e1 la captura de video y aplicar\u00e1 las reglas definidas en `rules.yaml`.
