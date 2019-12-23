import pickle
from .Dictionary import Dictionary

class DictionarySerialiser:

    def save(self, dictionary, path):
        with open(path, 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(dictionary.map, f, pickle.HIGHEST_PROTOCOL)
    
    def load(self, path):
        with open(path, 'rb') as f:
            mapping = pickle.load(f)
            dictionary = Dictionary(mapping)
            return dictionary