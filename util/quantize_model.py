import os
import argparse

MODEL_DIR = "assets/models/"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_in")
    parser.add_argument("model_out")

    args = parser.parse_args()

    import tensorflow as tf
    model = tf.keras.models.load_model(args.model_in)

    print(f"input_shape: {model.input_shape}")
    print(f"output_shape: {model.output_shape}")

    # quantize and store as bytefile
    quantized_model = convert(model)
    with open(args.model_out, 'wb+') as file:
        file.write(quantized_model)

def convert(model):
    import tensorflow as tf
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_LATENCY]
    # converter.inference_input_type = tf.uint8
    # converter.inference_output_type = tf.uint8
    # converter.target_spec.supported_types = [tf.lite.constants.FLOAT16] # reduce weights
    tflite_quant_model = converter.convert()
    return tflite_quant_model

if __name__ == '__main__':
    main()

