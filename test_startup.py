import sys

from PyQt5.QtWidgets import QApplication

from startup_dialog import StartupDialog

app = QApplication(sys.argv)

dialog = StartupDialog()

if dialog.exec_():

    print(dialog.mode)