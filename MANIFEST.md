# 📋 فهرست فایل‌های پروژه

## 🎮 برنامه (Application)

| فایل | توضیح |
|------|--------|
| `main.py` | کد اصلی برنامه (PyQt6) |
| `requirements.txt` | Dependencies (pip) |
| `icon.png` / `icon.ico` | آیکون برنامه |
| `splash.png` | صفحه شروع |

## 🔨 ابزارهای ساخت (Build Tools)

| فایل | توضیح |
|------|--------|
| `build.bat` | Batch script برای ساختن EXE (Windows) |
| `build_exe_for_windows.py` | Python script برای ساختن EXE |
| `Farsi-Game-Manager.spec` | PyInstaller specification |
| `dist/` | پوشه EXE نهایی |

## 📦 نصب کننده (Installer)

| فایل | توضیح |
|------|--------|
| `install.bat` | نصب‌کننده برای Windows |
| `uninstall.bat` | حذف‌کننده برای Windows |
| `INSTALL_GUIDE_FA.md` | راهنمای نصب فارسی |

## 📚 مستندات (Documentation)

| فایل | توضیح |
|------|--------|
| `README.md` | توضیح برنامه و ویژگی‌ها |
| `DEPLOYMENT.md` | راهنمای배포 و release |
| `MANIFEST.md` | این فایل |

## ✅ تست (Testing)

| فایل | توضیح |
|------|--------|
| `test_app.py` | تست کامل برنامه |

## 📂 ساختار نهایی

```
Farsi-Game-Manager/
├── main.py                      ← کد اصلی
├── requirements.txt             ← Dependencies
├── test_app.py                  ← تست‌ها
├── icon.png / icon.ico         ← آیکون‌ها
├── splash.png                   ← صفحه شروع
├── build.bat                    ← Build batch
├── build_exe_for_windows.py    ← Build Python
├── install.bat                  ← Installer
├── uninstall.bat               ← Uninstaller
├── README.md                    ← مستندات اصلی
├── INSTALL_GUIDE_FA.md         ← راهنمای نصب
├── DEPLOYMENT.md               ← راهنمای배포
├── MANIFEST.md                 ← این فایل
├── dist/
│   └── Farsi-Game-Manager.exe  ← برنامه نهایی
└── build/
    └── (فایل‌های build موقتی)
```

---

## 🚀 آغاز سریع

### برای کاربران عادی:
```
1. Farsi-Game-Manager.exe رو دانلود کنید
2. دو برابر کلیک کنید
3. از برنامه استفاده کنید!
```

### برای توسعه‌دهندگان:
```bash
pip install -r requirements.txt
python main.py
```

### برای ساختن EXE:
```bash
python build_exe_for_windows.py
# یا
build.bat  # روی Windows
```

---

## 📊 تعداد خطوط کد

| فایل | خطوط | نوع |
|------|------|------|
| main.py | ~800 | Python |
| build_exe_for_windows.py | ~50 | Python |
| test_app.py | ~250 | Python |
| build.bat | ~20 | Batch |
| install.bat | ~50 | Batch |
| uninstall.bat | ~30 | Batch |
| **Total** | **~1200** | - |

---

## 🔧 فناوری‌های استفاده شده

- **PyQt6**: رابط کاربری گرافیکی
- **requests**: دانلود و GitHub API
- **PyInstaller**: تبدیل به EXE
- **GitHub API**: دریافت محصولات

---

## 📋 چک‌لیست تکمیل شده

### ✅ ویژگی‌های انجام شده:

- [x] رابط کاربری بسیار خوب
- [x] اتصال GitHub API
- [x] دانلود فایل‌ها
- [x] سیستم کش
- [x] تست کامل
- [x] اجرایی Windows
- [x] نصب‌کننده
- [x] مستندات کامل
- [x] بدون باگ
- [x] انیمیشن و transitions
- [x] پشتیبانی فارسی

### 🎯 آینده:

- [ ] ویرایش فایل‌ها درون برنامه
- [ ] سفارشی‌سازی رنگ‌ها
- [ ] مدیریت نسخه‌ها
- [ ] Update خودکار
- [ ] پشتیبانی macOS و Linux
- [ ] Telegram bot integration

---

## 📞 پشتیبانی

**مشکل یا سوال؟**
- 📧 origin.core.ir@gmail.com
- 💬 [@FARSI_ORIGIN](https://t.me/farsi_origin)
- 🐙 [GitHub Issues](https://github.com/Origin-Core/Farsi-Game-Manager/issues)

---

**نسخه**: 1.0.0  
**آخرین بروزرسانی**: 2024  
**وضعیت**: ✅ آماده برای استفاده
