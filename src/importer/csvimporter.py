"""
Reads a CSV file into the database
"""
from importer.fileimporter import FileImporter
from pathlib import PurePath

import csv
import src.utils as utils


class CsvImporter(FileImporter):
    table_name = ""

    def __init__(self, f, d):
        super().__init__(f, d)

        # each CSV file is represented by a table in the DB
        # example-file.csv is stored in example_table_csv table
        self.table_name = PurePath(self.file_path).name.replace('.', '_').replace('-', '_')

        self.operation = 'none'
        self.__check_format()  # format validation

    # read the CSV file into the database
    # returns the name of the table that the file is
    # imported into
    def read(self):
        csv_file = self.file_path
        with open(csv_file, 'r') as csvfile:
            # DictReader provides a convenient API to read the CSV file
            # each returned row is in the form of
            # row[header] = value
            reader = csv.DictReader(csvfile)
            self.dbm.create_table(self.table_name, reader.fieldnames)
            self.dbm.insert_values(self.table_name, reader)
        return self.table_name

    def __check_format(self):
        # check 1
        # open file
        try:
            with open(self.file_path) as csvfile:
                header = csvfile.readline()
        except OSError as e:
            raise RuntimeError(e.strerror)

        # check 2
        # empty header
        if len(header) == 0:
            raise RuntimeError("Unsupported CSV format")

        # check 3
        # required columns
        # these are the attributes (or column names in the CSV file) that
        # any CVS file has to have
        required_columns = ['class', 'version', 'distName', 'id']
        csv_columns = []

        # remove non-printable characters
        header = utils.remove_non_printable(header)

        if ',' not in header:
            raise RuntimeError("Unsupported CSV format")
        else:
            csv_columns = header.split(',')

        # make sure csv_values is not shorter than test_values
        # and the CSV file has all the necessary fields in it
        if len(csv_columns) < len(required_columns) or required_columns != csv_columns[:len(required_columns)]:
            raise RuntimeError("Unsupported CSV format")

