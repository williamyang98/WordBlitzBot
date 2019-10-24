from PySide2 import QtGui, QtCore, QtWidgets
import argparse
import sys
import pytesseract
import threading

from src.util import load_bounding_boxes, load_tree
from src.app import App, MainWindow, ScreenRect

from pynput.keyboard import Key, Listener

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--boxes", default="assets/bounding_boxes.txt")
    parser.add_argument("--tesseract-cmd", default=r"C:/Program Files/Tesseract-OCR/tesseract.exe")
    parser.add_argument("--export", default=r"assets/data")
    parser.add_argument("--dictionary", default="assets/dictionaries/compact_dictionary.txt")

    args = parser.parse_args()

    pytesseract.pytesseract.tesseract_cmd = args.tesseract_cmd

    bounding_boxes = load_bounding_boxes(args.boxes)
    screen_rect = (526, 422, 438, 440)
    screen_rect = ScreenRect(screen_rect)

    app = App(bounding_boxes, screen_rect)
    app.args = args

    QtWidgets.QApplication.setStyle("fusion")
    qt_app = QtWidgets.QApplication([])

    def on_press(key):
        if key == Key.f3:
            print("Kill switch activated")
            qt_app.quit()

    def load_word_tree():
        word_tree = load_tree(args.dictionary)
        app.word_tree = word_tree

    key_listener = Listener(on_press=on_press)
    key_listener.start()

    word_tree_thread = threading.Thread(target=load_word_tree)
    word_tree_thread.start()

    window = MainWindow(app)
    window.show()

    # key_listener.join()
    # word_tree_thread.join()

    return qt_app.exec_()

if __name__ == '__main__':
    sys.exit(main())