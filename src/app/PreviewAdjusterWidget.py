from PySide2 import QtGui, QtCore, QtWidgets

class PreviewAdjusterWidget(QtWidgets.QWidget):
    def __init__(self, parent, preview):
        super().__init__(parent=parent)
        self.preview = preview

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.create_screen_sliders())

        self.setLayout(layout)

    def create_screen_sliders(self):
        slider_group = QtWidgets.QGroupBox("Screen rect")

        layout = QtWidgets.QHBoxLayout()

        left = self.create_spinbox(
            "Left", (0, 1920), 
            self.preview.screen_rect.left, 
            self.preview.screen_rect.set_left, 
            self.preview.screen_rect.left_changed) 

        top = self.create_spinbox(
            "Top", (0, 1080), 
            self.preview.screen_rect.top, 
            self.preview.screen_rect.set_top, 
            self.preview.screen_rect.top_changed) 

        width = self.create_spinbox(
            "Width", (0, 1920), 
            self.preview.screen_rect.width, 
            self.preview.screen_rect.set_width, 
            self.preview.screen_rect.width_changed) 

        height = self.create_spinbox(
            "Height", 
            (0, 1080), 
            self.preview.screen_rect.height, 
            self.preview.screen_rect.set_height, 
            self.preview.screen_rect.height_changed) 

        layout.addWidget(left)
        layout.addWidget(top)
        layout.addWidget(width)
        layout.addWidget(height)

        slider_group.setLayout(layout)

        return slider_group

    def create_spinbox(self, name, range, value, slot, signal):
        group = QtWidgets.QGroupBox(name)
        layout = QtWidgets.QHBoxLayout()

        slider = QtWidgets.QSpinBox()
        slider.setRange(range[0], range[1])
        slider.setValue(value)

        layout.addWidget(slider)
        group.setLayout(layout)

        slider.valueChanged.connect(slot)
        signal.connect(slider.setValue)

        return group


