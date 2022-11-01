"""
Base class for a file importer

Copyright (c) 2017-2022 Fehmi Noyan ISI. All rights reserved.
See the LICENSE file for the end user license agreement.
"""


# f - path to the import file
# d - valid DBManager instance
class FileImporter:
    def __init__(self, f, d):
        self.missing_val_str = '#N/A'
        self.file_path = f
        self.dbm = d

    # this method performs the file format conversion
    # operation. It is recommended to call the
    # __check_format() method before attempting a
    # conversion operation.
    def read(self):
        print("implement me")

    # a format validator method tht ideally should be called
    # before the convert() method
    # Child classes should implement the checks in this method
    # based on the expected input file format
    def __check_format(self):
        print("implement me")
