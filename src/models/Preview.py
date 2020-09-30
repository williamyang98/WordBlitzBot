import cv2
import mss
import numpy as np
import threading

class Preview:
    def __init__(self, bounding_boxes, screen_rect):
        self.preview = None
        self.thread_lock = threading.RLock()
        self.screen_rect = screen_rect
        self.bounding_boxes = bounding_boxes

    def take_screenshot(self):
        image = self.get_screenshot()
        with self.thread_lock:
            self.preview = image 

        return image
    
    def get_screenshot(self):
        monitor = {
            'left': self.screen_rect.left, 
            'top': self.screen_rect.top, 
            'width': self.screen_rect.width, 
            'height': self.screen_rect.height
        }

        _, _, width, height = self.bounding_boxes.get("window")[0]

        with mss.mss() as screen:
            image = screen.grab(monitor)
        
        image = np.array(image)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        image = cv2.resize(image, (height, width))

        return image
    
    def get_coordinates(self):
        coordinates = []
        x_off, y_off = self.screen_rect.left, self.screen_rect.top
        _, _, width_target, height_target = self.bounding_boxes.get("window")[0]
        width_source, height_source = self.screen_rect.width, self.screen_rect.height

        x_zoom = width_target / width_source
        y_zoom = height_target / height_source

        for box in self.bounding_boxes['characters']:
            left, top, right, bottom = box
            x = ((left+right)/2 / x_zoom) + x_off
            y = ((top+bottom)/2 / y_zoom) + y_off

            coordinates.append((x, y))
        coordinates = np.array(coordinates).reshape((4, 4, 2))
        return coordinates
    
    def get_characters(self):
        boxes = self.bounding_boxes.get("characters")
        return self.get_cropped(boxes)

    def get_bonuses(self):
        boxes = self.bounding_boxes.get("bonuses")
        return self.get_cropped(boxes)

    def get_values(self):
        boxes = self.bounding_boxes.get("values")
        return self.get_cropped(boxes)

    def get_cropped(self, boxes):
        images = []
        image  = self.preview
        for box in boxes:
            left, top, right, bottom = box
            cropped = image[top:bottom, left:right]
            images.append(cropped)
        return np.array(images)
