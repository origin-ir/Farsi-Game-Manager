@echo off
REM ============================================
REM Farsi Game Manager - Windows Uninstaller
REM ============================================

chcp 65001 >nul
setlocal enabledelayedexpansion

cls
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║     🎮 Farsi Game Manager - Uninstaller             ║
echo ╚══════════════════════════════════════════════════════╝
echo.

set "INSTALL_DIR=%ProgramFiles%\Farsi-Game-Manager"

echo آیا مطمئن هستید که می‌خواهید برنامه را حذف کنید؟
echo [Y/N]
set /P choice=

if /i not "%choice%"=="Y" (
    echo لغو شد
    exit /b 0
)

echo.
echo حذف برنامه...

REM حذف پوشه نصب
if exist "%INSTALL_DIR%" (
    rmdir /S /Q "%INSTALL_DIR%"
    echo ✅ پوشه نصب حذف شد
)

REM حذف Desktop Shortcut
if exist "%UserProfile%\Desktop\Farsi-Game-Manager.lnk" (
    del "%UserProfile%\Desktop\Farsi-Game-Manager.lnk"
    echo ✅ Desktop Shortcut حذف شد
)

REM حذف Start Menu Shortcut
set "STARTUP=%AppData%\Microsoft\Windows\Start Menu\Programs"
if exist "%STARTUP%\Farsi-Game-Manager.lnk" (
    del "%STARTUP%\Farsi-Game-Manager.lnk"
    echo ✅ Start Menu Shortcut حذف شد
)

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║           ✅ حذف با موفقیت تکمیل شد!              ║
echo ║                                                      ║
echo ║  با تشکر از استفاده از Farsi Game Manager! 🙏     ║
echo ╚══════════════════════════════════════════════════════╝
echo.

pause
