from PySide2 import QtGui, QtCore, QtWidgets

class TraceListWidget(QtWidgets.QTableView):
    def __init__(self, parent, tracer):
        super().__init__(parent=parent)
        self.tracer = tracer

        # self.setModel(MyListModel([1, 2, 3, 4]))
        self.setModel(self.tracer.trace_list)