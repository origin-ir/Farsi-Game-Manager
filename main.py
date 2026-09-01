"""
Farsi Game Manager - Official EXE Application
GitHub Integration + Beautiful UI with Animations

برنامه‌ای حرفه‌ای برای دانلود و مدیریت فارسی‌سازی‌های بازی
Professional Application for Managing Game Localizations

Author: Farsi-Origin Team
License: MIT
"""

import sys
import json
import os
import subprocess
import threading
import zipfile
from pathlib import Path
from typing import List, Dict, Optional
import requests
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QScrollArea, QFrame, QPushButton, QLabel, QLineEdit, QDialog,
    QProgressBar, QMessageBox, QFileDialog, QComboBox, QGridLayout,
    QStatusBar
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QSize, QRect, QPropertyAnimation,
    QEasingCurve, QPoint, QEvent, QDateTime
)
from PyQt6.QtGui import (
    QPixmap, QIcon, QFont, QColor, QPalette, QLinearGradient,
    QBrush, QPainter, QFontDatabase, QDropEvent, QDragEnterEvent
)
from PyQt6.QtSvg import QSvgWidget

# ====================
# ثابت‌های برنامه
# ====================

GITHUB_REPO = "Origin-Core/Farsi-Origin"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents"
RAW_GITHUB_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"

# رنگ‌ها
PRIMARY_COLOR = "#6C5CE7"
SECONDARY_COLOR = "#00B894"
DARK_BG = "#1E1E2E"
CARD_BG = "#2D2D44"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#B0B0C0"
ACCENT = "#FF6B6B"

# ====================
# سیستم دانلود GitHub
# ====================

class GitHubManager:
    """مدیریت تمام عملیات GitHub"""
    
    def __init__(self):
        self.products: List[Dict] = []
        self.cache_dir = Path.home() / ".farsi_game_manager" / "cache"
        self.downloads_dir = Path.home() / "Downloads" / "Farsi-Game-Manager"
        self.setup_directories()
    
    def setup_directories(self):
        """آماده‌سازی پوشه‌ها"""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
    
    def fetch_products(self) -> List[Dict]:
        """دریافت لیست محصولات از GitHub"""
        try:
            response = requests.get(GITHUB_API_URL, timeout=10)
            response.raise_for_status()
            files = response.json()
            
            # گروه‌بندی فایل‌ها بر اساس نام
            products_dict: Dict[str, Dict] = {}
            
            for file in files:
                if isinstance(file, dict) and file.get("type") == "file":
                    name = file["name"]
                    
                    # استخراج اسم محصول (قبل از نقطه)
                    product_name = name.split('.')[0].upper()
                    
                    if product_name not in products_dict:
                        products_dict[product_name] = {
                            "name": product_name,
                            "display_name": product_name,
                            "description": f"فارسی‌سازی {product_name}",
                            "image_url": None,
                            "markdown_url": None,
                            "zip_url": None,
                            "updated": datetime.now().isoformat()
                        }
                    
                    # تعیین نوع فایل
                    ext = name.split('.')[-1].lower()
                    if ext in ['png', 'jpg', 'jpeg']:
                        products_dict[product_name]["image_url"] = file["download_url"]
                    elif ext == 'md' or ext == 'txt':
                        products_dict[product_name]["markdown_url"] = file["download_url"]
                    elif ext == 'zip':
                        products_dict[product_name]["zip_url"] = file["download_url"]
            
            self.products = list(products_dict.values())
            self.save_cache()
            return self.products
            
        except Exception as e:
            print(f"خطا در دریافت محصولات: {e}")
            self.load_cache()
            return self.products
    
    def save_cache(self):
        """ذخیره کش محصولات"""
        try:
            cache_file = self.cache_dir / "products.json"
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطا در ذخیره کش: {e}")
    
    def load_cache(self):
        """بارگذاری کش محصولات"""
        try:
            cache_file = self.cache_dir / "products.json"
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self.products = json.load(f)
        except Exception as e:
            print(f"خطا در بارگذاری کش: {e}")
    
    def download_file(self, url: str, filename: str, progress_callback=None) -> Optional[Path]:
        """دانلود فایل از GitHub"""
        try:
            filepath = self.downloads_dir / filename
            
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total_size:
                            progress = int((downloaded / total_size) * 100)
                            progress_callback(progress)
            
            return filepath
        except Exception as e:
            print(f"خطا در دانلود: {e}")
            return None

