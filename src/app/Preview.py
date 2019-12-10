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

        self.panning = False
        self._last_position = QtCore.QPoint(0, 0)
    
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
        
        image = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
        self.qt_image = QtGui.QImage(image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.setPixmap(QtGui.QPixmap.fromImage(self.qt_image))
    
    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.MidButton:
            self.panning = True
            self._last_position = ev.pos()
        
        return super().mousePressEvent(ev)
    
    def mouseReleaseEvent(self, ev):
        if ev.button() == QtCore.Qt.MidButton:
            self.panning = False

        return super().mouseReleaseEvent(ev)
    
    def mouseMoveEvent(self, ev):
        if self.panning:
            delta = self._last_position-ev.pos()
            self._last_position = ev.pos()
            self.app.screen_rect.left += delta.x()
            self.app.screen_rect.top += delta.y()

        return super().mouseMoveEvent(ev)

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 16
        zoom = pow(1.20, delta/200)
        self.zoom(zoom)

        return super().wheelEvent(event)

    def zoom(self, zoom):
        self.app.screen_rect.width = int(self.app.screen_rect.width* zoom)
        self.app.screen_rect.height = int(self.app.screen_rect.height* zoom)

