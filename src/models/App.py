from PySide2 import QtCore

from .Preview import Preview
from .Analyser import Analyser
from .HTMLDictionaryExtractor import HTMLDictionaryExtractor

from .exporter import Exporter
from .solver import Solver
from .tracer import Tracer
from .matrix import Matrix
from .dictionary import Dictionary, DictionarySerialiser

from .ScreenRect import ScreenRect

from src.util import load_bounding_boxes

class App(QtCore.QObject):
    def __init__(self, config):
        super().__init__()
        self.config = config
        
        self.matrix = Matrix()

        self.dictionary_loader = DictionarySerialiser()
        self.dictionary = self.dictionary_loader.load(self.config["dictionary"])

        bounding_boxes = load_bounding_boxes(self.config["bounding_boxes"])
        screen_rect = (526, 422, 438, 440)
        screen_rect = ScreenRect(screen_rect)

        self.preview = Preview(bounding_boxes, screen_rect)
        self.solver = Solver(self.dictionary)
        self.analyser = Analyser(self.preview, self.matrix, self.config)

        self.tracer = Tracer(self.solver, self.preview, self.matrix)
        self.extractor = HTMLDictionaryExtractor(self.tracer, self.dictionary, self.config)

        self.exporter = Exporter(self.tracer, self.preview, self.matrix, self.extractor, self.config)

        self.thread_pool = QtCore.QThreadPool(self)





