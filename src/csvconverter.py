from fileconverter import FileConverter

import helperfunctions


class CsvConverter(FileConverter):
    def __init__(self, f):
        super().__init__(f)
        self.__check_format()  # format validation

    def convert(self):
        pass

    def __check_format(self):
        header = ''

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
        header = helperfunctions.removeNonPrintable(header)

        if not ',' in header:
            raise RuntimeError("Unsupported CSV format")
        else:
            csv_values = header.split(',')

        # make sure csv_values is not shorter than test_values
        # and the CSV file has all the necessary fields in it
        if len(csv_columns) < len(required_columns) or required_columns != csv_columns[:len(required_columns)]:
            raise RuntimeError("Unsupported CSV format")