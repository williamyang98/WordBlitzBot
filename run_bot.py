from PySide2 import QtGui, QtCore, QtWidgets
import argparse
import sys
import yaml
import os

from src.models import App
from src.app import MainWindow

from src.config import default_yaml, app_schema


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml", type=str)

    args = parser.parse_args()

    try:
        with open(args.config, "r") as fp:
            config = yaml.load(fp, Loader=yaml.FullLoader)
            config = app_schema.validate(config)
    except FileNotFoundError:
        with open(args.config, "w") as fp:
            yaml.dump(default_yaml, fp)
            config = default_yaml

    app = App(config)

    qt_app = QtWidgets.QApplication([])
    qt_app.setStyle("fusion")

    window = MainWindow(app)
    window.show()

    return qt_app.exec_()

if __name__ == '__main__':
    sys.exit(main())