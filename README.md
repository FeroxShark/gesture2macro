# Gesture2Macro

Gesture2Macro es una aplicaci\u00f3n que permite ejecutar macros en Windows mediante gestos de mano detectados por la webcam. Todo el procesamiento se realiza de forma local sin enviar ning\u00fan dato al exterior.

El proyecto est\u00e1 dise\u00f1ado para ser modular y f\u00e1cil de extender. Incluye detecci\u00f3n de mano con MediaPipe, ejecuci\u00f3n de macros con `pyautogui` y una interfaz b\u00e1sica basada en PySide6.

## Requisitos
- Python 3.11
- Las dependencias listadas en `requirements.txt` con sus versiones fijadas

## Uso
Instala las dependencias y ejecuta:
```bash
python -m gesture2macro
```
Esto lanzar\u00e1 la captura de video y aplicar\u00e1 las reglas definidas en `rules.yaml`.
Al guardar desde el editor integrado se crea autom\u00e1ticamente una copia `rules.yaml.bak`.

### Novedades

- Tema oscuro integrado.
- Vista con landmarks superpuestos sobre la imagen de la cámara.
- Nuevos tipos de macro: `open_app`, `write_text` y `move_cursor`.
- Sonido de confirmación al ejecutar una acción.
- Ventana gráfica para gestionar reglas sin editar YAML manualmente.


## Ejecutable para Windows

Para generar un instalador listo para usar ejecuta el script `build_windows.bat`.
Este archivo instalar\u00e1 las dependencias necesarias y crear\u00e1 un
`Gesture2Macro.exe` dentro de la carpeta `dist` mediante PyInstaller.

```cmd
build_windows.bat
```

Una vez finalizado el proceso abre `dist\Gesture2Macro.exe` para utilizar la
aplicaci\u00f3n sin requerir Python instalado.
