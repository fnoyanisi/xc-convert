from fileconverter import FileConverter


class CsvConverter(FileConverter):
    def __init__(self, f):
        super().__init__(f)
