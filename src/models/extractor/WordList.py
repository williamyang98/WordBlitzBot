from PySide2 import QtCore
from PySide2.QtCore import Slot, Signal, Property

class WordList(QtCore.QAbstractListModel):
    list_size_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._words = []
    
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.words)

    def data(self, index, role):
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return None

        i = index.row()
        try:
            word = self.words[i]
            return word
        except IndexError:
            return None
        return None

    @property
    def words(self):
        return self._words
    
    @words.setter
    def words(self, words):
        self.beginResetModel()
        self._words = words
        self.list_size_changed.emit(len(self._words))
        self.endResetModel()

    @property
    def list_size(self):
        return len(self.words)
    

 