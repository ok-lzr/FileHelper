"""文件信息展示区控件"""

import os
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from ..utils import get_icon_path, format_file_size

class FileInfoWidget(QWidget):
    def __init__(self, style):
        super().__init__()
        self.style = style
        self.current_file = None
        self.initUI()
        
    def initUI(self):
        style = self.style
        self.setStyleSheet(f"""
            QWidget {{
                background: {style['file_info_bg']};
                border: 1px solid {style['file_info_border']};
                border-radius: 5px;
            }}
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        title_label = QLabel("文件信息")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {style['text']};
                font-size: 16px;
                font-weight: bold;
                border: none;
                background: transparent;
                padding-bottom: 5px;
                border-bottom: 2px solid {style['file_border']};
            }}
        """)
        main_layout.addWidget(title_label)
        
        self.name_label = QLabel("未选择文件")
        self.name_label.setWordWrap(True)
        self.name_label.setStyleSheet(f"""
            QLabel {{
                color: {style['text']};
                font-size: 14px;
                font-weight: bold;
                border: none;
                background: transparent;
                padding: 10px 0;
            }}
        """)
        main_layout.addWidget(self.name_label)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                width: 8px;
                background: transparent;
            }}
            QScrollBar::handle:vertical {{
                background: {style['file_border']};
                border-radius: 4px;
            }}
        """)
        
        self.info_content = QWidget()
        self.info_layout = QVBoxLayout(self.info_content)
        self.info_layout.setContentsMargins(0, 0, 0, 0)
        self.info_layout.setSpacing(8)
        self.info_layout.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.info_content)
        main_layout.addWidget(scroll_area, 1)
        
        self.info_items = []
    
    def clear_info(self):
        for item in self.info_items:
            item.deleteLater()
        self.info_items.clear()
        self.name_label.setText("未选择文件")
        self.current_file = None
    
    def display_file_info(self, file_info):
        self.clear_info()
        self.current_file = file_info
        style = self.style
        
        self.name_label.setText(file_info['name'])
        
        # 文件路径
        self.add_info_item("路径", file_info['path'], "file_info")
        
        # 文件类型
        file_type = file_info.get('type', '')
        if file_type:
            self.add_info_item("类型", file_type, "file_info")
        
        # 文件大小
        size_bytes = file_info.get('size', 0)
        if size_bytes > 0:
            self.add_info_item("大小", format_file_size(size_bytes), "file_size")
        else:
            self.add_info_item("大小", "未知", "file_size")
        
        # 添加时间
        added_time = file_info.get('added_time', '')
        if added_time:
            self.add_info_item("添加时间", added_time, "file_time")
        
        # 修改时间
        file_path = file_info.get('path', '')
        if file_path and os.path.exists(file_path):
            mtime = os.path.getmtime(file_path)
            mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            self.add_info_item("修改时间", mtime_str, "file_time")
        
        # 文件状态
        if file_path:
            if os.path.exists(file_path):
                self.add_info_item("状态", "✓ 文件存在", "file_info")
            else:
                self.add_info_item("状态", "✗ 文件不存在", "file_info")
    
    def add_info_item(self, label, value, icon_name=""):
        style = self.style
        
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(0, 5, 0, 5)
        item_layout.setSpacing(10)
        
        if icon_name:
            icon_path = get_icon_path(f"{icon_name}.svg")
            if os.path.exists(icon_path):
                icon_label = QLabel()
                icon_label.setPixmap(QIcon(icon_path).pixmap(16, 16))
                icon_label.setFixedSize(20, 20)
                icon_label.setAlignment(Qt.AlignCenter)
                icon_label.setStyleSheet(f"""
                    QLabel {{
                        border: none;
                        background: transparent;
                        color: {style['info_icon_fg']};
                    }}
                """)
                item_layout.addWidget(icon_label)
        
        label_widget = QLabel(f"{label}:")
        label_widget.setFixedWidth(80)
        label_widget.setStyleSheet(f"""
            QLabel {{
                color: {style['info_label_fg']};
                font-size: 12px;
                font-weight: bold;
                border: none;
                background: transparent;
            }}
        """)
        item_layout.addWidget(label_widget)
        
        value_widget = QLabel(value)
        value_widget.setWordWrap(True)
        value_widget.setStyleSheet(f"""
            QLabel {{
                color: {style['info_value_fg']};
                font-size: 12px;
                border: none;
                background: transparent;
            }}
        """)
        item_layout.addWidget(value_widget, 1)
        
        self.info_layout.addWidget(item_widget)
        self.info_items.append(item_widget)
    
    def update_styles(self, style):
        self.style = style
        if self.current_file:
            self.display_file_info(self.current_file)