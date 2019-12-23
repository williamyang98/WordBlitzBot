import os

class SampleFilepathFinder:
    def __init__(self, formatter, override=False):
        self.formatter = formatter
        self.override = override
        self.index = 0

    def get_filepath(self):
        if not self.override:
            while os.path.exists(self.formatter.format(i=self.index)):
                self.index += 1
        else:
            self.index += 1
        
        return self.formatter.format(i=self.index)