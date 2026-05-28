"""单个文件项控件"""

import os
import subprocess
import platform
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QWidget, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from ..utils import get_icon_path, get_file_extension, create_file_icon

class FileItemWidget(QFrame):
    def __init__(self, file_info, style, category_name, category_manager, parent_widget):
        super().__init__()
        self.file_info = file_info
        self.style = style
        self.category_name = category_name
        self.category_manager = category_manager
        self.parent_widget = parent_widget
        self.selected = False
        self.initUI()
        
    def initUI(self):
        style = self.style
        
        self.setFrameStyle(QFrame.NoFrame)
        self.setCursor(Qt.PointingHandCursor)
        self.update_style()
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 8, 10, 8)
        main_layout.setSpacing(10)
        
        # 左侧：文件图标
        file_icon_label = QLabel()
        extension = get_file_extension(self.file_info['name'])
        icon = create_file_icon(extension, 48)
        file_icon_label.setPixmap(icon.pixmap(48, 48))
        file_icon_label.setFixedSize(48, 48)
        main_layout.addWidget(file_icon_label)
        
        # 中间：文件信息
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(5)
        
        file_name_label = QLabel(self.file_info['name'])
        file_name_label.setStyleSheet(f"""
            QLabel {{
                color: {style['file_name_fg']};
                font-size: 14px;
                font-weight: bold;
                border: none;
                background: transparent;
            }}
        """)
        file_name_label.setWordWrap(True)
        info_layout.addWidget(file_name_label)
        
        file_path_label = QLabel(self.file_info['path'])
        file_path_label.setStyleSheet(f"""
            QLabel {{
                color: {style['file_path_fg']};
                font-size: 11px;
                border: none;
                background: transparent;
            }}
        """)
        file_path_label.setWordWrap(True)
        info_layout.addWidget(file_path_label)
        
        main_layout.addWidget(info_widget, 1)
        
        # 右侧：操作按钮
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(5)
        
        # 打开文件按钮
        open_file_btn = QPushButton()
        open_file_btn.setIcon(QIcon(get_icon_path("open_file.svg")))
        open_file_btn.setIconSize(QSize(16, 16))
        open_file_btn.setFixedSize(32, 32)
        open_file_btn.setToolTip("打开文件")
        open_file_btn.setStyleSheet(f"""
            QPushButton {{
                background: {style['open_file_btn_bg']};
                border: none;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background: {style['open_file_btn_bg_hover']};
            }}
        """)
        open_file_btn.clicked.connect(self.open_file)
        buttons_layout.addWidget(open_file_btn)
        
        # 打开文件所在位置按钮
        open_folder_btn = QPushButton()
        open_folder_btn.setIcon(QIcon(get_icon_path("open_folder.svg")))
        open_folder_btn.setIconSize(QSize(16, 16))
        open_folder_btn.setFixedSize(32, 32)
        open_folder_btn.setToolTip("打开文件所在位置")
        open_folder_btn.setStyleSheet(f"""
            QPushButton {{
                background: {style['open_folder_btn_bg']};
                border: none;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background: {style['open_folder_btn_bg_hover']};
            }}
        """)
        open_folder_btn.clicked.connect(self.open_file_location)
        buttons_layout.addWidget(open_folder_btn)
        
        # 删除文件按钮
        remove_file_btn = QPushButton()
        remove_file_btn.setIcon(QIcon(get_icon_path("remove_file.svg")))
        remove_file_btn.setIconSize(QSize(16, 16))
        remove_file_btn.setFixedSize(32, 32)
        remove_file_btn.setToolTip("从分类中移除文件")
        remove_file_btn.setStyleSheet(f"""
            QPushButton {{
                background: {style['remove_file_btn_bg']};
                border: none;
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background: {style['remove_file_btn_bg_hover']};
            }}
        """)
        remove_file_btn.clicked.connect(self.remove_file)
        buttons_layout.addWidget(remove_file_btn)
        
        main_layout.addWidget(buttons_widget)
    
    def update_style(self):
        style = self.style
        if self.selected:
            self.setStyleSheet(f"""
                QFrame {{
                    background: {style['file_item_selected_bg']};
                    border: 2px solid {style['open_file_btn_bg']};
                    border-radius: 5px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QFrame {{
                    background: {style['file_item_bg']};
                    border: 1px solid {style['file_border']};
                    border-radius: 5px;
                }}
                QFrame:hover {{
                    background: {style['file_item_bg_hover']};
                }}
            """)
    
    def set_selected(self, selected):
        self.selected = selected
        self.update_style()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent_widget.select_file_item(self)
        super().mousePressEvent(event)
    
    def open_file(self):
        if os.path.exists(self.file_info['path']):
            try:
                if platform.system() == 'Windows':
                    os.startfile(self.file_info['path'])
                elif platform.system() == 'Darwin':
                    subprocess.run(['open', self.file_info['path']])
                else:
                    subprocess.run(['xdg-open', self.file_info['path']])
            except Exception as e:
                QMessageBox.warning(self, "错误", f"无法打开文件：{str(e)}")
        else:
            QMessageBox.warning(self, "错误", "文件不存在！")
    
    def open_file_location(self):
        file_dir = os.path.dirname(self.file_info['path'])
        if os.path.exists(file_dir):
            try:
                if platform.system() == 'Windows':
                    os.startfile(file_dir)
                elif platform.system() == 'Darwin':
                    subprocess.run(['open', '-R', self.file_info['path']])
                else:
                    subprocess.run(['xdg-open', file_dir])
            except Exception as e:
                QMessageBox.warning(self, "错误", f"无法打开文件位置：{str(e)}")
        else:
            QMessageBox.warning(self, "错误", "文件目录不存在！")
    
    def remove_file(self):
        reply = QMessageBox.question(
            self, "确认移除", 
            f"确定要从分类中移除文件\"{self.file_info['name']}\"吗？\n（不会删除原文件）",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.category_manager.remove_file_from_category(self.category_name, self.file_info['path']):
                self.parent_widget.refresh_file_list()