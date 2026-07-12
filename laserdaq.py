"""
laserdaq.py

Main entry point for LaserDAQ.
"""

import sys

from PyQt5.QtWidgets import QApplication

from startup_dialog import StartupDialog
from main_V1B import MainWindow


def main():

    app = QApplication(sys.argv)

    # ---------------------------------------
    # Show Startup Dialog
    # ---------------------------------------

    dialog = StartupDialog()

    if dialog.exec_() != dialog.Accepted:

        sys.exit()

    # ---------------------------------------
    # Get Selected Mode
    # ---------------------------------------

    selected_mode = dialog.mode

    print(f"Selected Mode : {selected_mode}")

    # ---------------------------------------
    # Launch Main Window
    # ---------------------------------------

    window = MainWindow(mode=selected_mode)

    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":

    main()