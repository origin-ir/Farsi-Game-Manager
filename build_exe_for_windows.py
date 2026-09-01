#!/usr/bin/env python3
"""
Build script for creating Windows EXE file
This script should be run on Windows or using Wine/Docker

نسخه از کد برای ساختن EXE برای ویندوز
"""

import subprocess
import sys
import os
from pathlib import Path

def build_exe():
    """ساختن فایل EXE برای Windows"""
    
    print("=" * 70)
    print("🎮 Farsi Game Manager - Windows EXE Builder")
    print("=" * 70)
    print()
    
    # بررسی نصب بودن dependencies
    print("📦 بررسی Dependencies...")
    try:
        import PyQt6
        import requests
        import pyinstaller
        print("✅ تمام Dependencies نصب شده اند")
    except ImportError as e:
        print(f"❌ خطا: {e}")
        print("🔧 نصب لازم dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    print()
    print("🔨 ساختن EXE...")
    print("-" * 70)
    
    # دستور ساخت
    pyinstaller_args = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "Farsi-Game-Manager",
        "--icon=icon.ico",
        "--add-data=icon.ico:.",
        "--add-data=splash.png:.",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=requests",
        "--clean",
        "--distpath=dist",
        "--buildpath=build",
        "main.py"
    ]
    
    # در صورت اجرا روی Windows
    if sys.platform.startswith('win'):
        result = subprocess.run(pyinstaller_args)
    else:
        print("⚠️ این برنامه برای ساختن EXE واقعی باید روی Windows اجرا شود!")
        print("🐧 اگر روی Linux هستید، می‌توانید Docker استفاده کنید")
        print("💡 دستور: docker run -v $(pwd):/src cdrx/pyinstaller-windows ./build_exe_for_windows.py")
        return False
    
    print("-" * 70)
    print()
    
    if result.returncode == 0:
        exe_path = Path("dist") / "Farsi-Game-Manager.exe"
        if exe_path.exists():
            print("✅ EXE با موفقیت ساخته شد!")
            print(f"📁 مسیر: {exe_path}")
            print(f"📊 اندازه: {exe_path.stat().st_size / (1024*1024):.2f} MB")
            print()
            print("🎉 برنامه آماده برای استفاده است!")
            return True
        else:
            print("❌ خطا: فایل EXE ایجاد نشد")
            return False
    else:
        print("❌ خطا در ساخت EXE")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
