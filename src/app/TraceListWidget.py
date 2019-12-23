from PySide2 import QtGui, QtCore, QtWidgets

class TraceListWidget(QtWidgets.QWidget):
    def __init__(self, parent, tracer):
        super().__init__(parent=parent)
        self.tracer = tracer

        layout = QtWidgets.QVBoxLayout()

        table = self.create_table()

        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)

        def progress_listener(progress):
            progress = int(progress*100)
            progress_bar.setValue(progress)


        self.tracer.progress_changed.connect(progress_listener)

        layout.addWidget(table)
        layout.addWidget(progress_bar)

        self.setLayout(layout)

    def create_table(self):
        table = QtWidgets.QTableView()

        table.setModel(self.tracer.trace_list)
        table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        return table
