"""主窗口"""

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
)
from PySide6.QtGui import QIcon

from .category_manager import CategoryManager
from .utils import get_icon_path
from .widgets import CategoryWidget, FileDisplayWidget, FileInfoWidget

class FileHelper(QMainWindow):
    def __init__(self, style):
        super().__init__()
        self.style = style
        self.category_manager = CategoryManager()
        self.initUI()
        self.setup_connections()

    def initUI(self):
        style = self.style
        self.setWindowTitle("FileHelper")
        self.resize(960, 640)
        self.setMinimumSize(960, 640)
        self.setStyleSheet(f"background: {style['background']}; color: {style['text']};")
        
        icon_path = get_icon_path("category.svg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # 左侧分类区
        self.category_widget = CategoryWidget(style, self.category_manager)
        main_layout.addWidget(self.category_widget, 4)

        # 右侧区域
        right_widget = QWidget()
        right_widget.setStyleSheet(f"background: {style['background']}; color: {style['text']};")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(5)

        # 文件信息区
        self.file_info_widget = FileInfoWidget(style)
        
        # 文件展示区
        self.file_display_widget = FileDisplayWidget(style, self.category_manager, self.file_info_widget)
        right_layout.addWidget(self.file_display_widget, 7)
        right_layout.addWidget(self.file_info_widget, 3)

        main_layout.addWidget(right_widget, 11)

    def setup_connections(self):
        self.category_widget.main_window = self
        self.file_display_widget.main_window = self

    def on_category_changed(self):
        pass

    def on_category_selected(self, category_name):
        self.file_display_widget.update_category_display(category_name)