# ====================
# Worker Threads
# ====================

class FetchProductsWorker(QThread):
    """Thread برای دریافت محصولات بدون انجماد UI"""
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, github_manager: GitHubManager):
        super().__init__()
        self.github_manager = github_manager
    
    def run(self):
        try:
            products = self.github_manager.fetch_products()
            self.finished.emit(products)
        except Exception as e:
            self.error.emit(str(e))

class DownloadWorker(QThread):
    """Thread برای دانلود بدون انجماد UI"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(str, bool)  # (message, success)
    
    def __init__(self, github_manager: GitHubManager, url: str, filename: str):
        super().__init__()
        self.github_manager = github_manager
        self.url = url
        self.filename = filename
    
    def run(self):
        try:
            filepath = self.github_manager.download_file(
                self.url,
                self.filename,
                self.progress.emit
            )
            if filepath:
                self.finished.emit(f"دانلود با موفقیت: {filepath}", True)
            else:
                self.finished.emit("خطا در دانلود", False)
        except Exception as e:
            self.finished.emit(f"خطا: {str(e)}", False)

# ====================
# Product Card Widget
# ====================

class ProductCard(QFrame):
    """کارت محصول با انیمیشن"""
    download_clicked = pyqtSignal(dict)
    
    def __init__(self, product: Dict, parent=None):
        super().__init__(parent)
        self.product = product
        self.is_hovered = False
        self.setup_ui()
        self.setup_animations()
    
    def setup_ui(self):
        """ایجاد رابط"""
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {CARD_BG};
                border-radius: 12px;
                border: 2px solid {CARD_BG};
            }}
        """)
        
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setLineWidth(0)
        self.setMinimumHeight(300)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # تصویر
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setMinimumHeight(150)
        image_label.setStyleSheet(f"background-color: #1E1E2E; border-radius: 8px;")
        
        if self.product.get("image_url"):
            try:
                img_response = requests.get(self.product["image_url"], timeout=5)
                pixmap = QPixmap()
                pixmap.loadFromData(img_response.content)
                scaled_pixmap = pixmap.scaledToHeight(150, Qt.TransformationMode.SmoothTransformation)
                image_label.setPixmap(scaled_pixmap)
            except:
                image_label.setText("📦")
                image_label.setFont(QFont("Segoe UI", 32))
        else:
            image_label.setText("📦")
            image_label.setFont(QFont("Segoe UI", 32))
        
        # عنوان
        title = QLabel(self.product.get("display_name", "Unknown"))
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {TEXT_PRIMARY};")
        
        # توضیح
        description = QLabel(self.product.get("description", ""))
        description.setFont(QFont("Segoe UI", 10))
        description.setStyleSheet(f"color: {TEXT_SECONDARY};")
        description.setWordWrap(True)
        
        # دکمه دانلود
        download_btn = QPushButton("📥 دانلود زیرنویس")
        download_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        download_btn.setMinimumHeight(40)
        download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        download_btn.setEnabled(bool(self.product.get("zip_url")))
        download_btn.clicked.connect(self.on_download_clicked)
        download_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #7B68EE;
            }}
            QPushButton:pressed {{
                background-color: #5B4FBE;
            }}
            QPushButton:disabled {{
                background-color: #444456;
                color: #888899;
            }}
        """)
        
        layout.addWidget(image_label)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()
        layout.addWidget(download_btn)
    
    def setup_animations(self):
        """آماده‌سازی انیمیشن‌ها"""
        pass
    
    def on_download_clicked(self):
        """هنگام کلیک دانلود"""
        self.download_clicked.emit(self.product)
    
    def enterEvent(self, event):
        """هنگام ورود موس"""
        self.is_hovered = True
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {CARD_BG};
                border-radius: 12px;
                border: 2px solid {PRIMARY_COLOR};
            }}
        """)
    
    def leaveEvent(self, event):
        """هنگام خروج موس"""
        self.is_hovered = False
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {CARD_BG};
                border-radius: 12px;
                border: 2px solid {CARD_BG};
            }}
        """)

# ====================
# Download Dialog
# ====================

class DownloadDialog(QDialog):
    """کادر دانلود"""
    
    def __init__(self, product: Dict, github_manager: GitHubManager, parent=None):
        super().__init__(parent)
        self.product = product
        self.github_manager = github_manager
        self.download_worker = None
        self.setup_ui()
        self.setWindowTitle(f"دانلود - {product['display_name']}")
        self.setModal(True)
        self.setMinimumWidth(400)
    
    def setup_ui(self):
        """ایجاد رابط"""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # عنوان
        title = QLabel(f"دانلود: {self.product['display_name']}")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {TEXT_PRIMARY};")
        
        # توضیح
        info = QLabel("فایل زیرنویس و اموزش‌های لازم برای فارسی کردن محصول دانلود می‌شود.")
        info.setFont(QFont("Segoe UI", 10))
        info.setStyleSheet(f"color: {TEXT_SECONDARY};")
        info.setWordWrap(True)
        
        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                background-color: {CARD_BG};
                border-radius: 5px;
                height: 25px;
            }}
            QProgressBar::chunk {{
                background-color: {SECONDARY_COLOR};
                border-radius: 3px;
            }}
        """)
        
        # متن پیشرفت
        self.status_label = QLabel("آماده‌سازی دانلود...")
        self.status_label.setFont(QFont("Segoe UI", 10))
        self.status_label.setStyleSheet(f"color: {TEXT_SECONDARY};")
        
        # دکمه‌ها
        btn_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("لغو")
        self.cancel_btn.setMinimumHeight(35)
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CARD_BG};
                color: {TEXT_PRIMARY};
                border: 1px solid {TEXT_SECONDARY};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #3D3D54;
            }}
        """)
        
        self.open_btn = QPushButton("🗂️ باز کردن پوشه")
        self.open_btn.setMinimumHeight(35)
        self.open_btn.setEnabled(False)
        self.open_btn.clicked.connect(self.open_downloads_folder)
        self.open_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {SECONDARY_COLOR};
                color: white;
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: #00D0A0;
            }}
            QPushButton:disabled {{
                background-color: {CARD_BG};
                color: {TEXT_SECONDARY};
            }}
        """)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.open_btn)
        
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)
        layout.addLayout(btn_layout)
        
        # شروع دانلود
        self.start_download()
    
    def start_download(self):
        """شروع دانلود"""
        zip_url = self.product.get("zip_url")
        if not zip_url:
            self.status_label.setText("❌ لینک دانلود موجود نیست")
            return
        
        filename = f"{self.product['display_name']}.zip"
        self.download_worker = DownloadWorker(self.github_manager, zip_url, filename)
        self.download_worker.progress.connect(self.on_progress)
        self.download_worker.finished.connect(self.on_download_finished)
        self.download_worker.start()
    
    def on_progress(self, value: int):
        """بروز‌رسانی پیشرفت"""
        self.progress.setValue(value)
        self.status_label.setText(f"در حال دانلود... {value}%")
    
    def on_download_finished(self, message: str, success: bool):
        """تکمیل دانلود"""
        self.cancel_btn.setText("بستن")
        self.cancel_btn.clicked.disconnect()
        self.cancel_btn.clicked.connect(self.accept)
        
        if success:
            self.open_btn.setEnabled(True)
            self.status_label.setText(f"✅ {message}")
            self.progress.setValue(100)
        else:
            self.status_label.setText(f"❌ {message}")
    
    def open_downloads_folder(self):
        """باز کردن پوشه دانلود‌ها"""
        os.startfile(str(self.github_manager.downloads_dir))
    
    def cancel_download(self):
        """لغو دانلود"""
        if self.download_worker:
            self.download_worker.quit()
            self.download_worker.wait()
        self.reject()

