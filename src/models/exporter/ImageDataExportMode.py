class ImageDataExportMode:
    @staticmethod
    def wraps(name, headers):
        def decorator(func):
            return ImageDataExportMode(name, headers, func)
        return decorator

    def __init__(self, name, headers, row_func):
        self.name = name
        self.headers = headers
        self.row_func = row_func
    
    def get_row(self, filepath, cell):
        return self.row_func(filepath, cell)