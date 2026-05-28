"""主程序入口"""

import sys
from PySide6.QtWidgets import QApplication
from app.styles import get_style, get_palette_mode
from app.main_window import FileHelper

def main():
    app = QApplication(sys.argv)
    style = get_style(get_palette_mode(app))
    window = FileHelper(style)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()