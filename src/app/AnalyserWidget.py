from PySide2 import QtGui, QtCore, QtWidgets

class AnalyserWidget(QtWidgets.QWidget):
    def __init__(self, parent, analyser):
        super().__init__(parent=parent)
        self.analyser = analyser

        layout = QtWidgets.QHBoxLayout()

        read_button = QtWidgets.QPushButton()
        read_button.setText("Read")
        read_button.clicked.connect(self.analyser.read_matrix)


        layout.addWidget(read_button)

        self.setLayout(layout)