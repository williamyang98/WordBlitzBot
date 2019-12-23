from PySide2 import QtCore
from PySide2.QtCore import Slot, Signal

from functools import total_ordering

@total_ordering
class Trace(QtCore.QObject):
    is_complete_changed = Signal(bool)

    def __init__(self, result):
        super().__init__()

        self.word = result.word
        self.path = result.path
        self.score = result.score

        self.is_complete = False

    def __str__(self):
        return f"{self.word} {self.path} {self.score} {self.is_complete}"
    
    def __repr__(self):
        return self.__str__()

    @property
    def is_complete(self):
        return self._is_complete

    @is_complete.setter
    def is_complete(self, is_complete):
        self._is_complete = is_complete
        self.is_complete_changed.emit(is_complete)
    
    @Slot(bool)
    def set_is_complete(self, is_complete):
        self.is_complete = is_complete

    def __lt__(self, other):
        return self.score < other.score
    
    def __eq__(self, other):
        return self.score == other.score

    