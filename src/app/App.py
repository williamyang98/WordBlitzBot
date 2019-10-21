import cv2
import mss
import numpy as np
import threading
import pytesseract

from pynput.keyboard import Key, Listener

class App:
    def __init__(self, bounding_boxes, screen_rect):
        self.is_running = False
        self.bounding_boxes = bounding_boxes
        self.screen_rect = screen_rect
        self.offset = (0, 0)

        self.preview = None
        self.preview_thread_lock = threading.RLock()

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
    
    def read_labels(self):
        boxes = self.bounding_boxes.get("characters", [])
        image = self.get_screenshot()
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, image = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY)

        left, top, right, bottom = boxes[0]
        width, height = right-left, bottom-top
        
        stitched = np.full((height, width*len(boxes)), 255)
        for i, box in enumerate(boxes):
            left, top, right, bottom = box
            cropped_image = image[top:bottom,left:right]
            stitched[:,i*width:(i+1)*width] = cropped_image
            # cropped_image = cv2.resize(cropped_image, (16, 16))

        whitelist = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz|"
        label = pytesseract.image_to_string(stitched, lang="eng", config=f"--psm 7 -c tessedit_char_whitelist={whitelist}")
        print(label)

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