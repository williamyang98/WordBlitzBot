import pickle

class Dictionary:
    def __init__(self, mapping={}):
        self.map = mapping

    def add_word(self, word):
        for i in range(len(word)):
            branch = word[:i]
            self.map.setdefault(branch, False)
        
        self.map.setdefault(word, True)

    def remove_word(self, word):
        # if word not in, then do nothing
        if not word in self.map:
            return False
        
        is_word = self.map[word]
        # if branch, do nothing
        if not is_word:
            return False

        # if it is a word, check that it has no branches, and remove
        self.map[word] = False 
        for i in range(ord('a'), ord('z')+1):
            c = chr(i)
            branch = word+c
            if self.is_branch(branch):
                break
        # if no branches, then just remove
        else:
            self.map.pop(word)

    def is_branch(self, word):
        return word in self.map

    def is_word(self, word):
        return self.is_branch(word) and self.map[word] is True
    
class DictionarySerialiser:

    def save(self, dictionary, path):
        with open(path, 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(dictionary, f, pickle.HIGHEST_PROTOCOL)
    
    def load(self, path):
        with open(path, 'rb') as f:
            mapping = pickle.load(f)
            dictionary = Dictionary(mapping)
            return dictionary
            