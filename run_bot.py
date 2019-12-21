from PySide2 import QtGui, QtCore, QtWidgets
import argparse
import sys

from src.models import App
from src.app import MainWindow

from pynput.keyboard import Key, Listener

def main():
    qt_app = QtWidgets.QApplication([])
    qt_app.setStyle("fusion")

    app = App()
    window = MainWindow(app)
    window.show()

    return qt_app.exec_()



if __name__ == '__main__':
    sys.exit(main())