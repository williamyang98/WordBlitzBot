from .Cell import Cell
import numpy as np

class Matrix:
    def __init__(self, shape=(4, 4)):
        self.shape = shape 
        cells = []
        cols, rows = shape
        for _ in range(rows*cols):
            cells.append(Cell())

        self.cells = np.array(cells).reshape(shape)

    def __str__(self):
        return str(self.cells)
    
    def get_cell(self, index):
        return self.cells[index]

    def get_characters(self):
        return np.vectorize(lambda cell: cell.char)(self.cells)

    def get_bonuses(self):
        return np.vectorize(lambda cell: cell.bonus)(self.cells)
    
    def get_values(self):
        return np.vectorize(lambda cell: cell.value)(self.cells)

