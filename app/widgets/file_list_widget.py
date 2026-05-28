"""文件列表滚动区域"""

from PySide6.QtWidgets import (
    QScrollArea, QVBoxLayout, QLabel, QWidget
)
from PySide6.QtCore import Qt

from .file_item_widget import FileItemWidget

class FileListWidget(QScrollArea):
    def __init__(self, style, category_manager, file_info_widget):
        super().__init__()
        self.style = style
        self.category_manager = category_manager
        self.file_info_widget = file_info_widget
        self.current_files = []
        self.current_category = None
        self.file_widgets = []
        self.selected_item = None
        self.initUI()
        
    def initUI(self):
        style = self.style
        self.setWidgetResizable(True)
        self.setStyleSheet(f"""
            QScrollArea {{
                background: {style['file_bg']};
                border: 1px solid {style['file_border']};
                border-radius: 3px;
            }}
            QScrollBar:vertical {{
                width: 10px;
                background: {style['file_bg']};
            }}
            QScrollBar::handle:vertical {{
                background: {style['file_border']};
                border-radius: 5px;
            }}
        """)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        self.content_layout.setSpacing(5)
        self.content_layout.setAlignment(Qt.AlignTop)
        
        self.empty_label = QLabel("暂无文件，请点击\"添加文件\"按钮添加")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet(f"""
            QLabel {{
                color: {style['file_path_fg']};
                font-size: 14px;
                padding: 20px;
                border: none;
                background: transparent;
            }}
        """)
        self.content_layout.addWidget(self.empty_label)
        
        self.setWidget(self.content_widget)
    
    def update_styles(self, style):
        """更新样式"""
        self.style = style
        self.setStyleSheet(f"""
            QScrollArea {{
                background: {style['file_bg']};
                border: 1px solid {style['file_border']};
                border-radius: 3px;
            }}
            QScrollBar:vertical {{
                width: 10px;
                background: {style['file_bg']};
            }}
            QScrollBar::handle:vertical {{
                background: {style['file_border']};
                border-radius: 5px;
            }}
        """)
        self.empty_label.setStyleSheet(f"""
            QLabel {{
                color: {style['file_path_fg']};
                font-size: 14px;
                padding: 20px;
                border: none;
                background: transparent;
            }}
        """)
    
    def load_files(self, category_name):
        self.current_category = category_name
        self.selected_item = None
        self.clear_files()
        
        if category_name:
            data = self.category_manager.load_category_data(category_name)
            if data and 'files' in data:
                self.current_files = data['files']
        
        self.update_display()
        self.file_info_widget.clear_info()
    
    def clear_files(self):
        for widget in self.file_widgets:
            widget.deleteLater()
        self.file_widgets.clear()
        self.empty_label.hide()
    
    def update_display(self):
        self.clear_files()
        
        if not self.current_files:
            self.empty_label.show()
        else:
            self.empty_label.hide()
            for file_info in self.current_files:
                file_widget = FileItemWidget(
                    file_info, self.style, self.current_category, 
                    self.category_manager, self
                )
                self.content_layout.addWidget(file_widget)
                self.file_widgets.append(file_widget)
    
    def select_file_item(self, item):
        if self.selected_item:
            self.selected_item.set_selected(False)
        
        self.selected_item = item
        item.set_selected(True)
        
        self.file_info_widget.display_file_info(item.file_info)
    
    def refresh_file_list(self):
        if self.current_category:
            self.load_files(self.current_category)