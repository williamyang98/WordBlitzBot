from PySide2.QtCore import QObject, Property, Slot, Signal

class Cell(QObject):
    value_changed = Signal(int)
    char_changed = Signal(str)
    bonus_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self._value = 1
        self._char = ' '
        self._bonus = ' '

    def __str__(self):
        return f"{self._value} {self._char} {self._bonus}"

    def __repr__(self):
        return self.__str__()
    
    @Property(int, notify=value_changed)
    def value(self):
        return self._value
    
    @Slot(int)
    def setValue(self, value):
        self._value = value
        self.value_changed.emit(value)

    @Property(str, notify=char_changed)
    def char(self):
        return self._char
    
    @Slot(str)
    def setChar(self, char):
        self._char = char
        self.char_changed.emit(char)
    
    @Property(str, notify=bonus_changed)
    def bonus(self):
        return self._bonus
    
    @Slot(str)
    def setBonus(self, bonus):
        self._bonus = bonus
        self.bonus_changed.emit(bonus)