from schema import Schema, And, Use, Optional, SchemaError
import os

from .defaults import default_dir

image_data_schema = Schema({
    "output_dir": str,
    "labels": str,
    "filename": str,
})

exporter_schema = Schema({
    "image_data": {
        "characters": image_data_schema,
        "bonuses": image_data_schema,
        "values": image_data_schema,
        "samples": {
            "output_dir": str,
            "filename": str,
        }
    },
    "metadata": {
        "output_dir": str,
        "files": {
            "traces": str,
            "matrix": str,
            "results": str,
        }
    }
})

image_data_yaml = {
    "characters": {
        "output_dir": os.path.join(default_dir, "data", "characters"),
        "labels": os.path.join(default_dir, "data", "characters", "labels.txt"),
        "filename": "sample_{i}.png",
    },
    "bonuses": {
        "output_dir": os.path.join(default_dir, "data", "bonuses"),
        "labels": os.path.join(default_dir, "data", "bonuses", "labels.txt"),
        "filename": "sample_{i}.png",
    },
    "values": {
        "output_dir": os.path.join(default_dir, "data", "values"),
        "labels": os.path.join(default_dir, "data", "values", "labels.txt"),
        "filename": "sample_{i}.png",
    },
    "samples": {
        "output_dir": os.path.join(default_dir, "samples"),
        "filename": "sample_{i}.png",
    }
}

metadata_yaml = {
    # directory to place metadata
    "output_dir": os.path.join(default_dir, "data", "traces", "{i}"),
    "files": {
        "traces": "traces.csv",
        "results": "results.html",
        "matrix": "matrix.csv", 
    }
}

exporter_yaml = {
    # where to export image data
    "image_data": image_data_yaml,
    # where to export metadata (matrix, traces, dictionary diff)
    "metadata": metadata_yaml,
}