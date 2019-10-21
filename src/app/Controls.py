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

        QtCore.QObject.connect(read_button, QtCore.SIGNAL("clicked()"), self.on_read)

        layout.addWidget(read_button)
        group.setLayout(layout)
        return group

    def on_read(self):
        self.app.read_labels()
