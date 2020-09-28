from PySide2 import QtGui, QtCore, QtWidgets
from PySide2 import QtCore

from src.models import LambdaRunner

class ControlsWidget(QtWidgets.QWidget):
    def __init__(self, parent, tracer, analyser, thread_pool):
        super().__init__(parent=parent)
        self.tracer = tracer
        self.analyser = analyser

        layout = QtWidgets.QHBoxLayout()

        read_button = QtWidgets.QPushButton()
        read_button.setText("Read")
        read_button.setToolTip("Read characters, bonuses, values from screen")
        read_button.clicked.connect(self.analyser.read_matrix)

        calculate_button = QtWidgets.QPushButton()
        calculate_button.setText("Calculate")
        calculate_button.setToolTip("Determine best list of words from read")
        calculate_button.clicked.connect(self.tracer.calculate_traces)

        start_button = QtWidgets.QPushButton()
        start_button.setText("Start")
        start_button.setToolTip("Start executing the list of words")
        start_button.clicked.connect(self.start_threaded_trace)

        delay_slider = QtWidgets.QSpinBox()
        delay_slider.setRange(0, 1000)
        delay_slider.valueChanged.connect(self.tracer.set_delay_ms)
        self.tracer.delay_changed.connect(delay_slider.setValue)
        delay_slider.setValue(self.tracer.delay_ms)

        layout.addWidget(read_button)
        layout.addWidget(calculate_button)
        layout.addWidget(start_button)
        layout.addWidget(delay_slider)

        self.setLayout(layout)

        self.thread_pool = thread_pool

    def start_threaded_trace(self):
        @LambdaRunner
        def runner():
            self.tracer.start()

        self.thread_pool.start(runner)
