from PySide2 import QtGui, QtCore, QtWidgets

from .PreviewWidget import PreviewWidget

from .MatrixWidget import MatrixWidget
from .ExporterWidget import ExporterWidget
from .TracerWidget import TracerWidget
from .PreviewAdjusterWidget import PreviewAdjusterWidget
from .AnalyserWidget import AnalyserWidget

from .TraceListWidget import TraceListWidget

class MainWindow:
    def __init__(self, app):
        self.app = app

        self.splitter = QtWidgets.QSplitter()
        self.splitter.setWindowTitle("Word Blitz Bot")

        self.vertical_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical, self.splitter)
        self.preview_widget = PreviewWidget(self.splitter, app.preview, app.thread_pool)
        self.trace_list_widget = TraceListWidget(self.splitter, app.tracer)

        self.preview_adjuster_widget = PreviewAdjusterWidget(self.vertical_splitter, app.preview)
        self.tracer_widget = TracerWidget(self.vertical_splitter, app.tracer, app.thread_pool)
        self.exporter_widget = ExporterWidget(self.vertical_splitter, app.exporter, app.thread_pool)
        self.analyser_widget = AnalyserWidget(self.vertical_splitter, app.analyser)
        self.matrix_widget = MatrixWidget(self.vertical_splitter, app.matrix)

    def show(self):
        self.splitter.show()