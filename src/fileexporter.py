# base class for a file exporter

# o - path to the output directory
# d - valid DBManager instance
class FileExporter:
    def __init__(self, o, d):
        self.missing_val_str = '#N/A'
        self.out_dir = o
        self.dbm = d
        self.operation = None

    # this method performs the file format conversion
    # operation. It is recommended to call the
    # __check_format() method before attempting a
    # conversion operation.
    def write(self, table_name):
        print("implement me")

    def set_operation(self, o):
        if not o in ['update', 'create', 'delete']:
            raise RuntimeError("Invalid operation type: " + str(o))
        self.operation = o
