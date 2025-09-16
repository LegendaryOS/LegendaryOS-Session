import os
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QComboBox, QScrollArea
from PySide6.QtCore import Qt
from terminal_widget import TerminalWidget

class NetworkConfig(QScrollArea):
    def __init__(self, parent=None):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        label = QLabel("Konfiguracja Internetu")
        label.setStyleSheet("font-size: 36px;")
        layout.addWidget(label)
        btn = QPushButton("Uruchom nmcli")
        btn.clicked.connect(self.config_network)
        layout.addWidget(btn)
        scan_btn = QPushButton("Skanuj Sieci WiFi")
        scan_btn.clicked.connect(self.scan_wifi)
        layout.addWidget(scan_btn)
        self.terminal = TerminalWidget()
        layout.addWidget(self.terminal)
        layout.addStretch()
        self.setWidget(widget)

    def config_network(self):
        self.terminal.run_command("nmcli")

    def scan_wifi(self):
        self.terminal.run_command("nmcli", ["device", "wifi", "list"])

class BluetoothConfig(QScrollArea):
    def __init__(self, parent=None):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        label = QLabel("Konfiguracja Bluetooth")
        label.setStyleSheet("font-size: 36px;")
        layout.addWidget(label)
        btn = QPushButton("Uruchom bluetoothctl")
        btn.clicked.connect(self.config_bluetooth)
        layout.addWidget(btn)
        self.terminal = TerminalWidget()
        layout.addWidget(self.terminal)
        layout.addStretch()
        self.setWidget(widget)

    def config_bluetooth(self):
        self.terminal.run_command("bluetoothctl")

class SoundConfig(QScrollArea):
    def __init__(self, parent=None):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        label = QLabel("Konfiguracja Dźwięku")
        label.setStyleSheet("font-size: 36px;")
        layout.addWidget(label)
        btn = QPushButton("Pokaż info pactl")
        btn.clicked.connect(self.config_sound)
        layout.addWidget(btn)
        self.terminal = TerminalWidget()
        layout.addWidget(self.terminal)

        volume_label = QLabel("Głośność")
        volume_label.setStyleSheet("font-size: 28px;")
        layout.addWidget(volume_label)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.volume_slider.setMinimumHeight(70)
        layout.addWidget(self.volume_slider)

        layout.addStretch()
        self.setWidget(widget)

    def config_sound(self):
        self.terminal.run_command("pactl info")

    def set_volume(self, value):
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{value}%"])

class BrightnessConfig(QScrollArea):
    def __init__(self, parent=None):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        label = QLabel("Konfiguracja Jasności")
        label.setStyleSheet("font-size: 36px;")
        layout.addWidget(label)

        self.bright_slider = QSlider(Qt.Horizontal)
        self.bright_slider.setRange(0, 100)
        self.bright_slider.setValue(50)
        self.bright_slider.valueChanged.connect(self.set_brightness)
        self.bright_slider.setMinimumHeight(70)
        layout.addWidget(self.bright_slider)

        layout.addStretch()
        self.setWidget(widget)

    def set_brightness(self, value):
        subprocess.run(["brightnessctl", "set", f"{value}%"])

class TimeConfig(QScrollArea):
    def __init__(self, parent=None):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        label = QLabel("Konfiguracja Czasu/Kraju/Miasta")
        label.setStyleSheet("font-size: 36px;")
        layout.addWidget(label)
        self.time_combo = QComboBox()
        self.time_combo.addItems([
            "Europe/Warsaw", "Europe/London", "Europe/Paris", "America/New_York",
            "America/Los_Angeles", "Asia/Tokyo", "Asia/Seoul", "Australia/Sydney",
            "Africa/Johannesburg", "America/Sao_Paulo", "Europe/Berlin", "Asia/Dubai"
        ])  # Added more for expansion
        layout.addWidget(self.time_combo)
        btn = QPushButton("Ustaw strefę czasową")
        btn.clicked.connect(self.config_time)
        layout.addWidget(btn)
        layout.addStretch()
        self.setWidget(widget)

    def config_time(self):
        timezone = self.time_combo.currentText()
        subprocess.run(["timedatectl", "set-timezone", timezone])

class UpdateConfig(QScrollArea):
    def __init__(self, parent=None):
        super().__init__()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        label = QLabel("Aktualizacja Systemu")
        label.setStyleSheet("font-size: 36px;")
        layout.addWidget(label)
        btn = QPushButton("Uruchom update-system")
        btn.clicked.connect(self.update_system)
        layout.addWidget(btn)
        self.terminal = TerminalWidget()
        layout.addWidget(self.terminal)
        layout.addStretch()
        self.setWidget(widget)

    def update_system(self):
        self.terminal.run_command("/usr/bin/update-system")
