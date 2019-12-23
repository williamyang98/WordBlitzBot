from schema import Schema, And, Use, Optional, SchemaError
import os

from .models import models_schema, models_yaml 
from .exporter import exporter_schema, exporter_yaml
from .screen_rect import screen_rect_schema, screen_rect_yaml

app_schema = Schema({
    "models": models_schema,
    "dictionary": And(str, os.path.exists),
    "bounding_boxes": And(str, os.path.exists),
    "exporter": exporter_schema,
    "screen_rect": screen_rect_schema, 
})

default_dir = "assets"
default_yaml = {
    "models": models_yaml,
    "dictionary": os.path.join(default_dir, "dictionaries", "dictionary.pickle"),
    "bounding_boxes": os.path.join(default_dir, "bounding_boxes.txt"),
    # exporter directories
    "exporter": exporter_yaml, 
    "screen_rect": screen_rect_yaml,
}