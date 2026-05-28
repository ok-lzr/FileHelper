"""分类区控件"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, 
    QGridLayout, QInputDialog, QMessageBox, QLineEdit
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from ..utils import get_icon_path

class CategoryWidget(QWidget):
    def __init__(self, style, category_manager):
        super().__init__()
        self.style = style
        self.category_manager = category_manager
        self.categories = []
        self.initUI()
        self.load_categories_from_files()

    def initUI(self):
        style = self.style
        self.setStyleSheet(f"background: {style['background']}; color: {style['text']};")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(3)

        # 顶部：添加分类按钮
        self.add_button = QPushButton(" 添加分类")
        self.add_button.setFixedHeight(40)
        self.add_button.setIcon(QIcon(get_icon_path("add_category.svg")))
        self.add_button.setIconSize(QSize(20, 20))
        self.add_button.setStyleSheet(f"""
            QPushButton {{
                background: {style['add_btn_bg']};
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
                text-align: left;
                padding-left: 12px;
            }}
            QPushButton:hover {{
                background: {style['add_btn_bg_hover']};
            }}
            QPushButton:pressed {{
                background: {style['add_btn_bg_pressed']};
            }}
        """)
        self.add_button.clicked.connect(self.add_category)
        main_layout.addWidget(self.add_button)

        # 中间：分类展示区
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: 1px solid {style['file_border']};
                background: {style['background']};
            }}
            QScrollBar:vertical {{
                width: 10px;
                background: {style['background']};
            }}
            QScrollBar::handle:vertical {{
                background: {style['file_border']};
                border-radius: 5px;
            }}
        """)

        scroll_content = QWidget()
        self.category_grid = QGridLayout(scroll_content)
        self.category_grid.setContentsMargins(5, 5, 5, 5)
        self.category_grid.setSpacing(3)
        self.category_grid.setAlignment(Qt.AlignTop)

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area, 1)

        # 底部：状态栏
        self.status_label = QLabel("就绪")
        self.status_label.setFixedHeight(40)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(f"""
            QLabel {{
                background: {style['status_bg']};
                color: {style['status_fg']};
                border-radius: 3px;
                font-size: 12px;
                padding: 5px;
            }}
        """)
        main_layout.addWidget(self.status_label)

        self.category_buttons = []
        self.current_category = None
        self.main_window = None

    def load_categories_from_files(self):
        self.categories = self.category_manager.load_categories()
        self.update_categories()
        if self.categories:
            self.status_label.setText(f"已加载 {len(self.categories)} 个分类")

    def update_styles(self, style):
        self.style = style
        self.setStyleSheet(f"background: {style['background']}; color: {style['text']};")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                background: {style['status_bg']};
                color: {style['status_fg']};
                border-radius: 3px;
                font-size: 12px;
                padding: 5px;
            }}
        """)
        self.add_button.setStyleSheet(f"""
            QPushButton {{
                background: {style['add_btn_bg']};
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
                text-align: left;
                padding-left: 12px;
            }}
            QPushButton:hover {{
                background: {style['add_btn_bg_hover']};
            }}
            QPushButton:pressed {{
                background: {style['add_btn_bg_pressed']};
            }}
        """)
        self.update_categories()

    def add_category(self):
        name, ok = QInputDialog.getText(
            self, "添加分类", "请输入分类名称：", QLineEdit.Normal, ""
        )
        if ok and name.strip():
            name = name.strip()
            if name in self.categories:
                QMessageBox.warning(self, "提示", "分类名称已存在！")
                return
            
            if self.category_manager.create_category(name):
                self.categories.append(name)
                self.categories.sort()
                self.update_categories()
                self.status_label.setText(f"已添加分类：{name}")
                if self.main_window:
                    self.main_window.on_category_changed()
            else:
                QMessageBox.warning(self, "提示", "创建分类文件失败！")

    def update_categories(self):
        style = self.style
        for button in self.category_buttons:
            button.deleteLater()
        self.category_buttons.clear()
        
        for i, name in enumerate(self.categories):
            btn = QPushButton(f" {name}")
            btn.setFixedHeight(40)
            btn.setIcon(QIcon(get_icon_path("category.svg")))
            btn.setIconSize(QSize(20, 20))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {style['category_btn_bg']};
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 13px;
                    text-align: left;
                    padding-left: 12px;
                }}
                QPushButton:hover {{
                    background: {style['category_btn_bg_hover']};
                }}
                QPushButton:pressed {{
                    background: {style['category_btn_bg_pressed']};
                }}
            """)
            btn.clicked.connect(lambda checked, n=name: self.select_category(n))
            self.category_grid.addWidget(btn, i, 0)
            self.category_buttons.append(btn)
        
        if self.current_category and self.current_category in self.categories:
            self.select_category(self.current_category)

    def select_category(self, name):
        style = self.style
        self.current_category = name
        self.status_label.setText(f"当前分类：{name}")
        for btn in self.category_buttons:
            if btn.text().strip() == name:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {style['category_btn_bg_selected']};
                        color: white;
                        border: 2px solid {style['category_btn_border_selected']};
                        border-radius: 5px;
                        font-size: 13px;
                        text-align: left;
                        padding-left: 12px;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {style['category_btn_bg']};
                        color: white;
                        border: none;
                        border-radius: 5px;
                        font-size: 13px;
                        text-align: left;
                        padding-left: 12px;
                    }}
                    QPushButton:hover {{
                        background: {style['category_btn_bg_hover']};
                    }}
                """)
        if self.main_window:
            self.main_window.on_category_selected(name)