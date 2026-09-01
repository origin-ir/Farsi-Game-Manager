# 🚀 Deployment Guide - راهنمای배포

## نسخه‌های موجود

### 1️⃣ Standalone EXE (بهترین)
- **فایل**: `Farsi-Game-Manager.exe`
- **اندازه**: ~80-100 MB
- **نیازمندی**: Windows 10/11
- **مزایا**: نصب‌نشدنی، موارد بدون نیاز
- **استفاده**: فقط دو برابر کلیک کنید!

### 2️⃣ Source Code (برای توسعه‌دهندگان)
- **فایل**: `main.py` + `requirements.txt`
- **نیازمندی**: Python 3.8+
- **مزایا**: قابل تغییر، open-source
- **استفاده**: `python main.py`

### 3️⃣ Installer Package
- **فایل**: `install.bat`
- **نیازمندی**: Windows + EXE
- **مزایا**: آسان نصب، shortcuts خودکار
- **استفاده**: دو برابر کلیک کنید

---

## نحوه ساختن EXE برای Windows

### روش 1: روی Windows خودتان

```bash
# 1. Clone repository
git clone https://github.com/Origin-Core/Farsi-Game-Manager.git
cd Farsi-Game-Manager

# 2. نصب Python 3.8+ و pip

# 3. نصب dependencies
pip install -r requirements.txt

# 4. ساختن EXE
python build_exe_for_windows.py

# نتیجه: dist/Farsi-Game-Manager.exe
```

### روش 2: استفاده از Docker (روی هر OS)

```bash
# Docker image برای ساختن EXE برای Windows
docker run -v $(pwd):/src \
    cdrx/pyinstaller-windows \
    pyinstaller --onefile \
    --windowed \
    --name Farsi-Game-Manager \
    --icon=icon.ico \
    main.py
```

### روش 3: GitHub Actions (خودکار)

اگر نسخه جدید رو push کنید، GitHub Actions به طور خودکار:
1. EXE رو می‌سازد
2. Release رو انتشار می‌دهد
3. فایل رو Download می‌کنید

---

## ایجاد نسخه جدید

### Step 1: بروزرسانی کد

```bash
# تغییرات خود را کنید
# فایل‌ها را تغییر دهید
# تست کنید

python test_app.py  # اطمینان بخش
```

### Step 2: سیمانتیک Versioning

فایل `main.py` را ویرایش کنید:

```python
VERSION = "1.0.1"  # X.Y.Z
CHANGELOG = {
    "1.0.1": [
        "✅ بگ فیکس",
        "✨ ویژگی جدید"
    ]
}
```

### Step 3: Commit و Push

```bash
git add .
git commit -m "Release v1.0.1: Description"
git tag v1.0.1
git push origin main
git push origin v1.0.1
```

### Step 4: ساختن Release

```bash
# ساختن EXE
python build_exe_for_windows.py

# یا کلیک روی GitHub Actions
```

---

## توزیع

### آپلود به GitHub Releases

1. برنامه: https://github.com/Origin-Core/Farsi-Game-Manager
2. Releases tab → Create release
3. آپلود کنید:
   - `dist/Farsi-Game-Manager.exe`
   - `install.bat`
   - `uninstall.bat`
   - `README_FA.md`

### ساخت Installer خودکار

استفاده از NSIS برای ساختن `.msi` installer:

```bash
# 1. NSIS نصب کنید
# 2. فایل `installer.nsi` ایجاد کنید
# 3. NSIS compiler اجرا کنید
makensis installer.nsi
# نتیجه: Farsi-Game-Manager-Setup.exe
```

---

## QA و تست

### Before Release:

```bash
# 1. تمام تست‌ها
python test_app.py

# 2. اجرای برنامه
python main.py

# 3. بررسی EXE
dist/Farsi-Game-Manager.exe

# 4. تست نصب‌کننده
install.bat
```

### Test Cases:

- ✅ برنامه شروع می‌شود
- ✅ محصولات بارگذاری می‌شوند
- ✅ دانلود کار می‌کند
- ✅ Progress bar صحیح است
- ✅ اخطارها صحیح نمایش داده می‌شوند
- ✅ فایل cache کار می‌کند
- ✅ offfline mode کار می‌کند

---

## مراقبت و نگهداری

### وظایف ماهانه:

```bash
# Dependencies را بروز کنید
pip install --upgrade -r requirements.txt

# تست کنید
python test_app.py

# EXE جدید بسازید و release کنید
```

### مراقبت GitHub:

1. Issues را بررسی کنید
2. Bug reports را پاسخ دهید
3. PR ها را review کنید
4. Documentation را بروز کنید

---

## بک‌آپ و بازیابی

### بک‌آپ کنید:

```bash
# تمام source code
zip -r Farsi-Game-Manager-backup.zip .

# فقط Release
zip Farsi-Game-Manager-exe.zip dist/Farsi-Game-Manager.exe
```

### بازیابی:

اگر مشکل پیش آمد:

```bash
# دنبالت کنید
git log --oneline

# برگردان
git checkout v1.0.0
```

---

## نمونه Release Checklist

```
[ ] کد بروز شده و تست شده
[ ] Version number بروز شده
[ ] CHANGELOG آپدیت شده
[ ] README بررسی شده
[ ] EXE ساخته شده
[ ] تمام تست‌ها Pass کردند
[ ] اندازه فایل قابل قبول است
[ ] Release Notes نوشته شده
[ ] Upload کردند
[ ] Tag ایجاد شد
[ ] Announcement شد
```

---

**نسخه**: 1.0.0  
**آخرین بروزرسانی**: 2024  
**وضعیت**: ✅ تولید
