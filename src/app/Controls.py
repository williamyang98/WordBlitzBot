from PySide2 import QtGui, QtCore, QtWidgets

import numpy as np
import pyautogui
import time
from pprint import pprint

import os
import pandas as pd
import cv2

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

class Controls(QtWidgets.QWidget):
    def __init__(self, parent, app):
        super().__init__(parent=parent)
        self.app = app
        self.delay = 35 

        layout = QtWidgets.QVBoxLayout()


        hgroup = QtWidgets.QWidget(parent=self)
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self.create_controls())
        hlayout.addWidget(self.create_exporter())
        hgroup.setLayout(hlayout)

        layout.addWidget(hgroup)

        matrix_widget = self.create_matrix((4, 4))
        layout.addWidget(matrix_widget)

        self.setLayout(layout)

        
    
    def create_controls(self):
        group = QtWidgets.QGroupBox("Controls")
        layout = QtWidgets.QHBoxLayout()

        read_button = QtWidgets.QPushButton()
        read_button.setText("Read")
        QtCore.QObject.connect(read_button, QtCore.SIGNAL("clicked()"), self.on_read)

        solve_button = QtWidgets.QPushButton()
        solve_button.setText("Solve")
        QtCore.QObject.connect(solve_button, QtCore.SIGNAL("clicked()"), self.start_solve)

        delay_slider = self.create_delay_slider() 

        layout.addWidget(read_button)
        layout.addWidget(solve_button)
        layout.addWidget(delay_slider)
        group.setLayout(layout)


        return group
    
    def create_exporter(self):
        group = QtWidgets.QGroupBox("Exporter")
        layout = QtWidgets.QHBoxLayout()

        export_button = QtWidgets.QPushButton()
        export_button.setText("Export")
        QtCore.QObject.connect(export_button, QtCore.SIGNAL("clicked()"), self.on_export)

        override_label = QtWidgets.QLabel("Override")
        override_checkbox = QtWidgets.QCheckBox()
        override_checkbox.setCheckState(QtCore.Qt.CheckState.Checked if self.app.override_export else QtCore.Qt.CheckState.Unchecked)
        QtCore.QObject.connect(override_checkbox, QtCore.SIGNAL("stateChanged(int)"), self.on_override_change)

        layout.addWidget(export_button)
        layout.addWidget(override_label)
        layout.addWidget(override_checkbox)

        group.setLayout(layout)

        return group
    
    def create_delay_slider(self):
        group = QtWidgets.QGroupBox("Delay")
        layout = QtWidgets.QHBoxLayout()

        slider = QtWidgets.QSpinBox()
        slider.setRange(0, 100)
        slider.setValue(self.delay)

        layout.addWidget(slider)
        group.setLayout(layout)

        QtCore.QObject.connect(slider, QtCore.SIGNAL("valueChanged(int)"), self.set_delay)    

        return group

    def set_delay(self, delay):
        self.delay = delay

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
                cell = self.app.matrix.cells[y][x]

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

                # checkbox = QtWidgets.QCheckBox()
                # checkbox.setCheckState(QtCore.Qt.CheckState.Unchecked)

                cell_layout.addWidget(bonuses) 
                cell_layout.addWidget(text)
                cell_layout.addWidget(value)
                # cell_layout.addWidget(checkbox)

                cell_group.setLayout(cell_layout)

                layout.addWidget(cell_group, y, x)
        
        group.setLayout(layout)
        return group

    def on_read(self):
        self.app.read_data()

    def get_coordinates(self):
        coordinates = []
        x_off, y_off = self.app.screen_rect.left, self.app.screen_rect.top
        _, _, width_target, height_target = self.app.bounding_boxes.get("window")[0]
        width_source, height_source = self.app.screen_rect.width, self.app.screen_rect.height

        x_zoom = width_target / width_source
        y_zoom = height_target / height_source

        for box in self.app.bounding_boxes['characters']:
            left, top, right, bottom = box
            x = ((left+right)/2 / x_zoom) + x_off
            y = ((top+bottom)/2 / y_zoom) + y_off

            coordinates.append((x, y))
        coordinates = np.array(coordinates).reshape((4, 4, 2))
        return coordinates

    def get_solve(self):
        paths = self.app.solve_matrix()

        length_mapping = {2: 3, 3: 4, 4: 6, 5: 9, 6: 11, 7: 14}

        # TODO: Calculate score for each path and find best paths for each word
        # TODO: Incoporate other metadata (bonuses and value)
        # TODO: Show the list of solved words and their values in a list somewhere
        filtered_paths = {}

        characters = self.app.matrix.get_characters()
        bonuses = self.app.matrix.get_bonuses()
        values = self.app.matrix.get_values()

        for word, path in paths:
            word_multipliers = 1
            product_sum = 0 # letter value * letter multiplier
            word_length = len(path)

            constant = length_mapping.get(word_length, 2*word_length)
            
            for character, value, letter_multiplier, word_multiplier in zip(*self.extract_metadata(path)):
                word_multipliers *= word_multiplier
                product_sum += value
                    
            score = (product_sum * word_multipliers) + constant

            if word not in filtered_paths:
                filtered_paths[word] = (score, path)
            else:
                prev_score, _ = filtered_paths[word]
                if score > prev_score:
                    filtered_paths[word] = (score, path)
        
        filtered_path_list = []
        for word, (score, path) in filtered_paths.items():
            filtered_path_list.append((score, word, path))

        filtered_path_list = sorted(filtered_path_list, key=lambda x: x[0], reverse=True)

        return filtered_path_list
    
    def extract_metadata(self, path):
        values = []
        word_multipliers = []
        letter_multipliers = []
        characters = []
        
        for index in path:
            cell = self.app.matrix.get_cell(index)
            values.append(cell.value)
            characters.append(cell.char)
            
            bonus = cell.bonus
            if bonus == '3W':
                word_multipliers.append(3)
            elif bonus == '2W':
                word_multipliers.append(2)
            else:
                word_multipliers.append(1)
            
            if bonus == '2L':
                letter_multipliers.append(2)
            elif bonus == '3L':
                letter_multipliers.append(3)
            else:
                letter_multipliers.append(1)
            
            
        
        return characters, values, letter_multipliers, word_multipliers

    def start_solve(self):
        coordinates = self.get_coordinates() 
        filtered_path_list = self.get_solve()
        pprint(filtered_path_list)

        for value, word, path in filtered_path_list:
            self.solve_path(path, coordinates)
            time.sleep(self.delay/1000)

    def solve_path(self, path, coordinates):
        j, i = path[0]
        x, y = coordinates[j][i]
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()

        for j, i in path[1:]:
            x, y = coordinates[j][i]
            pyautogui.moveTo(x, y)
            time.sleep(self.delay/1000)

        pyautogui.mouseUp()

    def on_export(self):
        filtered_path_list = self.get_solve()

        self.app.export_samples()

        i = 0
        filepath_formatter = "assets/score_prediction/{folder}"

        while os.path.exists(filepath_formatter.format(folder=i)):
            i += 1

        filepath = filepath_formatter.format(folder=i)         
        os.mkdir(filepath)

        # save scores
        score_dataframe = pd.DataFrame(filtered_path_list, columns=["score", "word", "path"])
        score_dataframe.to_csv(f"{filepath}/paths.csv", sep=" ")
        # save picture of sample for reference
        image = self.app.get_screenshot()
        cv2.imwrite(f"{filepath}/sample.png", image)

        # export the matrix data
        matrix_data = []
        matrix_header = ["index", "character", "value", "bonus"]
        for index in np.ndindex((4, 4)):
            cell = self.app.matrix.cells[index]            
            value = cell.value
            char = cell.char
            bonus = cell.bonus
            matrix_data.append([index, char, value, bonus])

        matrix_dataframe = pd.DataFrame(matrix_data, columns=matrix_header)
        matrix_dataframe.to_csv(f"{filepath}/matrix.csv", sep=" ")

        print("Exported all data")


    def on_override_change(self, state):
        if state == QtCore.Qt.CheckState.Checked:
            self.app.override_export = True
        else:
            self.app.override_export = False