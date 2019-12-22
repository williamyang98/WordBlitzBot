from PySide2 import QtGui, QtCore, QtWidgets

from .PreviewWidget import PreviewWidget

from .MatrixWidget import MatrixWidget
from .ExporterWidget import ExporterWidget
from .ControlsWidget import ControlsWidget
from .PreviewAdjusterWidget import PreviewAdjusterWidget

from .TraceListWidget import TraceListWidget
from .HTMLDictionaryExtractorWidget import HTMLDictionaryExtractorWidget

class MainWindow(QtWidgets.QSplitter):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Word Blitz Bot")

        left_panel = self.create_left_panel()
        preview_widget = PreviewWidget(None, self.app.preview, self.app.thread_pool)
        trace_list_widget = TraceListWidget(None, self.app.tracer)
        extractor_widget = HTMLDictionaryExtractorWidget(None, self.app.extractor)

        self.addWidget(left_panel)
        self.addWidget(preview_widget)
        self.addWidget(trace_list_widget)
        self.addWidget(extractor_widget)

    def create_left_panel(self):
        group = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        preview_adjuster_widget = PreviewAdjusterWidget(None, self.app.preview)
        tracer_widget = ControlsWidget(None, self.app.tracer, self.app.analyser, self.app.thread_pool)
        exporter_widget = ExporterWidget(None, self.app.exporter, self.app.thread_pool)
        matrix_widget = MatrixWidget(None, self.app.matrix)

        layout.addWidget(preview_adjuster_widget)
        layout.addWidget(tracer_widget)
        layout.addWidget(exporter_widget)
        layout.addWidget(matrix_widget)

        group.setLayout(layout)

        return group
