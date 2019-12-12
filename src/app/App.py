import cv2
import mss
import numpy as np
import threading
import pytesseract
import os

import keras

from src.matrix_search import search_entire_matrix

from src.models import Matrix

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
        self.matrix = Matrix()

        self.model = keras.models.load_model("assets/models/characters.h5")
        self.bonuses_model = keras.models.load_model("assets/models/bonuses.h5")
        self.values_model = keras.models.load_model("assets/models/values.h5")
        self.two_digit_model = keras.models.load_model("assets/models/two_digit_classifier.h5")


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

        _, _, width, height = self.bounding_boxes.get("window")[0]

        with mss.mss() as screen:
            image = screen.grab(monitor)
        
        image = np.array(image)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        image = cv2.resize(image, (height, width))

        return image
    
    def solve_matrix(self):
        if self.dictionary is None:
            print("Dictionary not loaded in yet")
            return []
        characters = self.matrix.get_characters()
        
        @np.vectorize
        def to_lower(x):
            return x.lower()

        characters = to_lower(characters)
        result = search_entire_matrix(characters, self.dictionary)
        return result

    def read_data(self):
        screenshot = self.get_screenshot()
        # image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
        # bonuses = self.read_bonuses(screenshot)
        characters = self.read_characters(screenshot)
        bonuses = self.read_bonuses(screenshot)
        # values = self.read_values(screenshot)
        values = self.read_two_digits(screenshot)
        for index in np.ndindex(4, 4):
            char = characters[index]
            bonus = bonuses[index]
            value = values[index]
            cell = self.matrix.cells[index]
            cell.setChar(char)
            cell.setBonus(bonus)
            cell.setValue(value)

    def read_bonuses(self, screenshot):
        boxes = self.bounding_boxes.get("bonuses")
        # image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
        image = screenshot

        images = []
        for box in boxes:
            left, top, right, bottom = box
            cropped_image = image[top:bottom,left:right]
            images.append(cropped_image)
        
        images = np.array(images)
        predictions = self.bonuses_model.predict(images/255.0)

        # {'1X': 0, '2L': 1, '2W': 2, '3L': 3, '3W': 4}
        mapping = [' ', '2L', '2W', '3L', '3W']
        map_indices = np.argmax(predictions, axis=1)
        bonuses = list((mapping[i] for i in map_indices))

        bonuses = np.array(bonuses).reshape((4, 4))
        return bonuses

    
    def read_characters(self, screenshot):
        boxes = self.bounding_boxes.get("characters")
        # image = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        image = screenshot
        # _, image = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY)

        left, top, right, bottom = boxes[0]
        # width, height = right-left, bottom-top

        # whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZl"
        
        # stitched = np.full((height, width*len(boxes)), 255)
        images = []
        for i, box in enumerate(boxes):
            left, top, right, bottom = box
            cropped_image = image[top:bottom,left:right,]
            images.append(cropped_image)

        images = np.array(images)
        predictions = self.model.predict(images/255.0)

        character_indices = np.argmax(predictions, axis=1)
        characters = list(map(lambda x: chr(x+ord('A')), character_indices)) 

        # label = pytesseract.image_to_string(stitched, lang="eng", config=f"--psm 7 -c tessedit_char_whitelist={whitelist}")
        characters = np.array(characters).reshape((4, 4))
        return characters

    def read_values(self, image):
        boxes = self.bounding_boxes.get("values")
        images = []
        for i, box in enumerate(boxes):
            left, top, right, bottom = box
            cropped_image = image[top:bottom,left:right,]
            images.append(cropped_image)

        images = np.array(images)
        predictions = self.values_model.predict(images/255.0)
        values = np.argmax(predictions, axis=1)

        values = np.array(values).reshape((4, 4))
        return values

    def read_two_digits(self, image):
        boxes = self.bounding_boxes.get("values")
        images = []
        for i, box in enumerate(boxes):
            left, top, right, bottom = box
            cropped_image = image[top:bottom,left:right,]
            images.append(cropped_image)

        images = np.array(images)
        predictions = self.two_digit_model.predict(images/255.0)

        values = []
        for prediction in predictions:
            is_single_digit = np.argmax(prediction[0:2]) == 1
    
            left_digit = np.argmax(prediction[2:2+10])
            right_digit = np.argmax(prediction[2+10:2+10+10])

            if is_single_digit:
                value = right_digit
            else:
                value = left_digit*10 + right_digit

            values.append(value)

        values = np.array(values).reshape((4, 4))
        return values
    
    def export_samples(self, ext="png"):
        image = self.get_screenshot()
        mappings = {
            "bonuses": lambda cell: cell.bonus, 
            "characters": lambda cell: cell.char, 
            "values": lambda cell: cell.value, 
        }
        for category in ("bonuses", "characters", "values"):
            boxes = self.bounding_boxes.get(category, [])
            samples = self.get_ranged_bounding_boxes(image, boxes)
            self.export_category_samples(category, samples, ext, mappings)



    def export_category_samples(self, category, samples, ext, mappings):
        header = ["filename", "category"]
        labels_file = os.path.join(self.args.export, category, "labels.txt")
        labels_created = os.path.exists(labels_file) and not self.override_export

        mode = "a" if not self.override_export else "w+"

        with open(labels_file, mode) as file:
            if not labels_created:
                file.write(" ".join(header)+"\n")

            i = 0
            for index in np.ndindex(samples.shape[:2]):
                current_samples = samples[index]
                cell = self.matrix.cells[index]
                for sample in current_samples:
                    filename = os.path.join(self.args.export, category, f"sample_{i}.{ext}")

                    while not self.override_export and os.path.exists(filename):
                        i += 1
                        filename = os.path.join(self.args.export, category, f"sample_{i}.{ext}")

                    cv2.imwrite(filename, sample)

                    file.write(f"sample_{i}.{ext} {mappings[category](cell)}\n")

                    i += 1

    
    def get_ranged_bounding_boxes(self, image, boxes, variation=1):
        samples = []
        for box in boxes:
            current_samples = []
            for x_off in range(-variation, variation+1):
                for y_off in range(-variation, variation+1):
                    left, top, right, bottom = box
                    sample = image[top+y_off:bottom+y_off, left+x_off:right+x_off, :]
                    current_samples.append(sample)
            samples.append(current_samples)

        samples = np.array(samples)
        new_shape = (4, 4) + samples.shape[1:] 
        return samples.reshape(new_shape)


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