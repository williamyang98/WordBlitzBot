from PySide2 import QtCore
from PySide2.QtCore import Slot, Signal, Property

import lxml.html
from src.models import DictionarySerialiser

from pprint import pprint

class HTMLDictionaryExtractor:
    def __init__(self, tracer, dictionary):
        self.text = ""
        self.tracer = tracer
        self.dictionary = dictionary

        self.dictionary_filepath = "assets/dictionaries/dictionary.pickle"
        self.dictionary_loader = DictionarySerialiser()

        self.add_word_list = WordList()
        self.removed_word_list = WordList()

    def load_dictionary(self):
        dictionary = self.dictionary_loader.load(self.dictionary_filepath)
        self.dictionary.map = dictionary.map

    def save_dictionary(self):
        self.dictionary_loader.save(self.dictionary, self.dictionary_filepath)

    def get_dictionary_diff(self):
        words = self.extract_words()

        # add words if there are not in dictionary
        add_words = []
        for word in words:
            if not self.dictionary.is_word(word):
                add_words.append(word)
        self.add_word_list.words = add_words
        
        # remove words if they are in the trace list, but not in the dictionary
        removed_words = []
        for trace in self.tracer.traces:
            if trace.word not in words:
                removed_words.append(trace.word)
        self.removed_word_list.words = removed_words
    
    def apply_dictionary_diff(self):
        for word in self.add_word_list.words:
            self.dictionary.add_word(word)
        
        for word in self.removed_word_list.words:
            self.dictionary.remove_word(word)

    def extract_words(self): 
        results_html = lxml.html.fromstring(self.text)
        
        words = {}
        score_board = results_html.cssselect("div.points-result")
        if not score_board:
            return words

        rows = score_board[0]

        for row in rows:
            word = row.cssselect("div.word")[0].text_content().lower()
            points = int(row.cssselect("div.points")[0].cssselect("div.left")[0].text_content())
            words[word] = points
        
        return words

class WordList(QtCore.QAbstractListModel):
    list_size_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._words = []
    
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.words)

    def data(self, index, role):
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return None

        i = index.row()
        try:
            word = self.words[i]
            return word
        except IndexError:
            return None
        return None

    @property
    def words(self):
        return self._words
    
    @words.setter
    def words(self, words):
        self.beginResetModel()
        self._words = words
        self.list_size_changed.emit(len(self._words))
        self.endResetModel()

    @property
    def list_size(self):
        return len(self.words)
    

    