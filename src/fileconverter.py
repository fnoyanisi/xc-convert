# base class for a file converter
class FileConverter:
    def __init__(self, f):
        self.missing_val_str = '#N/A'
        self.file_path = f
        self.out_dir = ""

    # this method performs the file format conversion
    # operation. It is recommended to call the
    # __check_format() method before attempting a
    # conversion operation.
    def convert(self, out_dir):
        self.out_dir = out_dir
        print("implement me")

    # a format validator method tht ideally should be called
    # before the convert() method
    # Child classes should implement the checks in this method
    # based on the expected input file format
    def __check_format(self):
        print("implement me")