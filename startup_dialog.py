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
    QGroupBox,
    QSizePolicy
)

from PyQt5.QtCore import Qt


class StartupDialog(QDialog):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("LaserDAQ")

        # Larger window
        self.resize(450, 260)
        self.setMinimumSize(420, 240)

        self.mode = "simulation"

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # --------------------------------
        # Title
        # --------------------------------

        title = QLabel("LaserDAQ")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        subtitle = QLabel("Laser Characterization Software")

        subtitle.setAlignment(Qt.AlignCenter)

        subtitle.setStyleSheet("""
            font-size:11pt;
        """)

        layout.addWidget(subtitle)

        # --------------------------------
        # Operating Mode
        # --------------------------------

        group = QGroupBox("Operating Mode")

        group_layout = QVBoxLayout()

        group_layout.setContentsMargins(12, 12, 12, 12)
        group_layout.setSpacing(10)

        self.simRadio = QRadioButton("Simulation Mode")

        self.hwRadio = QRadioButton("Hardware Mode")

        self.simRadio.setChecked(True)

        self.simRadio.setMinimumHeight(28)
        self.hwRadio.setMinimumHeight(28)

        group_layout.addWidget(self.simRadio)
        group_layout.addWidget(self.hwRadio)

        group.setLayout(group_layout)

        group.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        layout.addWidget(group)

        layout.addStretch()

        # --------------------------------
        # Buttons
        # --------------------------------

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        start_button = QPushButton("Start")
        exit_button = QPushButton("Exit")

        start_button.setMinimumSize(120, 36)
        exit_button.setMinimumSize(120, 36)

        start_button.clicked.connect(self.start)
        exit_button.clicked.connect(self.reject)

        button_layout.addWidget(start_button)
        button_layout.addSpacing(10)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def start(self):

        if self.simRadio.isChecked():

            self.mode = "simulation"

        else:

            self.mode = "hardware"

        self.accept()