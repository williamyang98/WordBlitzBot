from PySide2 import QtGui, QtCore, QtWidgets

class Controls(QtWidgets.QWidget):
    def __init__(self, parent, app):
        super().__init__(parent=parent)
        self.app = app

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.create_controls())

        self.setLayout(layout)
    
    def create_controls(self):
        group = QtWidgets.QGroupBox("Controls")
        layout = QtWidgets.QVBoxLayout()

        read_button = QtWidgets.QPushButton()
        read_button.setText("Read")

        export_button = QtWidgets.QPushButton()
        export_button.setText("Export")

        override_label = QtWidgets.QLabel("Override")
        override_checkbox = QtWidgets.QCheckBox()
        override_checkbox.setCheckState(QtCore.Qt.CheckState.Checked if self.app.override_export else QtCore.Qt.CheckState.Unchecked)

        QtCore.QObject.connect(read_button, QtCore.SIGNAL("clicked()"), self.on_read)
        QtCore.QObject.connect(export_button, QtCore.SIGNAL("clicked()"), self.on_export)
        QtCore.QObject.connect(override_checkbox, QtCore.SIGNAL("stateChanged(int)"), self.on_override_change)

        layout.addWidget(read_button)
        layout.addWidget(export_button)
        layout.addWidget(override_label)
        layout.addWidget(override_checkbox)
        group.setLayout(layout)
        return group

    def on_read(self):
        self.app.read_labels()

    def on_export(self):
        self.app.export_samples()

    def on_override_change(self, state):
        if state == QtCore.Qt.CheckState.Checked:
            self.app.override_export = True
        else:
            self.app.override_export = False