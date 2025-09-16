import os
import sys
import subprocess
from urllib.request import urlopen
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QFocusFrame, QProgressBar, QTabWidget
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QIcon, QPixmap, QColor, QImage
from terminal_widget import TerminalWidget
from config_pages import (NetworkConfig, BluetoothConfig, SoundConfig, BrightnessConfig, TimeConfig, UpdateConfig)
from styles import get_stylesheet

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LegendaryOS Session")
        self.showFullScreen()
        self.setStyleSheet(get_stylesheet())
        # Enable focus policy for gamepad/keyboard navigation
        self.setFocusPolicy(Qt.StrongFocus)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # Sidebar for navigation, wider for Steam-like feel
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar.setFixedWidth(450)
        sidebar.setStyleSheet("background-color: #1B2838; border-right: 8px solid #2A475E;")
        title_label = QLabel("LegendaryOS Session")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 42px; color: #66C0F4; border-bottom: 8px solid #2A475E; padding: 35px;")
        sidebar_layout.addWidget(title_label)
        self.home_btn = QPushButton(QIcon(self.create_pixel_icon("#FFFFFF")), "Strona Główna")
        self.home_btn.clicked.connect(self.show_home)
        self.home_btn.setFocusPolicy(Qt.StrongFocus)
        sidebar_layout.addWidget(self.home_btn)
        self.settings_btn = QPushButton(QIcon(self.create_pixel_icon("#66C0F4")), "Ustawienia")
        self.settings_btn.clicked.connect(self.show_settings)
        self.settings_btn.setFocusPolicy(Qt.StrongFocus)
        sidebar_layout.addWidget(self.settings_btn)
        self.launchers_btn = QPushButton(QIcon(self.create_pixel_icon("#00FF00")), "Launchery")
        self.launchers_btn.clicked.connect(self.show_launchers)
        self.launchers_btn.setFocusPolicy(Qt.StrongFocus)
        sidebar_layout.addWidget(self.launchers_btn)
        self.legendary_btn = QPushButton(QIcon(self.create_pixel_icon("#FF00FF")), "Legendary Menu")
        self.legendary_btn.clicked.connect(self.show_legendary_menu)
        self.legendary_btn.setFocusPolicy(Qt.StrongFocus)
        sidebar_layout.addWidget(self.legendary_btn)
        sidebar_layout.addStretch()
        # Add version footer
        version_label = QLabel("v1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("font-size: 18px; color: #C7D5E0; padding: 10px;")
        sidebar_layout.addWidget(version_label)
        main_layout.addWidget(sidebar)
        # Content area container
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        # Header for logo
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        logo_label = QLabel()
        logo_path = "/usr/share/LegendaryOS/Icons/LegendaryOS-nobackground.png"
        logo_pixmap = QPixmap(logo_path)
        if logo_pixmap.isNull():
            logo_pixmap = QPixmap(100, 100)  # Fallback empty pixmap
            logo_pixmap.fill(Qt.transparent)
        logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setStyleSheet("padding: 10px;")
        header_layout.addWidget(logo_label)
        content_layout.addLayout(header_layout)
        # Content stack
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #0F1E2B;")
        content_layout.addWidget(self.content_stack)
        main_layout.addWidget(content_container)
        # Home page enhanced
        self.home_page = self.create_home_page()
        self.content_stack.addWidget(self.home_page)
        # Settings page
        self.settings_page = self.create_settings_page()
        self.content_stack.addWidget(self.settings_page)
        # Launchers page
        self.launchers_page = self.create_launchers_page()
        self.content_stack.addWidget(self.launchers_page)
        # Legendary menu page
        self.legendary_page = self.create_legendary_page()
        self.content_stack.addWidget(self.legendary_page)
        # Progress bar for loading/operations
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("QProgressBar { background-color: #1B2838; border: 4px solid #2A475E; height: 20px; } QProgressBar::chunk { background-color: #66C0F4; }")
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.hide()
        self.statusBar().addWidget(self.progress_bar, 1)
        # Focus frame
        self.focus_frame = QFocusFrame(self)
        self.focus_frame.setWidget(self)

    def create_pixel_icon(self, color):
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(color))
        return pixmap

    def load_pixmap_from_url(self, url):
        try:
            data = urlopen(url).read()
            image = QImage.fromData(data)
            pixmap = QPixmap.fromImage(image)
            if pixmap.isNull():
                pixmap = QPixmap(64, 64)
                pixmap.fill(Qt.transparent)
            return pixmap
        except Exception as e:
            print(f"Error loading image from {url}: {e}")
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.transparent)
            return pixmap

    def create_home_page(self):
        home_page = QWidget()
        home_layout = QVBoxLayout(home_page)
        home_layout.setContentsMargins(60, 60, 60, 60)
        home_layout.setSpacing(20)
        welcome_label = QLabel("Witaj w LegendaryOS Session!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 40px; color: #EBEBEB;")
        home_layout.addWidget(welcome_label)
        sub_label = QLabel("Konfiguruj system z łatwością za pomocą gamepada lub klawiatury.")
        sub_label.setAlignment(Qt.AlignCenter)
        sub_label.setStyleSheet("font-size: 26px; color: #66C0F4;")
        home_layout.addWidget(sub_label)
        # Enhanced pixel art with fixed escape sequences using raw string
        ascii_art = QLabel(r"""
 .--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--.
/ .. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \
\ \/\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ \/ /
 \/ /`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'\/ /
 / /\                                                                                                        / /\
/ /\ \                                                                                                      / /\ \
\ \/ /                                                                                                      \ \/ /
 \/ /                                                                                                        \/ /
 / /\      ██▓    ▓█████   ▄████ ▓█████  ███▄    █ ▓█████▄  ▄▄▄       ██▀███ ▓██   ██▓ ▒█████    ██████      / /\
/ /\ \    ▓██▒    ▓█   ▀  ██▒ ▀█▒▓█   ▀  ██ ▀█   █ ▒██▀ ██▌▒████▄    ▓██ ▒ ██▒▒██  ██▒▒██▒  ██▒▒██    ▒     / /\ \
\ \/ /    ▒██░    ▒███   ▒██░▄▄▄░▒███   ▓██  ▀█ ██▒░██   █▌▒██  ▀█▄  ▓██ ░▄█ ▒ ▒██ ██░▒██░  ██▒░ ▓██▄       \ \/ /
 \/ /     ▒██░    ▒▓█  ▄ ░▓█  ██▓▒▓█  ▄ ▓██▒  ▐▌██▒░▓█▄   ▌░██▄▄▄▄██ ▒██▀▀█▄   ░ ▐██▓░▒██   ██░  ▒   ██▒     \/ /
 / /\     ░██████▒░▒████▒░▒▓███▀▒░▒████▒▒██░   ▓██░░▒████▓  ▓█   ▓██▒░██▓ ▒██▒ ░ ██▒▓░░ ████▓▒░▒██████▒▒     / /\
/ /\ \    ░ ▒░▓  ░░░ ▒░ ░ ░▒   ▒ ░░ ▒░ ░░ ▒░   ▒ ▒  ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░  ██▒▒▒ ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░    / /\ \
\ \/ /    ░ ░ ▒  ░ ░ ░  ░  ░   ░  ░ ░  ░░ ░░   ░ ▒░ ░ ▒  ▒   ▒   ▒▒ ░  ░▒ ░ ▒░▓██ ░▒░   ░ ▒ ▒░ ░ ░▒  ░ ░    \ \/ /
 \/ /       ░ ░      ░   ░ ░   ░    ░      ░   ░ ░  ░ ░  ░   ░   ▒     ░░   ░ ▒ ▒ ░░  ░ ░ ░ ▒  ░  ░  ░       \/ /
 / /\         ░  ░   ░  ░      ░    ░  ░         ░    ░          ░  ░   ░     ░ ░         ░ ░        ░       / /\
/ /\ \                                              ░                         ░ ░                           / /\ \
\ \/ /      ██████ ▓█████   ██████   ██████  ██▓ ▒█████   ███▄    █                                         \ \/ /
 \/ /     ▒██    ▒ ▓█   ▀ ▒██    ▒ ▒██    ▒ ▓██▒▒██▒  ██▒ ██ ▀█   █                                          \/ /
 / /\     ░ ▓██▄   ▒███   ░ ▓██▄   ░ ▓██▄   ▒██▒▒██░  ██▒▓██  ▀█ ██▒                                         / /\
/ /\ \      ▒   ██▒▒▓█  ▄   ▒   ██▒  ▒   ██▒░██░▒██   ██░▓██▒  ▐▌██▒                                        / /\ \
\ \/ /    ▒██████▒▒░▒████▒▒██████▒▒▒██████▒▒░██░░ ████▓▒░▒██░   ▓██░                                        \ \/ /
 \/ /     ▒ ▒▓▒ ▒ ░░░ ▒░ ░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░░▓  ░ ▒░▒░▒░ ░ ▒░   ▒ ▒                                          \/ /
 / /\     ░ ░▒  ░ ░ ░ ░  ░░ ░▒  ░ ░░ ░▒  ░ ░ ▒ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░                                         / /\
/ /\ \    ░  ░  ░     ░   ░  ░  ░  ░  ░  ░   ▒ ░░ ░ ░ ▒     ░   ░ ░                                         / /\ \
\ \/ /          ░     ░  ░      ░        ░   ░      ░ ░           ░                                         \ \/ /
 \/ /                                                                                                        \/ /
 / /\                                                                                                        / /\
/ /\ \                                                                                                      / /\ \
\ \/ /                                                                                                      \ \/ /
 \/ /                                                                                                        \/ /
 / /\.--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--..--./ /\
/ /\ \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \/\ \
\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `' /
 `--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'
        """)
        ascii_art.setAlignment(Qt.AlignCenter)
        ascii_art.setStyleSheet("font-family: monospace; color: #2A475E; background-color: #1B2838; padding: 25px; border: 8px solid #66C0F4; border-radius: 0px;")
        home_layout.addWidget(ascii_art)
        home_layout.addStretch()
        return home_page

    def create_settings_page(self):
        settings_page = QTabWidget()
        settings_page.setStyleSheet("QTabWidget { background-color: #0F1E2B; } QTabBar { font-size: 26px; }")
        settings_page.addTab(NetworkConfig(self), "Sieć")
        settings_page.addTab(BluetoothConfig(self), "Bluetooth")
        settings_page.addTab(SoundConfig(self), "Dźwięk")
        settings_page.addTab(BrightnessConfig(self), "Jasność")
        settings_page.addTab(TimeConfig(self), "Czas")
        settings_page.addTab(UpdateConfig(self), "Aktualizacja")
        return settings_page

    def create_launchers_page(self):
        launchers_page = QWidget()
        launchers_layout = QVBoxLayout(launchers_page)
        launchers_layout.setContentsMargins(60, 60, 60, 60)
        launchers_layout.setSpacing(30)
        launchers_label = QLabel("Launchery")
        launchers_label.setAlignment(Qt.AlignCenter)
        launchers_label.setStyleSheet("font-size: 40px; color: #EBEBEB;")
        launchers_layout.addWidget(launchers_label)
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(50)
        # Use local fallback icons to avoid HTTP 403 errors
        lutris_pixmap = QPixmap(64, 64)
        lutris_pixmap.fill(Qt.transparent)  # Fallback icon
        lutris_btn = QPushButton(QIcon(lutris_pixmap), "Lutris")
        lutris_btn.setIconSize(QSize(64, 64))
        lutris_btn.clicked.connect(self.launch_lutris)
        lutris_btn.setMinimumWidth(350)
        grid_layout.addWidget(lutris_btn)
        heroic_pixmap = QPixmap(64, 64)
        heroic_pixmap.fill(Qt.transparent)
        heroic_btn = QPushButton(QIcon(heroic_pixmap), "Heroic Games")
        heroic_btn.setIconSize(QSize(64, 64))
        heroic_btn.clicked.connect(self.launch_heroic)
        heroic_btn.setMinimumWidth(350)
        grid_layout.addWidget(heroic_btn)
        steam_pixmap = QPixmap(64, 64)
        steam_pixmap.fill(Qt.transparent)
        steam_btn = QPushButton(QIcon(steam_pixmap), "Steam")
        steam_btn.setIconSize(QSize(64, 64))
        steam_btn.clicked.connect(self.launch_steam)
        steam_btn.setMinimumWidth(350)
        grid_layout.addWidget(steam_btn)
        brave_pixmap = QPixmap(64, 64)
        brave_pixmap.fill(Qt.transparent)
        brave_btn = QPushButton(QIcon(brave_pixmap), "Brave")
        brave_btn.setIconSize(QSize(64, 64))
        brave_btn.clicked.connect(self.launch_brave)
        brave_btn.setMinimumWidth(350)
        grid_layout.addWidget(brave_btn)
        launchers_layout.addLayout(grid_layout)
        launchers_layout.addStretch()
        return launchers_page

    def create_legendary_page(self):
        legendary_page = QWidget()
        legendary_layout = QVBoxLayout(legendary_page)
        legendary_layout.setContentsMargins(60, 60, 60, 60)
        legendary_layout.setSpacing(30)
        legendary_label = QLabel("Legendary Menu")
        legendary_label.setAlignment(Qt.AlignCenter)
        legendary_label.setStyleSheet("font-size: 40px; color: #EBEBEB;")
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
        return legendary_page

    def show_page_with_animation(self, page):
        self.content_stack.setCurrentWidget(page)
        self.progress_bar.show()
        QTimer.singleShot(500, self.progress_bar.hide)

    def show_home(self):
        self.show_page_with_animation(self.home_page)

    def show_settings(self):
        self.show_page_with_animation(self.settings_page)

    def show_launchers(self):
        self.show_page_with_animation(self.launchers_page)

    def show_legendary_menu(self):
        self.show_page_with_animation(self.legendary_page)

    def launch_lutris(self):
        self.progress_bar.show()
        QTimer.singleShot(1000, lambda: [self.close(), subprocess.run(["cage", "lutris"]), self.progress_bar.hide()])

    def launch_heroic(self):
        self.progress_bar.show()
        QTimer.singleShot(1000, lambda: [self.close(), subprocess.run(["cage", "flatpak", "run", "com.heroicgameslauncher.hgl"]), self.progress_bar.hide()])

    def launch_steam(self):
        self.progress_bar.show()
        QTimer.singleShot(1000, lambda: [self.close(), subprocess.run(["gamescope-session-plus", "steam"]), self.progress_bar.hide()])

    def launch_brave(self):
        self.progress_bar.show()
        QTimer.singleShot(1000, lambda: [self.close(), subprocess.run(["cage", "brave"]), self.progress_bar.hide()])

    def shutdown(self):
        self.progress_bar.show()
        QTimer.singleShot(1000, lambda: [subprocess.run(["sudo", "shutdown", "0"]), self.progress_bar.hide()])

    def reboot(self):
        self.progress_bar.show()
        QTimer.singleShot(1000, lambda: [subprocess.run(["sudo", "reboot"]), self.progress_bar.hide()])

    def restart_app(self):
        self.progress_bar.show()
        QTimer.singleShot(1000, lambda: [self.close(), os.execl(sys.executable, sys.executable, *sys.argv), self.progress_bar.hide()])
