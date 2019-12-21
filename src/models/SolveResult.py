from functools import total_ordering

@total_ordering
class SolveResult:
    def __init__(self, word, path, score):
        self.word = word
        self.path = path
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score
    
    def __eq__(self, other):
        return self.score == other.score