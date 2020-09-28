import numpy as np
import tflite_runtime.interpreter as tflite

class LiteModel:
    @staticmethod
    def load_from_filepath(filepath):
        with open(filepath, "rb") as fp:
            data = bytes(fp.read())
            return LiteModel(model_content=data)

    def __init__(self, model_content):
        model_content = bytes(model_content)
        self.interpreter = tflite.Interpreter(model_content=model_content)

        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        self.input_shape = input_details[0]['shape']
        self.output_shape = output_details[0]['shape']

        self.input_index = input_details[0]['index']
        self.output_index = output_details[0]['index']

        self.input_scale, self.input_zero_point = input_details[0]['quantization']
        self.output_scale, self.output_zero_point = output_details[0]['quantization']

        self.interpreter.allocate_tensors()
    
    def predict(self, X):
        if len(X.shape) == len(self.input_shape)-1:
            return self.predict(np.array([X]))
        
        if len(X.shape) != len(self.input_shape):
            raise ValueError(f"Dimension mismatch got {X.shape} expected {self.input_shape}")
        
        X = np.array(X, dtype=np.float32)
        
        Y = []
        for x in X:
            self.interpreter.set_tensor(self.input_index, np.array([x]))
            self.interpreter.invoke()
            y = self.interpreter.get_tensor(self.output_index)
            Y.append(y[0])
        return np.array(Y, dtype=np.float32)

    