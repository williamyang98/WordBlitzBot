from schema import Schema, And, Use, Optional, SchemaError
import os
from src.models import LiteModel

from .defaults import default_dir 

model_schema = Schema(And(str, os.path.exists, Use(LiteModel.load_from_filepath)))

def compare_shapes(s1, s2):
    return list(s1) == list(s2)

def get_model_shape_schema(input_shape, output_shape):
    input_schema = And(lambda model: compare_shapes(model.input_shape, input_shape), error=f"Got input shape {{0.input_shape}} expected {input_shape}")
    output_schema = And(lambda model: compare_shapes(model.output_shape, output_shape), error=f"Got input shape {{0.output_shape}} expected {output_shape}")
    return And(input_schema, output_schema)

models_schema = Schema({
    "characters": And(model_schema, get_model_shape_schema((1, 36, 36, 3), (1, 26))),
    "bonuses": And(model_schema, get_model_shape_schema((1, 15, 22, 3), (1, 5))),
    "values": And(model_schema, get_model_shape_schema((1, 17, 22, 3), (1, 22))),
})

models_yaml = {
    "characters": os.path.join(default_dir, "models", "characters.h5"),
    "values": os.path.join(default_dir, "models", "two_digit_classifier.h5"),
    "bonuses": os.path.join(default_dir, "models", "bonuses.h5"),
}