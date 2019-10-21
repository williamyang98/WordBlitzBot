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

        layout = QtWidgets.QVBoxLayout()

        left_label = QtWidgets.QLabel("Left")
        left_slider = QtWidgets.QSpinBox()
        left_slider.setRange(0, 1920)
        left_slider.setValue(self.app.screen_rect.left)
        layout.addWidget(left_label)
        layout.addWidget(left_slider)

        top_label = QtWidgets.QLabel("Top")
        top_slider = QtWidgets.QSpinBox()
        top_slider.setRange(0, 1080)
        top_slider.setValue(self.app.screen_rect.top)
        layout.addWidget(top_label)
        layout.addWidget(top_slider)

        width_label = QtWidgets.QLabel("Width")
        width_slider = QtWidgets.QSpinBox()
        width_slider.setRange(0, 1080)
        width_slider.setValue(self.app.screen_rect.width)
        layout.addWidget(width_label)
        layout.addWidget(width_slider)

        height_label = QtWidgets.QLabel("Height")
        height_slider = QtWidgets.QSpinBox()
        height_slider.setRange(0, 1080)
        height_slider.setValue(self.app.screen_rect.height)
        layout.addWidget(height_label)
        layout.addWidget(height_slider)

        slider_group.setLayout(layout)

        QtCore.QObject.connect(left_slider, QtCore.SIGNAL("valueChanged(int)"), self.app.screen_rect.set_left)
        QtCore.QObject.connect(top_slider, QtCore.SIGNAL("valueChanged(int)"), self.app.screen_rect.set_top)
        QtCore.QObject.connect(width_slider, QtCore.SIGNAL("valueChanged(int)"), self.app.screen_rect.set_width)
        QtCore.QObject.connect(height_slider, QtCore.SIGNAL("valueChanged(int)"), self.app.screen_rect.set_height)

        return slider_group


