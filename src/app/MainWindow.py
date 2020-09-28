from PySide2 import QtGui, QtCore, QtWidgets

from .PreviewWidget import PreviewWidget

from .MatrixWidget import MatrixWidget
from .ExporterWidget import ExporterWidget
from .ControlsWidget import ControlsWidget
from .PreviewAdjusterWidget import PreviewAdjusterWidget

from .TraceListWidget import TraceListWidget
from .ExtractorWidget import ExtractorWidget

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Word Blitz Bot")

        left_panel = self.create_left_panel()
        preview_widget = PreviewWidget(None, self.app.preview, self.app.thread_pool, app)
        trace_list_widget = TraceListWidget(None, self.app.tracer)
        extractor_widget = ExtractorWidget(None, self.app.extractor)

        main_tab = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(left_panel)
        layout.addWidget(preview_widget)
        main_tab.setLayout(layout)

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(main_tab, "Primary")
        tabs.addTab(trace_list_widget, "Progress")
        tabs.addTab(extractor_widget, "Dictionary Editor")

        def update_progress_tab(prog):
            tabs.setTabText(1, f"Progress ({prog*100:.0f}%)")
        
        app.tracer.progress_changed.connect(update_progress_tab)

        self.setCentralWidget(tabs)
        self.adjustSize()

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

    # active threads use app.is_running 
    # use this to stop all threads so app closes properly 
    def closeEvent(self, event):
        self.app.is_running = False
        return super().closeEvent(event)
