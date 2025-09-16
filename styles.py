def get_stylesheet():
    return """
            QMainWindow {
                background-color: #0F1E2B;  /* Dark blue-grey like Steam */
            }
            QWidget {
                color: #C7D5E0;  /* Light text */
                font-family: 'Courier New', monospace;
                font-size: 22px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #1B2838;  /* Steam dark panel */
                border: 8px solid #2A475E;  /* Thicker blocky pixel border */
                color: #66C0F4;  /* Steam blue text */
                padding: 25px;
                border-radius: 0px;  /* Sharp corners */
                min-height: 70px;  /* Larger for gamepad */
            }
            QPushButton:hover, QPushButton:focus {
                background-color: #2A475E;
                border: 8px solid #66C0F4;  /* Highlight */
                color: #FFFFFF;
            }
            QPushButton:pressed {
                background-color: #66C0F4;
                color: #1B2838;
            }
            QLabel {
                color: #66C0F4;  /* Steam accent */
                font-size: 30px;
                padding: 5px;  /* Improved padding */
            }
            QTextEdit {
                background-color: #0F1E2B;
                color: #C7D5E0;
                border: 8px solid #2A475E;
            }
            QComboBox {
                background-color: #1B2838;
                border: 8px solid #2A475E;
                color: #66C0F4;
                padding: 20px;
                min-height: 60px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 40px;
                border-left-width: 1px;
                border-left-color: #2A475E;
                border-left-style: solid;
            }
            QSlider::groove:horizontal {
                border: 6px solid #2A475E;
                height: 40px;
                background: #1B2838;
            }
            QSlider::handle:horizontal {
                background: #66C0F4;
                border: 8px solid #2A475E;
                width: 80px;
                margin: -20px 0;
            }
            QTabWidget::pane {
                border: 8px solid #2A475E;
                background-color: #0F1E2B;
            }
            QTabBar::tab {
                background-color: #1B2838;
                color: #66C0F4;
                padding: 25px;
                border: 8px solid #2A475E;
                border-bottom: 0px;
                min-width: 180px;
            }
            QTabBar::tab:selected {
                background-color: #2A475E;
                border: 8px solid #66C0F4;
                color: #FFFFFF;
            }
            QScrollArea {
                border: 8px solid #2A475E;
                background-color: #0F1E2B;
            }
            QFocusFrame {
                border: 6px dashed #66C0F4;  /* Gamepad focus */
            }
            QProgressBar {
                background-color: #1B2838;
                border: 6px solid #2A475E;
                height: 30px;
                text-align: center;
                color: #FFFFFF;
            }
            QProgressBar::chunk {
                background-color: #66C0F4;
            }
        """
