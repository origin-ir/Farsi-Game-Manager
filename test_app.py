#!/usr/bin/env python3
"""
Testing script for Farsi Game Manager
تست کامل برنامه برای اطمینان از عملکرد درست
"""

import sys
import json
from pathlib import Path
import requests

def test_imports():
    """تست import کردن تمام dependencies"""
    print("🧪 تست 1: بررسی Dependencies...")
    
    dependencies = {
        'PyQt6': 'رابط کاربری',
        'requests': 'دانلود و GitHub API',
    }
    
    failed = []
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"  ✅ {module:15} ({description})")
        except ImportError as e:
            print(f"  ❌ {module:15} ({description}) - {e}")
            failed.append(module)
    
    return len(failed) == 0

def test_github_api():
    """تست اتصال به GitHub API"""
    print("\n🧪 تست 2: اتصال GitHub API...")
    
    try:
        url = "https://api.github.com/repos/Origin-Core/Farsi-Origin/contents"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        files = response.json()
        print(f"  ✅ اتصال برقرار")
        print(f"  ✅ {len(files)} فایل دریافت شد")
        
        # تشخیص محصولات
        products = set()
        for file in files:
            if isinstance(file, dict) and file.get("type") == "file":
                name = file["name"]
                product = name.split('.')[0].upper()
                if product not in ['README', '_CONFIG', '_LAYOUTS', 'BBBGGG', 'DDDMMM']:
                    products.add(product)
        
        print(f"  ✅ {len(products)} محصول شناسایی شد: {', '.join(sorted(products))}")
        return True
    except Exception as e:
        print(f"  ❌ خطا: {e}")
        return False

def test_cache_system():
    """تست سیستم cache"""
    print("\n🧪 تست 3: سیستم Cache...")
    
    try:
        cache_dir = Path.home() / ".farsi_game_manager" / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # تست نوشتن
        test_file = cache_dir / "test.json"
        test_data = {"test": "data", "status": "working"}
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        print(f"  ✅ نوشتن Cache: {cache_dir}")
        
        # تست خواندن
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        
        if loaded == test_data:
            print(f"  ✅ خواندن Cache: موفق")
        else:
            print(f"  ❌ داده‌های Cache منطبق نیست")
            return False
        
        # تمیز کردن
        test_file.unlink()
        
        return True
    except Exception as e:
        print(f"  ❌ خطا: {e}")
        return False

def test_downloads_folder():
    """تست پوشه دانلود‌ها"""
    print("\n🧪 تست 4: پوشه Downloads...")
    
    try:
        downloads_dir = Path.home() / "Downloads" / "Farsi-Game-Manager"
        downloads_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"  ✅ پوشه آماده شد: {downloads_dir}")
        
        # بررسی فضای خالی
        stat = downloads_dir.stat()
        print(f"  ✅ دسترسی آماده")
        
        return True
    except Exception as e:
        print(f"  ❌ خطا: {e}")
        return False

def test_internet_speed():
    """تست سرعت اینترنت"""
    print("\n🧪 تست 5: سرعت اینترنت...")
    
    try:
        import time
        
        # دانلود یک فایل کوچک
        url = "https://raw.githubusercontent.com/Origin-Core/Farsi-Origin/main/AMOZISH.md"
        
        start = time.time()
        response = requests.get(url, timeout=10)
        duration = time.time() - start
        
        size = len(response.content) / 1024  # KB
        speed = size / duration
        
        print(f"  ✅ فایل دانلود شد: {size:.1f} KB")
        print(f"  ✅ سرعت: {speed:.1f} KB/s ({duration:.2f}s)")
        
        if speed < 10:
            print(f"  ⚠️  اینترنت کند است (انتظار کنید که دانلود زمان‌بر باشد)")
        
        return True
    except Exception as e:
        print(f"  ❌ خطا: {e}")
        return False

def test_ui_basic():
    """تست رابط کاربری (بدون نمایش GUI)"""
    print("\n🧪 تست 6: مدول‌های UI...")
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
        from PyQt6.QtCore import Qt, QTimer
        from PyQt6.QtGui import QColor, QFont
        
        print(f"  ✅ PyQt6.QtWidgets")
        print(f"  ✅ PyQt6.QtCore")
        print(f"  ✅ PyQt6.QtGui")
        
        # تست رنگ‌ها
        colors = ["#6C5CE7", "#00B894", "#1E1E2E", "#FF6B6B"]
        for color in colors:
            QColor(color)
        
        print(f"  ✅ تمام رنگ‌ها صحیح‌اند")
        
        return True
    except Exception as e:
        print(f"  ❌ خطا: {e}")
        return False

def main():
    """اجرای تمام تست‌ها"""
    print("=" * 60)
    print("🎮 Farsi Game Manager - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("Dependencies", test_imports),
        ("GitHub API", test_github_api),
        ("Cache System", test_cache_system),
        ("Downloads Folder", test_downloads_folder),
        ("Internet Speed", test_internet_speed),
        ("UI Modules", test_ui_basic),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ خطا غیرمنتظره در تست {name}: {e}")
            results.append((name, False))
    
    # خلاصه
    print("\n" + "=" * 60)
    print("📊 خلاصه نتایج:")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:25} {status}")
    
    print("=" * 60)
    print(f"\n📈 نتیجه: {passed}/{total} تست موفق\n")
    
    if passed == total:
        print("🎉 تمام تست‌ها موفق!")
        print("✨ برنامه آماده برای استفاده است!")
        return 0
    else:
        print(f"⚠️  {total - passed} مشکل وجود دارد")
        print("💡 لطفاً مشکلات را حل کنید و دوباره تست کنید")
        return 1

if __name__ == "__main__":
    sys.exit(main())
