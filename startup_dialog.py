"""
startup_dialog.py

LaserDAQ Startup Dialog

Allows the user to choose between
Simulation Mode and Hardware Mode.
"""

from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QGroupBox
)

from PyQt5.QtCore import Qt


class StartupDialog(QDialog):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("LaserDAQ")

        self.setFixedSize(400, 260)

        self.mode = "simulation"

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        # --------------------------
        # Title
        # --------------------------

        title = QLabel("LaserDAQ")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        subtitle = QLabel("Laser Characterization Software")

        subtitle.setAlignment(Qt.AlignCenter)

        layout.addWidget(subtitle)

        layout.addSpacing(15)

        # --------------------------
        # Mode Selection
        # --------------------------

        group = QGroupBox("Operating Mode")

        group_layout = QVBoxLayout()

        self.simRadio = QRadioButton("Simulation Mode")

        self.hwRadio = QRadioButton("Hardware Mode")

        self.simRadio.setChecked(True)

        group_layout.addWidget(self.simRadio)

        group_layout.addWidget(self.hwRadio)

        group.setLayout(group_layout)

        layout.addWidget(group)

        layout.addStretch()

        # --------------------------
        # Buttons
        # --------------------------

        button_layout = QHBoxLayout()

        start_button = QPushButton("Start")

        cancel_button = QPushButton("Exit")

        start_button.clicked.connect(self.start)

        cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()

        button_layout.addWidget(start_button)

        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def start(self):

        if self.simRadio.isChecked():

            self.mode = "simulation"

        else:

            self.mode = "hardware"

        self.accept()