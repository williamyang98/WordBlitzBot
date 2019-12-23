import os
import cv2
import numpy as np
import pandas as pd
import csv

from .SampleFilepathFinder import SampleFilepathFinder
from .ImageDataExportMode import ImageDataExportMode

class Exporter:
    def __init__(self, tracer, preview, matrix, extractor, config):
        self.tracer = tracer
        self.preview = preview
        self.matrix = matrix
        self.extractor = extractor

        self.override = False
        self.config = config["exporter"]

        @ImageDataExportMode.wraps("characters", ["filename", "category"])
        def characters_mode(filename, cell):
            return [filename, cell.char] 
        
        @ImageDataExportMode.wraps("bonuses", ["filename", "category"])
        def bonuses_mode(filename, cell):
            return [filename, cell.bonus] 

        @ImageDataExportMode.wraps("values", ["filename", "total_digits", "left_digit", "right_digit"])
        def values_mode(filename, cell):
            total_digits = 2 if cell.value >= 10 else 1
            left_digit = cell.value // 10
            right_digit = cell.value - (left_digit*10)
            return [filename, total_digits, left_digit, right_digit] 

        self.image_data_modes = [characters_mode, bonuses_mode, values_mode]

    def export_image_data(self):
        image = self.preview.preview
        self.export_sample(image)
        for mode in self.image_data_modes:
            self.export_image_data_type(image, mode)
    
    def export_metadata(self):
        directory_sampler = SampleFilepathFinder(self.config["metadata"]["output_dir"])
        directory = directory_sampler.get_filepath()
        os.makedirs(directory)
        self.export_matrix(directory)
        self.export_traces(directory)
        self.export_results(directory)

    def export_sample(self, image):
        formatter = os.path.join(
            self.config["image_data"]["samples"]["output_dir"],
            self.config["image_data"]["samples"]["filename"])
        sampler = SampleFilepathFinder(formatter)

        filepath = sampler.get_filepath()
        cv2.imwrite(filepath, image)

    def export_image_data_type(self, image, mode):
        fp, writer = self.seed_csv_file(
            self.config["image_data"][mode.name]["labels"], 
            mode.headers)

        directory = self.config["image_data"][mode.name]["output_dir"]
        filename = self.config["image_data"][mode.name]["filename"]
        formatter = os.path.join(directory, filename)

        sampler = SampleFilepathFinder(formatter, self.override)

        boxes = self.preview.bounding_boxes.get(mode.name)
        samples = self.get_ranged_bounding_boxes(image, boxes, variation=1)

        for index in np.ndindex(samples.shape[:2]):
            cell = self.matrix.cells[index]
            sub_samples = samples[index]
            for sample in sub_samples:
                filepath = sampler.get_filepath()
                filename = os.path.basename(filepath)
                cv2.imwrite(filepath, sample)

                writer.writerow(mode.get_row(filepath, cell))

        fp.close()

    # word, path, score 
    def export_traces(self, directory):
        filename = self.config["metadata"]["files"]["traces"]

        traces = self.tracer.traces
        traces_header = ["score", "word", "path"]
        traces_data = []
        for trace in sorted(traces, reverse=True):
            traces_data.append((trace.score, trace.word, trace.path))

        # save scores
        score_dataframe = pd.DataFrame(traces_data, columns=traces_header)
        score_dataframe.to_csv(os.path.join(directory, filename), sep=" ", index=False)

    def export_matrix(self, directory):
        filename = self.config["metadata"]["files"]["matrix"]
        # export the matrix data
        matrix_data = []
        matrix_header = ["index", "character", "value", "bonus"]
        for index, cell in np.ndenumerate(self.matrix.cells):
            value = cell.value
            char = cell.char
            bonus = cell.bonus
            matrix_data.append([index, char, value, bonus])

        matrix_dataframe = pd.DataFrame(matrix_data, columns=matrix_header)
        matrix_dataframe.to_csv(os.path.join(directory, filename), sep=" ", index=False)
    
    def export_results(self, directory):
        filename = self.config["metadata"]["files"]["results"]
        with open(os.path.join(directory, filename), "w+") as fp:
            fp.write(self.extractor.text)

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

    def seed_csv_file(self, filepath, columns):
        # get a csv file
        # if it exists and override, then recreate
        # if it exists and not override, then append
        # if it doesnt exist, create
        create_header = not os.path.exists(filepath) or self.override
        mode = "a" if not self.override else "w+"

        fp = open(filepath, mode)
        writer = csv.writer(fp, delimiter=' ')
        if create_header:
            writer.writerow(columns)
        
        return fp, writer




