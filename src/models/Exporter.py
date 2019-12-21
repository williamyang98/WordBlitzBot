import os
import cv2
import numpy as np
import pandas as pd
import csv

class Exporter:
    def __init__(self, tracer, preview, matrix, extractor):
        self.tracer = tracer
        self.preview = preview
        self.matrix = matrix
        self.extractor = extractor

        self.override = False
        self.directory = "assets/"

    def export_image_data(self):
        image = self.preview.preview
        self.export_samples(image)
        self.export_characters(image)
        self.export_bonuses(image)
        self.export_values(image)

    
    def export_metadata(self):
        directory_sampler = SampleFilepathFinder(os.path.join(self.directory, "data", "traces", "{i}"))
        directory = directory_sampler.get_filepath()
        os.makedirs(directory)
        self.export_matrix(directory)
        self.export_traces(directory)
        self.export_results(directory)

    def export_samples(self, image, ext="png"):
        formatter = os.path.join(self.directory, "samples", f"sample_{{i}}.{ext}")
        sampler = SampleFilepathFinder(formatter)

        filepath = sampler.get_filepath()
        cv2.imwrite(filepath, image)

    def export_characters(self, image, ext="png"):
        directory = os.path.join(self.directory, "data/characters")
        fp, writer = self.seed_csv_file(
            os.path.join(directory, "labels.txt"), 
            ["filename", "category"])

        formatter = os.path.join(directory, f"sample_{{i}}.{ext}")
        sampler = SampleFilepathFinder(formatter, self.override)

        boxes = self.preview.bounding_boxes.get("characters")
        samples = self.get_ranged_bounding_boxes(image, boxes, variation=1)

        for index in np.ndindex(samples.shape[:2]):
            cell = self.matrix.cells[index]
            sub_samples = samples[index]
            for sample in sub_samples:
                filepath = sampler.get_filepath()
                filename = os.path.basename(filepath)
                cv2.imwrite(filepath, sample)
                writer.writerow([filename, cell.char])

        fp.close()
    
    def export_bonuses(self, image, ext="png"):
        directory = os.path.join(self.directory, "data/bonuses")
        fp, writer = self.seed_csv_file(
            os.path.join(directory, "labels.txt"), 
            ["filename", "category"])

        formatter = os.path.join(directory, f"sample_{{i}}.{ext}")
        sampler = SampleFilepathFinder(formatter, self.override)

        boxes = self.preview.bounding_boxes.get("bonuses")
        samples = self.get_ranged_bounding_boxes(image, boxes, variation=1)

        for index in np.ndindex(samples.shape[:2]):
            cell = self.matrix.cells[index]
            sub_samples = samples[index]
            for sample in sub_samples:
                filepath = sampler.get_filepath()
                filename = os.path.basename(filepath)
                cv2.imwrite(filepath, sample)
                writer.writerow([filename, cell.bonus])

        fp.close()

    def export_values(self, image, ext="png"):
        directory = os.path.join(self.directory, "data/values")
        fp, writer = self.seed_csv_file(
            os.path.join(directory, "labels.txt"), 
            ["filename", "total_digits", "left_digit", "right_digit"])

        formatter = os.path.join(directory, f"sample_{{i}}.{ext}")
        sampler = SampleFilepathFinder(formatter, self.override)

        boxes = self.preview.bounding_boxes.get("values")
        samples = self.get_ranged_bounding_boxes(image, boxes, variation=1)

        for index in np.ndindex(samples.shape[:2]):
            cell = self.matrix.cells[index]
            sub_samples = samples[index]
            for sample in sub_samples:
                filepath = sampler.get_filepath()
                filename = os.path.basename(filepath)
                cv2.imwrite(filepath, sample)

                total_digits = 2 if cell.value >= 10 else 1
                left_digit = cell.value // 10
                right_digit = cell.value - (left_digit*10)
                writer.writerow([filename, total_digits, left_digit, right_digit])

        fp.close()

    # word, path, score 
    def export_traces(self, directory):
        traces = self.tracer.traces
        traces_header = ["score", "word", "path"]
        traces_data = []
        for trace in sorted(traces, reverse=True):
            traces_data.append((trace.score, trace.word, trace.path))

        # save scores
        score_dataframe = pd.DataFrame(traces_data, columns=traces_header)
        score_dataframe.to_csv(os.path.join(directory, "paths.csv"), sep=" ", index=False)

    def export_matrix(self, directory):
        # export the matrix data
        matrix_data = []
        matrix_header = ["index", "character", "value", "bonus"]
        for index, cell in np.ndenumerate(self.matrix.cells):
            value = cell.value
            char = cell.char
            bonus = cell.bonus
            matrix_data.append([index, char, value, bonus])

        matrix_dataframe = pd.DataFrame(matrix_data, columns=matrix_header)
        matrix_dataframe.to_csv(os.path.join(directory, "matrix.csv"), sep=" ", index=False)
    
    def export_results(self, directory):
        with open(os.path.join(directory, "results.html"), "w+") as fp:
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


class SampleFilepathFinder:
    def __init__(self, formatter, override=False):
        self.formatter = formatter
        self.override = override
        self.index = 0

    def get_filepath(self):
        if not self.override:
            while os.path.exists(self.formatter.format(i=self.index)):
                self.index += 1
        else:
            self.index += 1
        
        return self.formatter.format(i=self.index)