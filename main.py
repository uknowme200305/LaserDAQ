import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import random
from PyQt5.QtCore import QTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        uic.loadUi("test_gpt1.ui", self)

        # Connect button click to function
        self.readCurrentButton.clicked.connect(self.say_hello)
        self.connectLaserButton.clicked.connect(self.connect_laser)


        self.timer = QTimer()
        self.timer.timeout.connect(self.update_power)




    def say_hello(self):
        measured_current = random.uniform(24.5, 25.5)

        self.label.setText(
            f"Measured Current = {measured_current:.2f} mA"
        )

    # connect laser fn
    def connect_laser(self):
        self.statusLabel.setText("Laser Connected")

        self.connectLaserButton.setEnabled(False)
        self.readCurrentButton.setEnabled(True)
        self.timer.start(1000)  # Update every 1 second

    def update_power(self):
        power = random.uniform(9.0, 11.0)

        self.powerLabel.setText(
            f"Power = {power:.2f} mW"   
        )

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())