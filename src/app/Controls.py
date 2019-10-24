from PySide2 import QtGui, QtCore, QtWidgets

import numpy as np
import pyautogui
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

class Controls(QtWidgets.QWidget):
    def __init__(self, parent, app):
        super().__init__(parent=parent)
        self.app = app
        self.matrix = np.full((4, 4), '')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.create_controls())
        matrix_widget, self.matrix = self.create_matrix((4, 4))
        layout.addWidget(matrix_widget)

        self.setLayout(layout)
    
    def create_controls(self):
        group = QtWidgets.QGroupBox("Controls")
        layout = QtWidgets.QVBoxLayout()

        read_button = QtWidgets.QPushButton()
        read_button.setText("Read")
        QtCore.QObject.connect(read_button, QtCore.SIGNAL("clicked()"), self.on_read)

        solve_button = QtWidgets.QPushButton()
        solve_button.setText("Solve")
        QtCore.QObject.connect(solve_button, QtCore.SIGNAL("clicked()"), self.start_solve)

        export_button = QtWidgets.QPushButton()
        export_button.setText("Export")
        QtCore.QObject.connect(export_button, QtCore.SIGNAL("clicked()"), self.on_export)

        override_label = QtWidgets.QLabel("Override")
        override_checkbox = QtWidgets.QCheckBox()
        override_checkbox.setCheckState(QtCore.Qt.CheckState.Checked if self.app.override_export else QtCore.Qt.CheckState.Unchecked)
        QtCore.QObject.connect(override_checkbox, QtCore.SIGNAL("stateChanged(int)"), self.on_override_change)


        layout.addWidget(read_button)
        layout.addWidget(solve_button)
        # layout.addWidget(export_button)
        # layout.addWidget(override_label)
        # layout.addWidget(override_checkbox)
        group.setLayout(layout)
        return group

    def create_matrix(self, size):
        group = QtWidgets.QGroupBox("Matrix")
        layout = QtWidgets.QGridLayout()

        width, height = size
        matrix = []

        for y in range(height):
            row = []
            for x in range(width):
                text = QtWidgets.QLineEdit()
                text.setText('')
                layout.addWidget(text, y, x)
                row.append(text)
            matrix.append(row)
        
        group.setLayout(layout)
        return (group, matrix)

    def on_read(self):
        matrix = self.app.read_labels()
        width, height = matrix.shape
        for x in range(width):
            for y in range(height):
                char = matrix[y][x]
                text = self.matrix[y][x]
                text.setText(char)

    def start_solve(self):
        path = []
        for x in range(4):
            for y in range(4):
                path.append((x, y))

        coordinates = []
        x_off, y_off = self.app.screen_rect.left, self.app.screen_rect.top
        for box in self.app.bounding_boxes['characters']:
            left, top, right, bottom = box
            x = (left+right)/2 + x_off
            y = (top+bottom)/2 + y_off
            coordinates.append((x, y))
        coordinates = np.array(coordinates).reshape((4, 4, 2))

        matrix = []
        for y in range(4):
            row = []
            for x in range(4):
                text = self.matrix[y][x]
                char = text.text()
                row.append(char.lower())
            matrix.append(row)
        matrix = np.array(matrix)

        print(matrix)

        paths = self.app.solve_matrix(matrix)
        print(paths)
        filtered_paths = {}

        for word, path in paths:
            if word in filtered_paths:
                continue
            filtered_paths[word] = path
        
        filtered_path_list = []
        for word, path in filtered_paths.items():
            filtered_path_list.append((word, path))
        
        filtered_path_list = sorted(filtered_path_list, key=lambda x: len(x[0]), reverse=True)
        print(filtered_path_list)
        for word, path in filtered_path_list:
            self.solve_path(path, coordinates)
            time.sleep(0.04)

    def solve_path(self, path, coordinates):
        x, y = path[0]
        x, y = coordinates[y][x]
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()

        delay = 0.04

        for i, j in path[1:]:
            x, y = coordinates[j][i]
            pyautogui.moveTo(x, y)
            time.sleep(delay)

        pyautogui.mouseUp()

    def on_export(self):
        self.app.export_samples()

    def on_override_change(self, state):
        if state == QtCore.Qt.CheckState.Checked:
            self.app.override_export = True
        else:
            self.app.override_export = False