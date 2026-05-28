"""工具函数"""

import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont, QPixmap, QPainter, QColor, QPen

def get_icon_path(icon_name):
    """获取图标文件路径"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 向上两级到项目根目录
    project_root = os.path.dirname(current_dir)
    assets_dir = os.path.join(project_root, "assets")
    return os.path.join(assets_dir, icon_name)

def get_file_extension(filename):
    """获取文件扩展名（不含点）"""
    _, ext = os.path.splitext(filename)
    return ext[1:].upper() if ext else "?"

def format_file_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def create_file_icon(extension, size=48):
    """创建带扩展名的文件图标"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    bg_color = QColor("#E2E8F0")
    border_color = QColor("#CBD5E1")
    
    painter.setPen(QPen(border_color, 2))
    painter.setBrush(bg_color)
    
    margin = 4
    body_rect = pixmap.rect().adjusted(margin, margin + 10, -margin, -margin)
    painter.drawRoundedRect(body_rect, 4, 4)
    
    fold_size = 14
    painter.setPen(QPen(border_color, 2))
    painter.setBrush(bg_color.darker(110))
    from PySide6.QtCore import QPoint
    painter.drawPolygon([body_rect.topRight() + QPoint(-fold_size, 0),
                         body_rect.topRight(),
                         body_rect.topRight() + QPoint(0, fold_size)])
    
    painter.setPen(QColor("#333"))
    font = QFont("Arial", 10, QFont.Bold)
    painter.setFont(font)
    
    display_text = extension[:4]
    text_rect = body_rect.adjusted(4, 16, -4, -4)
    painter.drawText(text_rect, Qt.AlignCenter, display_text)
    
    painter.end()
    return QIcon(pixmap)