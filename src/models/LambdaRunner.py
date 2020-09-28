from PySide2 import QtCore

class LambdaRunner(QtCore.QRunnable):
    def __init__(self, runner):
        super().__init__()
        self.runner = runner
    
    def run(self):
        self.runner()

    def autoDelete(self):
        return True