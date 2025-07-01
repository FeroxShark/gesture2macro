@echo off
REM Construye un ejecutable standalone para Windows usando PyInstaller
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --noconfirm --onefile --name Gesture2Macro gesture2macro\__main__.py

ECHO Instalacion completa. El ejecutable se encuentra en dist\Gesture2Macro.exe
pause
