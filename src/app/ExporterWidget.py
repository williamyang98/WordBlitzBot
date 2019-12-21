
from PySide2 import QtGui, QtCore, QtWidgets

class ExporterWidget(QtWidgets.QWidget):
    def __init__(self, parent, exporter, thread_pool):
        super().__init__(parent=parent)
        self.exporter = exporter

        layout = QtWidgets.QHBoxLayout()

        export_button = QtWidgets.QPushButton()
        export_button.setText("Export")
        export_button.clicked.connect(self.on_export)

        override_label = QtWidgets.QLabel("Override")
        override_checkbox = QtWidgets.QCheckBox()
        override_checkbox.setCheckState(QtCore.Qt.CheckState.Checked if self.exporter.override else QtCore.Qt.CheckState.Unchecked)
        override_checkbox.stateChanged.connect(self.on_override_change)

        layout.addWidget(export_button)
        layout.addWidget(override_label)
        layout.addWidget(override_checkbox)

        self.setLayout(layout)

        self.thread_pool = thread_pool

    def on_override_change(self, state):
        if state == QtCore.Qt.CheckState.Checked:
            self.exporter.override = True
        else:
            self.exporter.override = False

    def on_export(self):
        exporter_runner = ExporterRunner(self.exporter)
        self.thread_pool.start(exporter_runner)


class ExporterRunner(QtCore.QRunnable):
    def __init__(self, exporter):
        super().__init__()
        self.exporter = exporter
    
    def run(self):
        self.exporter.export()

    def autoDelete(self):
        return False
