import numpy as np
import cv2

# loads data into matrix
class Analyser:
    def __init__(self, preview, matrix, config):
        self.preview = preview
        self.matrix = matrix

        self.characters_model = config["models"]["characters"]
        self.bonuses_model = config["models"]["bonuses"]
        self.values_model = config["models"]["values"]
    
    def read_matrix(self):
        characters = self.read_characters()
        bonuses = self.read_bonuses()
        values = self.read_values()

        for index, cell in np.ndenumerate(self.matrix.cells):
            cell.setChar(characters[index])
            cell.setBonus(bonuses[index])
            cell.setValue(values[index])

    def resize_images(self, images, shape):
        h, w = shape
        images = [cv2.resize(img, (w, h), interpolation=cv2.INTER_NEAREST) for img in images]
        return np.array(images)

    def read_characters(self):
        images = self.preview.get_characters()
        images = self.resize_images(images, self.characters_model.input_shape[1:3])
        predictions = self.characters_model.predict(images/255.0)

        def convert_prediction(prediction):
            char_index = np.argmax(prediction, axis=0)
            char = chr(char_index + ord('A'))
            return char

        characters = np.apply_along_axis(convert_prediction, 1, predictions)
        characters = np.array(characters).reshape(self.matrix.shape)

        return characters

    def read_values(self):
        images = self.preview.get_values()
        images = self.resize_images(images, self.values_model.input_shape[1:3])
        predictions = self.values_model.predict(images/255.0)

        def convert_prediction(prediction):
            is_single_digit = np.argmax(prediction[0:2]) == 1
            left_digit = np.argmax(prediction[2:2+10])
            right_digit = np.argmax(prediction[-10:]) 

            if is_single_digit:
                return right_digit
            else:
                return left_digit*10 + right_digit

        values = np.apply_along_axis(convert_prediction, 1, predictions)
        values = values.reshape(self.matrix.shape)

        return values
    
    def read_bonuses(self):
        images = self.preview.get_bonuses()
        images = self.resize_images(images, self.bonuses_model.input_shape[1:3])
        predictions = self.bonuses_model.predict(images/255.0)

        mapping = [" ", "2L", "2W", "3L", "3W"]

        def convert_prediction(prediction):
            bonus_type = np.argmax(prediction)
            bonus = mapping[bonus_type]
            return bonus

        bonuses = np.array([convert_prediction(pred) for pred in predictions])
        bonuses = bonuses.reshape(self.matrix.shape)

        return bonuses



