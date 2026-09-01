@echo off
echo ============================================
echo Farsi Game Manager - Build Script
echo ============================================
echo.

echo [1/3] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2/3] Building executable...
pyinstaller --onefile ^
    --windowed ^
    --name "Farsi-Game-Manager" ^
    --icon=icon.ico ^
    --add-data "icon.ico:." ^
    --splash splash.png ^
    main.py

echo.
echo [3/3] Build complete!
echo Executable location: dist\Farsi-Game-Manager.exe
echo.
pause
