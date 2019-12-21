from PySide2 import QtGui, QtCore, QtWidgets

class TracerWidget(QtWidgets.QWidget):
    def __init__(self, parent, tracer):
        super().__init__(parent=parent)
        self.tracer = tracer

        layout = QtWidgets.QHBoxLayout()

        calculate_button = QtWidgets.QPushButton()
        calculate_button.setText("Calculate")
        calculate_button.clicked.connect(self.tracer.calculate_traces)

        start_button = QtWidgets.QPushButton()
        start_button.setText("Start")
        start_button.clicked.connect(self.tracer.start)

        delay_slider = QtWidgets.QSpinBox()
        delay_slider.setRange(0, 1000)
        delay_slider.valueChanged.connect(self.tracer.set_delay_ms)
        self.tracer.delay_changed.connect(delay_slider.setValue)
        delay_slider.setValue(self.tracer.delay_ms)

        layout.addWidget(calculate_button)
        layout.addWidget(start_button)
        layout.addWidget(delay_slider)

        self.setLayout(layout)

