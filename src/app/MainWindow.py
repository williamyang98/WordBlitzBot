from PySide2 import QtGui, QtCore, QtWidgets

from .Preview import Preview
from .Editor import Editor
from .Controls import Controls

class MainWindow:
    def __init__(self, application):
        self.application = application

        self.splitter = QtWidgets.QSplitter()
        self.splitter.setWindowTitle("Word Blitz Bot")

        self.vertical_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical, self.splitter)
        self.editor = Editor(self.vertical_splitter, application)
        self.controls = Controls(self.vertical_splitter, application)


        self.preview = Preview(self.splitter, application)

        # setup main timer
        self.screen_shot_timer = QtCore.QTimer(self.splitter)
        self.screen_shot_timer.setSingleShot(False)
        self.screen_shot_timer.start(25)
        QtCore.QObject.connect(self.screen_shot_timer, QtCore.SIGNAL("timeout()"), self.application.take_screenshot)

    def show(self):
        self.splitter.show()