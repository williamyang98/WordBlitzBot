from PySide2 import QtGui, QtCore, QtWidgets

import numpy as np
import pyautogui
import time
from pprint import pprint

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

class Controls(QtWidgets.QWidget):
    def __init__(self, parent, app):
        super().__init__(parent=parent)
        self.app = app

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.create_controls())
        matrix_widget, self.character_fields, self.bonus_fields = self.create_matrix((4, 4))
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

        character_fields = []
        bonus_fields = [] 

        for y in range(height):
            for x in range(width):
                cell_group = QtWidgets.QGroupBox()
                cell_layout = QtWidgets.QHBoxLayout()

                text = QtWidgets.QLineEdit()
                text.setText('')

                checkbox = QtWidgets.QCheckBox()
                checkbox.setCheckState(QtCore.Qt.CheckState.Unchecked)
            
                cell_layout.addWidget(text)
                cell_layout.addWidget(checkbox)

                character_fields.append(text)
                bonus_fields.append(checkbox)

                cell_group.setLayout(cell_layout)

                layout.addWidget(cell_group, y, x)
        
        group.setLayout(layout)
        character_fields = np.array(character_fields).reshape((4, 4))
        bonus_fields = np.array(bonus_fields).reshape((4, 4))
        return group, character_fields, bonus_fields

    def on_read(self):
        characters, bonuses = self.app.read_data()
        
        width, height = characters.shape
        for x in range(width):
            for y in range(height):
                char = characters[y][x]
                text = self.character_fields[y][x]
                text.setText(char)
                
                bonus = bonuses[y][x]
                state = QtCore.Qt.CheckState.Checked if bonus else QtCore.Qt.CheckState.Unchecked
                checkbox = self.bonus_fields[y][x]
                checkbox.setCheckState(state)

    
    def get_coordinates(self):
        coordinates = []
        x_off, y_off = self.app.screen_rect.left, self.app.screen_rect.top
        for box in self.app.bounding_boxes['characters']:
            left, top, right, bottom = box
            x = (left+right)/2 + x_off
            y = (top+bottom)/2 + y_off
            coordinates.append((x, y))
        coordinates = np.array(coordinates).reshape((4, 4, 2))
        return coordinates

    def start_solve(self):
        coordinates = self.get_coordinates() 

        @np.vectorize
        def get_characters(text):
            return text.text().lower()[:1] 

        @np.vectorize
        def get_bonuses(checkbox):
            bonus = int(checkbox.checkState() == QtCore.Qt.CheckState.Checked)
            return bonus

        characters = get_characters(self.character_fields)
        bonuses = get_bonuses(self.bonus_fields)

        paths = self.app.solve_matrix(characters)

        # TODO: Calculate score for each path and find best paths for each word
        # TODO: Incoporate other metadata (bonuses and value)
        # TODO: Show the list of solved words and their values in a list somewhere
        filtered_paths = {}

        for word, path in paths:
            additional_value = 0
            for x, y in path:
                bonus = bonuses[y][x]
                additional_value += bonus 

            total_value = len(word) + additional_value
            if word not in filtered_paths:
                filtered_paths[word] = (total_value, path)
            else:
                prev_value, _ = filtered_paths[word]
                if total_value > prev_value:
                    filtered_paths[word] = (total_value, path)
        
        filtered_path_list = []
        for word, (total_value, path) in filtered_paths.items():
            filtered_path_list.append((total_value, word, path))

        filtered_path_list = sorted(filtered_path_list, key=lambda x: x[0], reverse=True)

        pprint(filtered_path_list)

        for value, word, path in filtered_path_list:
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