# 📦 راهنمای نصب Farsi Game Manager

## سریع‌ترین روش (پیشنهادی)

### مرحله 1: دانلود فایل
1. فایل `Farsi-Game-Manager.exe` را از اینجا دانلود کنید
2. یا از [GitHub Releases](https://github.com/Origin-Core/Farsi-Game-Manager/releases) دانلود کنید

### مرحله 2: اجرا
- فایل `.exe` را دو بار کلیک کنید
- **تمام!** ✅

> ⚠️ **نکته**: نیازی به نصب Python یا هیچ برنامه دیگری نیست!

---

## نصب با Installer (بهتر برای استفاده طولانی‌مدت)

### مرحله 1: دانلود Installer
- فایل `install.bat` را دانلود کنید
- یا تمام فایل‌های پروژه را دانلود کنید

### مرحله 2: اجرای Installer
1. فایل `install.bat` را کلیک کنید
2. دستوری را برای نصب تأیید کنید
3. انتظار برای تکمیل نصب
4. اختیار اجرای برنامه بعد از نصب

### مرحله 3: استفاده
- برنامه روی Desktop شما ایجاد شده است
- یا از Start Menu برنامه را جستجو کنید

---

## خطای رایج و حل‌ها

### ❌ خطا: "فایل ایجاد نشده"
**حل**: 
- فایل `install.bat` و `dist/Farsi-Game-Manager.exe` را در یک پوشه قرار دهید
- Installer را دوباره اجرا کنید

### ❌ خطا: "دسترسی رد شد"
**حل**:
- Installer را به عنوان Administrator اجرا کنید
- روی فایل کلیک کنید → Run as Administrator

### ❌ خطا: "Windows Defender مسدود کرده"
**حل**:
1. پیام Defender را ببینید
2. "اطلاعات بیشتر" کلیک کنید
3. "اجرا کنید" کلیک کنید

---

## حذف برنامه

### روش 1: استفاده از Uninstaller
1. فایل `uninstall.bat` را اجرا کنید
2. تأیید حذف
3. **تمام!** ✅

### روش 2: دستی
1. به `%ProgramFiles%\Farsi-Game-Manager` بروید
2. پوشه را حذف کنید
3. Shortcut‌ها را از Desktop و Start Menu حذف کنید

---

## مشکلات پیشرفته

### مسئله: برنامه پس از نصب اجرا نمی‌شود

**تشخیص مشکل:**
```
1. آیا پیام خطا دیده‌اید؟
2. ویندوز کدام نسخه دارید (10 یا 11)?
3. چقدر RAM دارید؟
```

**حل‌های ممکن:**
- Windows 10 رو به روز کنید
- تمام برنامه‌های زمینه را ببندید
- RAM خود را آزاد کنید
- برنامه را دوباره نصب کنید

### مسئله: فایل‌های دانلود‌شده مفقود

**مکان‌های عام:**
- `C:\Users\[YourUsername]\Downloads\Farsi-Game-Manager`
- دسکتاپ
- مجلد اسناد

**راه‌حل:**
1. Windows File Explorer را باز کنید
2. مسیری که برنامه نشان می‌دهد را بروید
3. فایل‌های دانلود‌شده را استخراج کنید

---

## نصب برای توسعه‌دهندگان

اگر می‌خواهید کد را اصلاح یا توسعه دهید:

### نیازمندی‌ها:
- Python 3.8+ (دانلود از [python.org](https://www.python.org))
- Git (اختیاری)

### مراحل:

```bash
# 1. Repository را Clone کنید
git clone https://github.com/Origin-Core/Farsi-Game-Manager.git
cd Farsi-Game-Manager

# 2. Python Environment را ایجاد کنید
python -m venv venv
venv\Scripts\activate

# 3. Dependencies را نصب کنید
pip install -r requirements.txt

# 4. برنامه را اجرا کنید
python main.py

# 5. EXE را ساختن (اختیاری)
python build_exe_for_windows.py
```

---

## نکات مهم

✅ **موارد نیاز:**
- Windows 10 یا 11 (64-bit)
- 512 MB RAM حداقل
- 100 MB فضای خالی

✅ **معمول است:**
- اولین بار اجرا قد زمان‌بر باشد (کش‌ها درحال تولید هستند)
- درخواست Firewall نمایش داده شود (نیاز برای اتصال GitHub)

⚠️ **احتیاطات:**
- برنامه را از منابع معتبر دانلود کنید
- نسخه‌های فایل‌ها را پشتیبان گیری کنید
- قبل از دانلود بزرگ، اتصال اینترنت را بررسی کنید

---

## پشتیبانی

اگر با مشکل روبرو شدید:

1. **GitHub Issues**: [Issues Page](https://github.com/Origin-Core/Farsi-Game-Manager/issues)
2. **Telegram**: [@FARSI_ORIGIN](https://t.me/farsi_origin)
3. **Email**: origin.core.ir@gmail.com

---

**آخرین بروزرسانی**: 2024
**نسخه برنامه**: 1.0.0
**سیستم عامل پشتیبانی**: Windows 10/11 (64-bit)
