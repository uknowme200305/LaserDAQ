import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt5 import uic

import pyqtgraph as pg
from PyQt5.QtCore import QTimer
import random


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("laser_characterization_V1.ui", self)

        # Create plot widget
        self.li_plot = pg.PlotWidget()

        # Put plot widget inside the placeholder QWidget
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.li_plot)

        self.liPlotWidget.setLayout(layout)

        # Sample L-I data
        current = [0, 20, 40, 60, 80, 100]
        power = [0, 0, 5, 20, 40, 65]

        self.li_plot.plot(
            current,
            power,
            pen='y',
            symbol='o'
        )

        self.li_plot.setTitle("L-I Curve")
        self.li_plot.setLabel('left', 'Power (mW)')
        self.li_plot.setLabel('bottom', 'Current (mA)')
        self.li_plot.showGrid(x=True, y=True)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())