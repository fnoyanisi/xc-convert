"""
Base class for a file exporter

Copyright (c) 2017-2022 Fehmi Noyan ISI. All rights reserved.
See the LICENSE file for the end user license agreement.
"""


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
        if o not in ['update', 'create', 'delete']:
            raise RuntimeError("Invalid operation type: " + str(o))
        self.operation = o
