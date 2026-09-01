@echo off
REM ============================================
REM Farsi Game Manager - Windows Installer
REM ============================================

chcp 65001 >nul
setlocal enabledelayedexpansion

cls
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║     🎮 Farsi Game Manager - Windows Installer       ║
echo ║              فارسی‌سازی بازی                        ║
echo ╚══════════════════════════════════════════════════════╝
echo.

REM بررسی اینکه برنامه روی Windows است
if not "%OS%"=="Windows_NT" (
    echo ❌ خطا: این برنامه فقط برای Windows است!
    pause
    exit /b 1
)

REM تنظیم متغیرها
set "APP_NAME=Farsi-Game-Manager"
set "APP_VERSION=1.0.0"
set "EXE_SOURCE=dist\%APP_NAME%.exe"
set "INSTALL_DIR=%ProgramFiles%\Farsi-Game-Manager"

echo.
echo [1/3] بررسی فایل‌های نصب...
if not exist "%EXE_SOURCE%" (
    echo ❌ خطا: فایل %EXE_SOURCE% یافت نشد!
    echo 💡 لطفاً ابتدا برنامه را ساخته یا دانلود کنید
    pause
    exit /b 1
)

echo ✅ فایل یافت شد

echo.
echo [2/3] نصب برنامه...
mkdir "%INSTALL_DIR%" 2>nul

REM کپی فایل
copy /Y "%EXE_SOURCE%" "%INSTALL_DIR%\%APP_NAME%.exe" >nul
if %ERRORLEVEL% neq 0 (
    echo ❌ خطا در کپی فایل
    pause
    exit /b 1
)

echo ✅ فایل نصب شد

echo.
echo [3/3] ایجاد Shortcuts...

REM ایجاد shortcut بر روی Desktop
powershell -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; " ^
    "$Shortcut = $WshShell.CreateShortcut('%UserProfile%\Desktop\Farsi-Game-Manager.lnk'); " ^
    "$Shortcut.TargetPath = '%INSTALL_DIR%\%APP_NAME%.exe'; " ^
    "$Shortcut.WorkingDirectory = '%INSTALL_DIR%'; " ^
    "$Shortcut.Save()"

REM ایجاد shortcut بر روی Start Menu
set "STARTUP=%AppData%\Microsoft\Windows\Start Menu\Programs"
powershell -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; " ^
    "$Shortcut = $WshShell.CreateShortcut('%STARTUP%\Farsi-Game-Manager.lnk'); " ^
    "$Shortcut.TargetPath = '%INSTALL_DIR%\%APP_NAME%.exe'; " ^
    "$Shortcut.WorkingDirectory = '%INSTALL_DIR%'; " ^
    "$Shortcut.Save()"

echo ✅ Shortcuts ایجاد شد

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║           ✅ نصب با موفقیت تکمیل شد!              ║
echo ╠══════════════════════════════════════════════════════╣
echo ║ 📁 مسیر نصب: %INSTALL_DIR%            ║
echo ║ 🖱️  Desktop Shortcut: فارسی-گیم-منیجر              ║
echo ║ 📌 Start Menu: Farsi-Game-Manager                   ║
echo ╚══════════════════════════════════════════════════════╝
echo.

echo آیا می‌خواهید برنامه را اکنون اجرا کنید؟
echo [Y/N]
set /P choice=
if /i "%choice%"=="Y" (
    start "" "%INSTALL_DIR%\%APP_NAME%.exe"
)

echo.
echo درود! برنامه نصب شد.
echo 🎮 از استفاده از Farsi Game Manager لذت ببرید!
echo.

pause
