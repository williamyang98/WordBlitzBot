from .SolveResult import SolveResult

class Trace(SolveResult):
    def __init__(self, result):
        super().__init__(result.word, result.path, result.score)
        self.is_complete = False

    def __str__(self):
        return f"{self.word} {self.path} {self.score} {self.is_complete}"
    
    def __repr__(self):
        return self.__str__()