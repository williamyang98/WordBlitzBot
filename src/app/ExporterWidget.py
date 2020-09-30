from PySide2 import QtGui, QtCore, QtWidgets

from src.models import LambdaRunner

class ExporterWidget(QtWidgets.QWidget):
    def __init__(self, parent, exporter, thread_pool):
        super().__init__(parent=parent)
        self.exporter = exporter

        layout = QtWidgets.QHBoxLayout()

        export_images_button = QtWidgets.QPushButton()
        export_images_button.setText("Export Images")
        export_images_button.clicked.connect(self.on_export_images)

        export_metadata_button = QtWidgets.QPushButton()
        export_metadata_button.setText("Export Metadata")
        export_metadata_button.clicked.connect(self.on_export_metadata)

        override_label = QtWidgets.QLabel("Override")
        override_checkbox = QtWidgets.QCheckBox()
        override_checkbox.setCheckState(QtCore.Qt.CheckState.Checked if self.exporter.override else QtCore.Qt.CheckState.Unchecked)
        override_checkbox.stateChanged.connect(self.on_override_change)

        layout.addWidget(export_images_button)
        layout.addWidget(export_metadata_button)
        layout.addWidget(override_label)
        layout.addWidget(override_checkbox)

        self.setLayout(layout)

        self.thread_pool = thread_pool

    def on_override_change(self, state):
        if state == QtCore.Qt.CheckState.Checked:
            self.exporter.override = True
        else:
            self.exporter.override = False

    def on_export_images(self):
        @LambdaRunner
        def runner():
            self.exporter.export_image_data()

        self.thread_pool.start(runner)

    def on_export_metadata(self):
        @LambdaRunner
        def runner():
            self.exporter.export_metadata()
        
        self.thread_pool.start(runner)
