import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QTextEdit, QLineEdit, QComboBox, QSlider, QTabWidget, QScrollArea
from PySide6.QtCore import QProcess, Qt
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor

class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: #001000; color: #00FF00; border: 4px solid #008000; font-family: 'Courier New'; font-size: 14px;")
        self.layout.addWidget(self.output)
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)

    def run_command(self, command):
        self.output.clear()
        self.process.start(command)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.output.append(stdout)

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.output.append(stderr)

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pixel Art Config App")
        self.showFullScreen()
        
        # Enhanced pixel art style with more vibrant colors and blocky feel
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0A0A0A;
            }
            QWidget {
                color: #FFFFFF;
                font-family: 'Courier New', monospace;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #404040;
                border: 4px solid #808080;
                color: #00FF00;
                padding: 15px;
                border-radius: 0px;  /* Blocky */
            }
            QPushButton:hover {
                background-color: #606060;
                border: 4px solid #00FF00;
            }
            QLabel {
                color: #00FFFF;
                font-size: 24px;
            }
            QTextEdit {
                background-color: #101010;
                color: #FFFF00;
                border: 4px solid #808080;
            }
            QComboBox {
                background-color: #202020;
                border: 4px solid #808080;
                color: #00FF00;
                padding: 10px;
            }
            QSlider::groove:horizontal {
                border: 2px solid #808080;
                height: 20px;
                background: #404040;
            }
            QSlider::handle:horizontal {
                background: #00FF00;
                border: 4px solid #008000;
                width: 40px;
                margin: -10px 0;
            }
            QTabWidget::pane {
                border: 4px solid #808080;
                background-color: #101010;
            }
            QTabBar::tab {
                background-color: #404040;
                color: #00FF00;
                padding: 15px;
                border: 4px solid #808080;
                border-bottom: 0px;
            }
            QTabBar::tab:selected {
                background-color: #606060;
                border: 4px solid #00FF00;
            }
            QScrollArea {
                border: 4px solid #808080;
                background-color: #0A0A0A;
            }
        """)
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Sidebar for navigation
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("background-color: #202020; border-right: 4px solid #808080;")
        
        title_label = QLabel("Pixel Config")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 32px; color: #FF00FF; border-bottom: 4px solid #808080; padding: 20px;")
        sidebar_layout.addWidget(title_label)
        
        home_btn = QPushButton("Strona Główna")
        home_btn.clicked.connect(self.show_home)
        sidebar_layout.addWidget(home_btn)
        
        settings_btn = QPushButton("Ustawienia")
        settings_btn.clicked.connect(self.show_settings)
        sidebar_layout.addWidget(settings_btn)
        
        launchers_btn = QPushButton("Launchery")
        launchers_btn.clicked.connect(self.show_launchers)
        sidebar_layout.addWidget(launchers_btn)
        
        legendary_btn = QPushButton("Legendary Menu")
        legendary_btn.clicked.connect(self.show_legendary_menu)
        sidebar_layout.addWidget(legendary_btn)
        
        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)
        
        # Content area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # Home page
        self.home_page = QWidget()
        home_layout = QVBoxLayout(self.home_page)
        welcome_label = QLabel("Witaj w Pixel Config App!\nWybierz sekcję z menu po lewej.")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 28px; color: #00FFFF;")
        home_layout.addWidget(welcome_label)
        
        # Add some pixel art feel with ASCII art
        ascii_art = QLabel("""
        ##########
        #        #
        #  PIXEL #
        #  CONFIG#
        #        #
        ##########
        """)
        ascii_art.setAlignment(Qt.AlignCenter)
        ascii_art.setStyleSheet("font-family: monospace; color: #FFFF00;")
        home_layout.addWidget(ascii_art)
        
        home_layout.addStretch()
        self.content_stack.addWidget(self.home_page)
        
        # Settings page with tabs for better organization
        self.settings_page = QTabWidget()
        self.settings_page.setStyleSheet("QTabWidget { background-color: #101010; }")
        
        # Tab 1: Network
        net_tab = QScrollArea()
        net_widget = QWidget()
        net_layout = QVBoxLayout(net_widget)
        net_label = QLabel("Konfiguracja Internetu")
        net_layout.addWidget(net_label)
        net_btn = QPushButton("Uruchom nmcli")
        net_btn.clicked.connect(self.config_network)
        net_layout.addWidget(net_btn)
        self.net_terminal = TerminalWidget()
        net_layout.addWidget(self.net_terminal)
        net_layout.addStretch()
        net_tab.setWidget(net_widget)
        self.settings_page.addTab(net_tab, "Sieć")
        
        # Tab 2: Bluetooth
        bt_tab = QScrollArea()
        bt_widget = QWidget()
        bt_layout = QVBoxLayout(bt_widget)
        bt_label = QLabel("Konfiguracja Bluetooth")
        bt_layout.addWidget(bt_label)
        bt_btn = QPushButton("Uruchom bluetoothctl")
        bt_btn.clicked.connect(self.config_bluetooth)
        bt_layout.addWidget(bt_btn)
        self.bt_terminal = TerminalWidget()
        bt_layout.addWidget(self.bt_terminal)
        bt_layout.addStretch()
        bt_tab.setWidget(bt_widget)
        self.settings_page.addTab(bt_tab, "Bluetooth")
        
        # Tab 3: Sound
        sound_tab = QScrollArea()
        sound_widget = QWidget()
        sound_layout = QVBoxLayout(sound_widget)
        sound_label = QLabel("Konfiguracja Dźwięku")
        sound_layout.addWidget(sound_label)
        sound_btn = QPushButton("Pokaż info pactl")
        sound_btn.clicked.connect(self.config_sound)
        sound_layout.addWidget(sound_btn)
        self.sound_terminal = TerminalWidget()
        sound_layout.addWidget(self.sound_terminal)
        
        # Expanded: Add volume slider
        volume_label = QLabel("Głośność")
        sound_layout.addWidget(volume_label)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)  # Default
        self.volume_slider.valueChanged.connect(self.set_volume)
        sound_layout.addWidget(self.volume_slider)
        
        sound_layout.addStretch()
        sound_tab.setWidget(sound_widget)
        self.settings_page.addTab(sound_tab, "Dźwięk")
        
        # Tab 4: Brightness
        bright_tab = QScrollArea()
        bright_widget = QWidget()
        bright_layout = QVBoxLayout(bright_widget)
        bright_label = QLabel("Konfiguracja Jasności")
        bright_layout.addWidget(bright_label)
        
        # Use slider for brightness
        self.bright_slider = QSlider(Qt.Horizontal)
        self.bright_slider.setRange(0, 100)
        self.bright_slider.setValue(50)  # Default
        self.bright_slider.valueChanged.connect(self.set_brightness)
        bright_layout.addWidget(self.bright_slider)
        
        bright_layout.addStretch()
        bright_tab.setWidget(bright_widget)
        self.settings_page.addTab(bright_tab, "Jasność")
        
        # Tab 5: Time/Location
        time_tab = QScrollArea()
        time_widget = QWidget()
        time_layout = QVBoxLayout(time_widget)
        time_label = QLabel("Konfiguracja Czasu/Kraju/Miasta")
        time_layout.addWidget(time_label)
        self.time_combo = QComboBox()
        # Expanded: More timezones
        self.time_combo.addItems([
            "Europe/Warsaw", "Europe/London", "Europe/Paris", "America/New_York", 
            "America/Los_Angeles", "Asia/Tokyo", "Asia/Seoul", "Australia/Sydney",
            "Africa/Johannesburg", "America/Sao_Paulo"
        ])
        time_layout.addWidget(self.time_combo)
        time_btn = QPushButton("Ustaw strefę czasową")
        time_btn.clicked.connect(self.config_time)
        time_layout.addWidget(time_btn)
        time_layout.addStretch()
        time_tab.setWidget(time_widget)
        self.settings_page.addTab(time_tab, "Czas")
        
        # Tab 6: Update
        update_tab = QScrollArea()
        update_widget = QWidget()
        update_layout = QVBoxLayout(update_widget)
        update_label = QLabel("Aktualizacja Systemu")
        update_layout.addWidget(update_label)
        update_btn = QPushButton("Uruchom update-system")
        update_btn.clicked.connect(self.update_system)
        update_layout.addWidget(update_btn)
        self.update_terminal = TerminalWidget()
        update_layout.addWidget(self.update_terminal)
        update_layout.addStretch()
        update_tab.setWidget(update_widget)
        self.settings_page.addTab(update_tab, "Aktualizacja")
        
        self.content_stack.addWidget(self.settings_page)
        
        # Launchers page - grid for better look
        self.launchers_page = QWidget()
        launchers_layout = QVBoxLayout(self.launchers_page)
        launchers_label = QLabel("Launchery")
        launchers_label.setAlignment(Qt.AlignCenter)
        launchers_layout.addWidget(launchers_label)
        
        grid_layout = QHBoxLayout()
        lutris_btn = QPushButton("Lutris")
        lutris_btn.clicked.connect(self.launch_lutris)
        grid_layout.addWidget(lutris_btn)
        
        heroic_btn = QPushButton("Heroic Games")
        heroic_btn.clicked.connect(self.launch_heroic)
        grid_layout.addWidget(heroic_btn)
        
        steam_btn = QPushButton("Steam")
        steam_btn.clicked.connect(self.launch_steam)
        grid_layout.addWidget(steam_btn)
        
        brave_btn = QPushButton("Brave")
        brave_btn.clicked.connect(self.launch_brave)
        grid_layout.addWidget(brave_btn)
        
        launchers_layout.addLayout(grid_layout)
        launchers_layout.addStretch()
        self.content_stack.addWidget(self.launchers_page)
        
        # Legendary menu page
        self.legendary_page = QWidget()
        legendary_layout = QVBoxLayout(self.legendary_page)
        legendary_label = QLabel("Legendary Menu")
        legendary_label.setAlignment(Qt.AlignCenter)
        legendary_layout.addWidget(legendary_label)
        
        shutdown_btn = QPushButton("Wyłącz Komputer")
        shutdown_btn.clicked.connect(self.shutdown)
        legendary_layout.addWidget(shutdown_btn)
        
        reboot_btn = QPushButton("Uruchom Ponownie Komputer")
        reboot_btn.clicked.connect(self.reboot)
        legendary_layout.addWidget(reboot_btn)
        
        restart_app_btn = QPushButton("Uruchom Ponownie Aplikację")
        restart_app_btn.clicked.connect(self.restart_app)
        legendary_layout.addWidget(restart_app_btn)
        
        legendary_layout.addStretch()
        self.content_stack.addWidget(self.legendary_page)

    def show_home(self):
        self.content_stack.setCurrentWidget(self.home_page)
    
    def show_settings(self):
        self.content_stack.setCurrentWidget(self.settings_page)
    
    def show_launchers(self):
        self.content_stack.setCurrentWidget(self.launchers_page)
    
    def show_legendary_menu(self):
        self.content_stack.setCurrentWidget(self.legendary_page)
    
    def config_network(self):
        self.net_terminal.run_command("nmcli")
    
    def config_bluetooth(self):
        self.bt_terminal.run_command("bluetoothctl")
    
    def config_sound(self):
        self.sound_terminal.run_command("pactl info")
    
    def set_volume(self, value):
        os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {value}%")
    
    def set_brightness(self, value):
        os.system(f"brightnessctl set {value}%")
    
    def config_time(self):
        timezone = self.time_combo.currentText()
        os.system(f"timedatectl set-timezone {timezone}")
    
    def update_system(self):
        self.update_terminal.run_command("/usr/bin/update-system")
    
    def launch_lutris(self):
        self.close()
        os.system("cage lutris")
    
    def launch_heroic(self):
        self.close()
        os.system('cage "flatpak run com.heroicgameslauncher.hgl"')
    
    def launch_steam(self):
        self.close()
        os.system("gamescope-session-plus steam")
    
    def launch_brave(self):
        self.close()
        os.system("cage brave")
    
    def shutdown(self):
        os.system("sudo shutdown 0")
    
    def reboot(self):
        os.system("sudo reboot")
    
    def restart_app(self):
        self.close()
        os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Set font for pixel feel
    font = QFont("Courier New", 14)
    app.setFont(font)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
