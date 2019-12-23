from schema import Schema, And, Use, Optional, SchemaError
import os

rect_field_schema = And(Use(int), lambda x: x >= 0) 

screen_rect_schema = Schema({
    "left": rect_field_schema, 
    "top": rect_field_schema, 
    "width": rect_field_schema, 
    "height": rect_field_schema, 
})

screen_rect_yaml = {
    "left": 526, 
    "top": 422,
    "width": 438,
    "height": 440,
}