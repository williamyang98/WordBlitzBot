class WordTree:
    def __init__(self, parent=None):
        self.leafs = {}
        self.word = None
        self.parent = parent

    def add_word(self, word):
        self.attach_word(word, word)

    def attach_word(self, branch, word):
        if not branch:
            return

        head = branch[0]
        body = branch[1:]
        child = self.leafs.setdefault(head, WordTree(parent=self))
        if body:
            child.attach_word(body, word)
        else:
            child.word = word
    
    def get_leaf(self, word):
        if not word:
            return None

        head = word[0]
        body = word[1:]
        
        child = self.leafs.get(head, None)
        if not child:
            return None
        if body:
            return child.get_leaf(body)
        return child