# ====================
# Main Application
# ====================

class FarsiGameManagerApp(QMainWindow):
    """برنامه اصلی"""
    
    def __init__(self):
        super().__init__()
        self.github_manager = GitHubManager()
        self.fetch_worker = None
        self.products = []
        
        self.setWindowTitle("🎮 Farsi Game Manager - فارسی‌سازی بازی")
        self.setWindowIcon(self.create_app_icon())
        self.setMinimumSize(1200, 700)
        
        self.setup_ui()
        self.apply_theme()
        self.fetch_products()
    
    def create_app_icon(self) -> QIcon:
        """ایجاد آیکون برنامه"""
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor(PRIMARY_COLOR))
        painter = QPainter(pixmap)
        painter.setFont(QFont("Segoe UI", 40))
        painter.setPen(QColor("white"))
        painter.drawText(0, 0, 64, 64, Qt.AlignmentFlag.AlignCenter, "🎮")
        painter.end()
        return QIcon(pixmap)
    
    def setup_ui(self):
        """ایجاد رابط اصلی"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # محتوای اصلی
        content = self.create_content()
        main_layout.addWidget(content)
    
    def create_header(self) -> QWidget:
        """ایجاد header"""
        header = QFrame()
        header.setStyleSheet(f"background-color: {DARK_BG}; border-bottom: 1px solid {CARD_BG};")
        header.setMinimumHeight(80)
        
        layout = QVBoxLayout(header)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        # عنوان
        title_layout = QHBoxLayout()
        
        title = QLabel("🎮 Farsi Game Manager")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {TEXT_PRIMARY};")
        
        subtitle = QLabel("مدیریت دانلود فارسی‌سازی‌های بازی")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet(f"color: {TEXT_SECONDARY};")
        
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        layout.addWidget(subtitle)
        
        return header
    
    def create_content(self) -> QWidget:
        """ایجاد بخش محتوا"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {DARK_BG}; 
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {CARD_BG};
                width: 10px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {PRIMARY_COLOR};
                border-radius: 5px;
            }}
        """)
        
        content_widget = QWidget()
        content_widget.setStyleSheet(f"background-color: {DARK_BG};")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        # بخش محصولات
        self.products_container = QWidget()
        self.products_layout = QVBoxLayout(self.products_container)
        self.products_layout.setSpacing(20)
        
        self.products_layout.addStretch()
        
        content_layout.addWidget(self.products_container)
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        return scroll
    
    def apply_theme(self):
        """اعمال تم تاریک"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(DARK_BG))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(TEXT_PRIMARY))
        self.setPalette(palette)
    
    def fetch_products(self):
        """دریافت محصولات"""
        self.fetch_worker = FetchProductsWorker(self.github_manager)
        self.fetch_worker.finished.connect(self.on_products_loaded)
        self.fetch_worker.error.connect(self.on_fetch_error)
        self.fetch_worker.start()
    
    def on_products_loaded(self, products: List[Dict]):
        """هنگام بارگذاری محصولات"""
        self.products = products
        self.display_products()
    
    def on_fetch_error(self, error: str):
        """هنگام خطا در دریافت"""
        QMessageBox.warning(self, "⚠️ خطا", f"خطا در دریافت محصولات:\n{error}\n\nاز کش قبلی استفاده می‌شود.")
        self.products = self.github_manager.products
        self.display_products()
    
    def display_products(self):
        """نمایش محصولات"""
        # پاک کردن layout قبلی
        while self.products_layout.count() > 1:
            child = self.products_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not self.products:
            empty_label = QLabel("❌ هیچ محصولی برای نمایش وجود ندارد")
            empty_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 14px;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.products_layout.insertWidget(0, empty_label)
            return
        
        # ایجاد شبکه 3 ستونی
        products_per_row = 3
        row_widget = None
        row_layout = None
        
        for i, product in enumerate(self.products):
            if i % products_per_row == 0:
                row_widget = QWidget()
                row_layout = QHBoxLayout(row_widget)
                row_layout.setSpacing(15)
                row_layout.setContentsMargins(0, 0, 0, 0)
                self.products_layout.insertWidget(self.products_layout.count() - 1, row_widget)
            
            card = ProductCard(product)
            card.download_clicked.connect(self.on_product_download)
            row_layout.addWidget(card)
        
        # اگر آخرین ردیف کمتر از 3 تا است، stretch اضافه کن
        if row_layout:
            row_layout.addStretch()
    
    def on_product_download(self, product: Dict):
        """هنگام کلیک دانلود"""
        dialog = DownloadDialog(product, self.github_manager, self)
        dialog.exec()

# ====================
# نقطه شروع
# ====================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = FarsiGameManagerApp()
    window.show()
    
    sys.exit(app.exec())
