from PySide2 import QtCore

from .Matrix import Matrix
from .Dictionary import Dictionary, DictionarySerialiser
from .Exporter import Exporter
from .Preview import Preview
from .Solver import Solver
from .Tracer import Tracer
from .Analyser import Analyser
from .ScreenRect import ScreenRect
from .HTMLDictionaryExtractor import HTMLDictionaryExtractor

from src.util import load_bounding_boxes

class App(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.matrix = Matrix()

        self.dictionary_loader = DictionarySerialiser()
        self.dictionary = self.dictionary_loader.load("assets/dictionaries/dictionary.pickle")

        bounding_boxes = load_bounding_boxes("assets/bounding_boxes.txt")
        screen_rect = (526, 422, 438, 440)
        screen_rect = ScreenRect(screen_rect)

        self.preview = Preview(bounding_boxes, screen_rect)
        self.solver = Solver(self.dictionary)
        self.analyser = Analyser(self.preview, self.matrix)

        self.tracer = Tracer(self.solver, self.preview, self.matrix)
        self.extractor = HTMLDictionaryExtractor(self.tracer, self.dictionary)

        self.exporter = Exporter(self.tracer, self.preview, self.matrix, self.extractor)

        self.thread_pool = QtCore.QThreadPool(self)





