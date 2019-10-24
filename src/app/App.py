import cv2
import mss
import numpy as np
import threading
import pytesseract
import os

from src.matrix_search import search_entire_matrix

class App:
    def __init__(self, bounding_boxes, screen_rect):
        self.is_running = False
        self.bounding_boxes = bounding_boxes
        self.screen_rect = screen_rect
        self.offset = (0, 0)

        self.override_export = False
        self.preview = None
        self.preview_thread_lock = threading.RLock()

        self.word_tree = None


    def take_screenshot(self):
        image = self.get_screenshot()
        with self.preview_thread_lock:
            self.preview = image 
    
    def get_screenshot(self):
        monitor = {
            'left': self.screen_rect.left, 
            'top': self.screen_rect.top, 
            'width': self.screen_rect.width, 
            'height': self.screen_rect.height
        }

        with mss.mss() as screen:
            image = screen.grab(monitor)
        
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return image
    
    def solve_matrix(self, matrix):
        if self.word_tree is None:
            print("Work tree not loaded")
            return
        result = search_entire_matrix(matrix, self.word_tree)
        return result
        
    
    def read_labels(self):
        boxes = self.bounding_boxes.get("characters", [])
        image = self.get_screenshot()
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, image = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY)

        left, top, right, bottom = boxes[0]
        width, height = right-left, bottom-top

        whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        
        # stitched = np.full((height, width*len(boxes)), 255)
        labels = []
        for i, box in enumerate(boxes):
            left, top, right, bottom = box
            cropped_image = image[top:bottom,left:right]
            # stitched[:,i*width:(i+1)*width] = cropped_image
            label = pytesseract.image_to_string(cropped_image, lang="eng", config=f"--psm 10 -c tessedit_char_whitelist={whitelist}")
            if not label:
                label = ''
            if len(label) > 0:
                label = label[0]
            label = label.upper()
            
            labels.append(label)

        # label = pytesseract.image_to_string(stitched, lang="eng", config=f"--psm 7 -c tessedit_char_whitelist={whitelist}")
        matrix = np.array(labels).reshape((4, 4))
        return matrix
    
    def export_samples(self, ext="png"):
        image = self.get_screenshot()
        for key in self.bounding_boxes.keys():
            boxes = self.bounding_boxes.get(key, [])
            samples = self.get_bounding_boxes(image, boxes)
            i = 0
            for sample in samples:
                filename = os.path.join(self.args.export, key, f"sample_{i}.{ext}")

                while not self.override_export and os.path.exists(filename):
                    i += 1
                    filename = os.path.join(self.args.export, key, f"sample_{i}.{ext}")

                cv2.imwrite(filename, sample)
                i += 1

    def get_bounding_boxes(self, image, boxes):
        for box in boxes:
            left, top, right, bottom = box
            sample = image[top:bottom,left:right,:]
            yield sample
    
class ScreenRect:
    def __init__(self, rect):
        left, top, width, height = rect
        self.left = left
        self.top = top
        self.width = width
        self.height = height
    
    def set_left(self, left):
        self.left = left

    def set_top(self, top):
        self.top = top

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height