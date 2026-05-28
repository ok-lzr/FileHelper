"""文件展示区控件"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QFileDialog, QInputDialog, QMessageBox, QLineEdit
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

from ..utils import get_icon_path
from .file_list_widget import FileListWidget

class FileDisplayWidget(QWidget):
    def __init__(self, style, category_manager, file_info_widget):
        super().__init__()
        self.style = style
        self.category_manager = category_manager
        self.file_info_widget = file_info_widget
        self.initUI()

    def initUI(self):
        style = self.style
        self.setStyleSheet(f"background: {style['background']}; color: {style['text']};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        # 顶部工具栏
        toolbar = QWidget()
        toolbar.setFixedHeight(60)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        toolbar_layout.setSpacing(10)

        self.category_name_label = QLabel("未选择分类")
        self.category_name_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {style['toolbar_label_fg']};
                padding: 5px;
            }}
        """)
        toolbar_layout.addWidget(self.category_name_label)

        toolbar_layout.addStretch()

        # 添加文件按钮
        self.add_file_button = QPushButton(" 添加文件")
        self.add_file_button.setFixedSize(110, 35)
        self.add_file_button.setIcon(QIcon(get_icon_path("add_file.svg")))
        self.add_file_button.setIconSize(QSize(18, 18))
        self.add_file_button.setStyleSheet(f"""
            QPushButton {{
                background: {style['add_file_btn_bg']};
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                text-align: left;
                padding-left: 8px;
            }}
            QPushButton:hover {{
                background: {style['add_file_btn_bg_hover']};
            }}
        """)
        self.add_file_button.clicked.connect(self.add_file_to_category)
        toolbar_layout.addWidget(self.add_file_button)

        # 重命名分类按钮
        self.rename_button = QPushButton(" 重命名")
        self.rename_button.setFixedSize(100, 35)
        self.rename_button.setIcon(QIcon(get_icon_path("rename.svg")))
        self.rename_button.setIconSize(QSize(18, 18))
        self.rename_button.setStyleSheet(f"""
            QPushButton {{
                background: {style['rename_btn_bg']};
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                text-align: left;
                padding-left: 8px;
            }}
            QPushButton:hover {{
                background: {style['rename_btn_bg_hover']};
            }}
        """)
        self.rename_button.clicked.connect(self.rename_category)
        toolbar_layout.addWidget(self.rename_button)

        # 删除分类按钮
        self.delete_button = QPushButton(" 删除")
        self.delete_button.setFixedSize(100, 35)
        self.delete_button.setIcon(QIcon(get_icon_path("delete.svg")))
        self.delete_button.setIconSize(QSize(18, 18))
        self.delete_button.setStyleSheet(f"""
            QPushButton {{
                background: {style['delete_btn_bg']};
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                text-align: left;
                padding-left: 8px;
            }}
            QPushButton:hover {{
                background: {style['delete_btn_bg_hover']};
            }}
        """)
        self.delete_button.clicked.connect(self.delete_category)
        toolbar_layout.addWidget(self.delete_button)

        main_layout.addWidget(toolbar)

        # 文件列表区域
        self.file_list_widget = FileListWidget(style, self.category_manager, self.file_info_widget)
        main_layout.addWidget(self.file_list_widget, 1)

        self.main_window = None

    def update_styles(self, style):
        self.style = style
        self.setStyleSheet(f"background: {style['background']}; color: {style['text']};")
        self.category_name_label.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {style['toolbar_label_fg']};
                padding: 5px;
            }}
        """)
        self.add_file_button.setStyleSheet(f"""
            QPushButton {{
                background: {style['add_file_btn_bg']};
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                text-align: left;
                padding-left: 8px;
            }}
            QPushButton:hover {{
                background: {style['add_file_btn_bg_hover']};
            }}
        """)
        self.rename_button.setStyleSheet(f"""
            QPushButton {{
                background: {style['rename_btn_bg']};
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                text-align: left;
                padding-left: 8px;
            }}
            QPushButton:hover {{
                background: {style['rename_btn_bg_hover']};
            }}
        """)
        self.delete_button.setStyleSheet(f"""
            QPushButton {{
                background: {style['delete_btn_bg']};
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
                text-align: left;
                padding-left: 8px;
            }}
            QPushButton:hover {{
                background: {style['delete_btn_bg_hover']};
            }}
        """)
        # 更新文件列表样式
        self.file_list_widget.update_styles(style)

    def update_category_display(self, category_name):
        self.category_name_label.setText(category_name if category_name else "未选择分类")
        self.file_list_widget.load_files(category_name)

    def add_file_to_category(self):
        if not self.main_window or not self.main_window.category_widget.current_category:
            QMessageBox.warning(self, "提示", "请先选择一个分类！")
            return
        
        category_name = self.main_window.category_widget.current_category
        
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择要添加的文件", "", "所有文件 (*.*)"
        )
        
        if file_paths:
            added_count = 0
            for file_path in file_paths:
                if self.category_manager.add_file_to_category(category_name, file_path):
                    added_count += 1
            
            if added_count > 0:
                self.file_list_widget.refresh_file_list()
                self.main_window.category_widget.status_label.setText(
                    f"已向 {category_name} 添加 {added_count} 个文件"
                )
            else:
                QMessageBox.information(self, "提示", "文件已存在或添加失败！")

    def rename_category(self):
        if not self.main_window or not self.main_window.category_widget.current_category:
            QMessageBox.warning(self, "提示", "请先选择一个分类！")
            return
        
        old_name = self.main_window.category_widget.current_category
        new_name, ok = QInputDialog.getText(
            self, "重命名分类", "请输入新名称：", QLineEdit.Normal, old_name
        )
        
        if ok and new_name.strip() and new_name.strip() != old_name:
            new_name = new_name.strip()
            if new_name in self.main_window.category_widget.categories:
                QMessageBox.warning(self, "提示", "分类名称已存在！")
                return
            
            if self.main_window.category_widget.category_manager.rename_category(old_name, new_name):
                categories = self.main_window.category_widget.categories
                index = categories.index(old_name)
                categories[index] = new_name
                self.main_window.category_widget.current_category = new_name
                self.main_window.category_widget.update_categories()
                self.update_category_display(new_name)
                self.main_window.category_widget.status_label.setText(f"已重命名为：{new_name}")
            else:
                QMessageBox.warning(self, "提示", "重命名分类文件失败！")

    def delete_category(self):
        if not self.main_window or not self.main_window.category_widget.current_category:
            QMessageBox.warning(self, "提示", "请先选择一个分类！")
            return
        
        name = self.main_window.category_widget.current_category
        
        data = self.category_manager.load_category_data(name)
        file_count = len(data.get('files', [])) if data else 0
        
        message = f"确定要删除分类\"{name}\"吗？\n"
        if file_count > 0:
            message += f"该分类包含 {file_count} 个文件，"
        message += "此操作会删除对应的JSON文件且不可恢复！"
        
        reply = QMessageBox.question(
            self, "确认删除", message, QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.main_window.category_widget.category_manager.delete_category(name):
                self.main_window.category_widget.categories.remove(name)
                self.main_window.category_widget.current_category = None
                self.main_window.category_widget.update_categories()
                self.update_category_display(None)
                self.main_window.category_widget.status_label.setText(f"已删除分类：{name}")
            else:
                QMessageBox.warning(self, "提示", "删除分类文件失败！")