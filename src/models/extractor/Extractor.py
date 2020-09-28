from PySide2.QtCore import QObject, Property, Slot, Signal
from PySide2 import QtCore

from src.models.dictionary import DictionarySerialiser
from .WordList import WordList

class Extractor(QObject):
    dictionary_changed = Signal(bool)

    # callback = function that takes in html text, and returns list of words
    def __init__(self, tracer, dictionary, config, callback):
        super().__init__()
        self.text = ""
        self.tracer = tracer
        self.dictionary = dictionary
        self.callback = callback

        self.dictionary_filepath = config["dictionary"]
        self.dictionary_loader = DictionarySerialiser()

        self.trace_word_list = WordList()
        self.extracted_word_list = WordList()
        self.add_word_list = WordList()
        self.removed_word_list = WordList()

    def load_dictionary(self):
        dictionary = self.dictionary_loader.load(self.dictionary_filepath)
        self.dictionary.map = dictionary.map
        self.dictionary_changed.emit(False)

    def save_dictionary(self):
        self.dictionary_loader.save(self.dictionary, self.dictionary_filepath)
        self.dictionary_changed.emit(False)

    def get_dictionary_diff(self):
        words = self.extract_words()
        words = set(words)

        self.extracted_word_list.words = list(words)

        # add words if there are not in dictionary
        add_words = []
        for word in words:
            if not self.dictionary.is_word(word):
                add_words.append(word)
        self.add_word_list.words = add_words
        
        # remove words if they are in the trace list, and in the dictionary
        removed_words = []
        for trace in self.tracer.traces:
            if trace.word not in words and self.dictionary.is_word(trace.word):
                removed_words.append(trace.word)
        self.removed_word_list.words = removed_words

        self.trace_word_list.words = [trace.word for trace in self.tracer.traces]
    
    def apply_dictionary_diff(self):
        n_changes = len(self.add_word_list.words) + len(self.removed_word_list.words)
        
        for word in self.add_word_list.words:
            self.dictionary.add_word(word)
        
        for word in self.removed_word_list.words:
            self.dictionary.remove_word(word)
        
        self.add_word_list.words = []
        self.removed_word_list.words = []

        self.dictionary_changed.emit(n_changes > 0)
        
    def extract_words(self): 
        return self.callback(self.text)
        # raise NotImplementedError("Need to implement BaseExtractor.extract_words in superclass")

