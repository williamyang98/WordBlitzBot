from schema import Schema, And, Use, Optional, SchemaError
import keras
import os

from .defaults import default_dir 

model_schema = Schema(And(str, os.path.exists, Use(keras.models.load_model)))

def get_model_shape_schema(input_shape, output_shape):
    input_schema = And(lambda model: model.input_shape == input_shape, error=f"Expected input shape: {input_shape}")
    output_schema = And(lambda model: model.output_shape == output_shape, error=f"Expected output shape: {output_shape}")
    return And(input_schema, output_schema)

models_schema = Schema({
    "characters": And(model_schema, get_model_shape_schema((None, 36, 36, 3), (None, 26))),
    "bonuses": And(model_schema, get_model_shape_schema((None, 15, 22, 3), (None, 5))),
    "values": And(model_schema, get_model_shape_schema((None, 17, 22, 3), (None, 22))),
})

models_yaml = {
    "characters": os.path.join(default_dir, "models", "characters.h5"),
    "values": os.path.join(default_dir, "models", "two_digit_classifier.h5"),
    "bonuses": os.path.join(default_dir, "models", "bonuses.h5"),
}