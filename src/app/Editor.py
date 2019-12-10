from PySide2 import QtGui, QtCore, QtWidgets

class Editor(QtWidgets.QWidget):
    def __init__(self, parent, app):
        super().__init__(parent=parent)
        self.app = app

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.create_screen_sliders())

        self.setLayout(layout)

    def create_screen_sliders(self):
        slider_group = QtWidgets.QGroupBox("Screen rect")

        layout = QtWidgets.QHBoxLayout()

        left = self.create_spinbox("Left", (0, 1920), self.app.screen_rect.left, self.app.screen_rect.set_left) 
        top = self.create_spinbox("Top", (0, 1080), self.app.screen_rect.top, self.app.screen_rect.set_top) 
        width = self.create_spinbox("Width", (0, 1920), self.app.screen_rect.width, self.app.screen_rect.set_width) 
        height = self.create_spinbox("Height", (0, 1080), self.app.screen_rect.height, self.app.screen_rect.set_height) 

        layout.addWidget(left)
        layout.addWidget(top)
        layout.addWidget(width)
        layout.addWidget(height)

        slider_group.setLayout(layout)

        return slider_group

    def create_spinbox(self, name, range, value, listener):
        group = QtWidgets.QGroupBox(name)
        layout = QtWidgets.QHBoxLayout()

        slider = QtWidgets.QSpinBox()
        slider.setRange(range[0], range[1])
        slider.setValue(value)

        layout.addWidget(slider)
        group.setLayout(layout)

        QtCore.QObject.connect(slider, QtCore.SIGNAL("valueChanged(int)"), listener)

        return group


