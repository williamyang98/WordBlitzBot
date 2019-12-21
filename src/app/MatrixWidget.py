from PySide2 import QtGui, QtCore, QtWidgets
import numpy as np

class MatrixWidget(QtWidgets.QWidget):
    def __init__(self, parent, matrix):
        super().__init__(parent=parent)
        self.matrix = matrix

        layout = QtWidgets.QGridLayout()

        for (y, x), cell in np.ndenumerate(self.matrix.cells):
            cell_group = self.create_cell_group(cell)
            layout.addWidget(cell_group, y, x)
        
        self.setLayout(layout)
    
    def create_cell_group(self, cell):
        cell_group = QtWidgets.QGroupBox()
        cell_layout = QtWidgets.QHBoxLayout()

        text = QtWidgets.QLineEdit()
        text.setText('')
        text.textEdited.connect(cell.setChar)
        cell.char_changed.connect(text.setText)

        bonuses = QtWidgets.QComboBox()
        bonuses.addItems([" ", "2W", "2L", "3W", "3L"])                
        bonuses.currentTextChanged.connect(cell.setBonus)
        cell.bonus_changed.connect(bonuses.setCurrentText)

        value = QtWidgets.QSpinBox()
        value.setRange(1, 99)
        value.valueChanged.connect(cell.setValue)
        cell.value_changed.connect(value.setValue)
        value.setValue(1)

        cell_layout.addWidget(bonuses) 
        cell_layout.addWidget(text)
        cell_layout.addWidget(value)

        cell_group.setLayout(cell_layout)

        return cell_group
