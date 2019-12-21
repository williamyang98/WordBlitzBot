from PySide2.QtCore import QObject, Property, Slot, Signal
from PySide2 import QtCore

from pprint import pprint

class TraceListModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None, *args):
        super().__init__(parent, *args)
        self._traces = []
        self.header = ["Word", "Score", "Is Complete"]

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.traces)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.header)

    def data(self, index, role):
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return None 

        y = index.row()
        x = index.column()

        trace = self.traces[y]

        try:
            trace = self.traces[y]
            if x == 0:
                return trace.word 
            elif x == 1:
                return str(trace.score)
            elif x == 2:
                return trace.is_complete
        except IndexError:
            return None

        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if section < 0 or section >= len(self.header):
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation != QtCore.Qt.Horizontal:
            return None
        
        return self.header[section]

    @property
    def traces(self):
        return self._traces
    
    @traces.setter
    def traces(self, traces):
        self.beginResetModel()
        self._traces = traces
        self.endResetModel()


