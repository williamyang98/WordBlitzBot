from PySide2 import QtGui, QtCore, QtWidgets
import argparse
import sys
import pytesseract

from src.util import load_bounding_boxes
from src.app import App, MainWindow, ScreenRect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--boxes", default="assets/bounding_boxes.txt")
    parser.add_argument("--tesseract-cmd", default=r"C:/Program Files/Tesseract-OCR/tesseract.exe")

    args = parser.parse_args()

    pytesseract.pytesseract.tesseract_cmd = args.tesseract_cmd

    bounding_boxes = load_bounding_boxes(args.boxes)
    screen_rect = (526, 422, 438, 440)
    screen_rect = ScreenRect(screen_rect)

    app = App(bounding_boxes, screen_rect)

    QtWidgets.QApplication.setStyle("fusion")
    qt_app = QtWidgets.QApplication([])

    window = MainWindow(app)
    window.show()

    return qt_app.exec_()




if __name__ == '__main__':
    sys.exit(main())