# Representation of our dictionary
# stores string/boolean pairs
# boolean represents if the word is a just a branch or a complete word
# this is so we can determine if we use a key inside the dictionary as a word
# dict[just a branch] = False
# dict[word and maybe also a branch] = True

# we explore the dictionary in a tree-like manner by exploring its children
class Dictionary:
    def __init__(self, mapping={}):
        self.map = mapping

    def add_word(self, word):
        for i in range(len(word)):
            branch = word[:i]
            self.map.setdefault(branch, False)
        
        self.map[word] = True

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

        # TODO: add multilanguage support
        # by extending with more branches to search
        # or by introducting an additional lookup to keep track of number of children
        for i in range(ord('a'), ord('z')+1):
        # for i in range(ord('a'), ord('z')+1):
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
    
