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
        cols, rows = self.shape
        data = []
        for x in range(cols):
            for y in range(rows):
                data.append(self.cells[y][x].char)
        return np.array(data).reshape(self.shape)

    def get_bonuses(self):
        cols, rows = self.shape
        data = []
        for x in range(cols):
            row = []
            data.append(row)
            for y in range(rows):
                row.append(self.cells[y][x].bonus)
        return np.array(data).reshape(self.shape)
    
    def get_values(self):
        cols, rows = self.shape
        data = []
        for x in range(cols):
            row = []
            data.append(row)
            for y in range(rows):
                row.append(self.cells[y][x].value)
        return np.array(data).reshape(self.shape)

