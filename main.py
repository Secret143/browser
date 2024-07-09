import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout,
    QComboBox, QScrollArea, QPushButton, QInputDialog, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Responsive Design Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # Top section with URL input and reload all button
        self.top_section_layout = QHBoxLayout()
        
        self.address_bar = QLineEdit(self)
        self.address_bar.returnPressed.connect(self.load_url)
        self.top_section_layout.addWidget(self.address_bar)
        
        self.reload_all_button = QPushButton("Reload All", self)
        self.reload_all_button.clicked.connect(self.reload_all)
        self.top_section_layout.addWidget(self.reload_all_button)
        
        self.layout.addLayout(self.top_section_layout)
        
        self.web_area = QScrollArea()
        self.web_area.setWidgetResizable(True)
        self.web_area.setStyleSheet("""
            QScrollArea {
                background: white;
            }
            QScrollBar:horizontal {
                background: #f0f0f0;
                height: 15px;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 15px;
            }
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
            }
        """)
        
        self.canvas_widget = QWidget()
        self.canvas_layout = QHBoxLayout()
        self.canvas_widget.setLayout(self.canvas_layout)
        self.web_area.setWidget(self.canvas_widget)
        
        self.layout.addWidget(self.web_area)
        
        self.dropdown_button = QComboBox(self)
        self.dropdown_button.addItem("Add Screen Size")
        screen_sizes = [
            "Laptop (1366x768)",
            "Mobile (375x667)",
            "Tablet (768x1024)",
            "Desktop (1920x1080)",
            "TV (2560x1440)",
            "Monitor (3840x2160)",
            "Portrait Mobile (667x375)",
            "Portrait Tablet (1024x768)",
            "iPhone 14 (390x844)",
            "iPhone 15 Pro (430x932)",
            "Redmi Note 10 (393x873)",
            "Samsung Galaxy S21 (360x800)",
            "Google Pixel 5 (393x851)",
            "OnePlus 8 (412x869)",
            "Custom"
        ]
        for size in screen_sizes:
            self.dropdown_button.addItem(size)
        self.dropdown_button.activated[str].connect(self.add_screen)
        
        self.layout.addWidget(self.dropdown_button)
        
        self.web_views = []

    def load_url(self):
        url = self.address_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        qurl = QUrl(url)
        for web_view in self.web_views:
            web_view.setUrl(qurl)
    
    def add_screen(self, size):
        if size == "Add Screen Size":
            return
        elif size == "Custom":
            width, ok1 = QInputDialog.getInt(self, "Custom Screen Size", "Enter width:")
            height, ok2 = QInputDialog.getInt(self, "Custom Screen Size", "Enter height:")
            if not (ok1 and ok2):
                return
            size = f"Custom ({width}x{height})"
        else:
            width, height = map(int, size.split('(')[1].split(')')[0].split('x'))
        
        screen_widget = QWidget()
        screen_layout = QVBoxLayout()
        screen_widget.setLayout(screen_layout)

        size_label = QLabel(size, self)
        screen_layout.addWidget(size_label)

        web_view = QWebEngineView()
        web_view.setFixedSize(width, height)
        screen_layout.addWidget(web_view)

        reload_button = QPushButton("Reload", self)
        reload_button.clicked.connect(lambda: self.reload_screen(web_view))
        screen_layout.addWidget(reload_button)

        remove_button = QPushButton(f"Remove {size}", self)
        remove_button.clicked.connect(lambda: self.remove_screen(screen_widget))
        screen_layout.addWidget(remove_button)

        self.canvas_layout.addWidget(screen_widget)
        self.web_views.append(web_view)
        
        url = self.address_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        web_view.setUrl(QUrl(url))

    def reload_screen(self, web_view):
        web_view.reload()

    def reload_all(self):
        url = self.address_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        qurl = QUrl(url)
        for web_view in self.web_views:
            web_view.setUrl(qurl)

    def remove_screen(self, screen_widget):
        for i in range(self.canvas_layout.count()):
            if self.canvas_layout.itemAt(i).widget() == screen_widget:
                self.web_views.pop(i)
                self.canvas_layout.itemAt(i).widget().deleteLater()
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
