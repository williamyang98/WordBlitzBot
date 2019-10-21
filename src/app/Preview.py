from PySide2 import QtGui, QtCore, QtWidgets
import cv2

class Preview(QtWidgets.QLabel):
    def __init__(self, parent, app):
        super().__init__(parent=parent)
        self.app = app

        self.colour_map = {
            "characters":   (255, 0, 0),
            "bonuses":      (0, 255, 0),
            "values":       (0, 0, 255),
        }

        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.start(25)

        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update)
    
    def update(self):
        with self.app.preview_thread_lock:
            preview = self.app.preview
            self.app.preview = None

        if preview is None:
            return
        # construct preview 
        for key, bounding_boxes in self.app.bounding_boxes.items():
            colour = self.colour_map.get(key, (255, 0, 0))
            for bounding_box in bounding_boxes:
                left, top, right, bottom = bounding_box
                cv2.rectangle(preview, (left, top), (right, bottom), colour)
        # display
        height, width, channel = preview.shape
        bytes_per_line = width * 3
        self.qt_image = QtGui.QImage(preview.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.setPixmap(QtGui.QPixmap.fromImage(self.qt_image))