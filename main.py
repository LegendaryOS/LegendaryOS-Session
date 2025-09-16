import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QColor, QPalette
from app import MainApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Courier New", 16)
    app.setFont(font)
    # Set palette for overall theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#0F1E2B"))
    palette.setColor(QPalette.WindowText, QColor("#C7D5E0"))
    app.setPalette(palette)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
