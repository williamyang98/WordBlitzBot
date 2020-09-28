from src.models.dictionary import DictionarySerialiser
from .WordList import WordList

class Extractor:
    # callback = function that takes in html text, and returns list of words
    def __init__(self, tracer, dictionary, config, callback):
        self.text = ""
        self.tracer = tracer
        self.dictionary = dictionary
        self.callback = callback

        self.dictionary_filepath = config["dictionary"]
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
        return self.callback(self.text)
        # raise NotImplementedError("Need to implement BaseExtractor.extract_words in superclass")

