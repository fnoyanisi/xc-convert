# base class for a file converter
class FileConverter:
    def __init__(self, f):
        self.file_path = f
        self.out_dir = ""

    def convert(self, out_dir):
        self.out_dir = out_dir
        print("implement me")

