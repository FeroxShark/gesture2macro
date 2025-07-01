@echo off
REM Empaqueta Gesture2Macro como ejecutable usando PyInstaller
python -m pip install -r requirements.txt
pyinstaller --noconsole --onefile -n Gesture2Macro gesture2macro\__main__.py
echo.
echo El ejecutable se encuentra en dist\Gesture2Macro.exe
pause

