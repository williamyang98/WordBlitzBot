from PySide2 import QtGui, QtCore, QtWidgets

class TraceListWidget(QtWidgets.QListView):
    def __init__(self, parent, tracer):
        super().__init__(parent=parent)
        self.tracer = tracer

        self.model = QtCore.QStringListModel() 
        self.setModel(self.model)

        self.tracer.traces_changed.connect(self.on_traces_change)


    def on_traces_change(self):
        strings = [str(trace) for trace in self.tracer.traces]
        self.model.setStringList(strings)
