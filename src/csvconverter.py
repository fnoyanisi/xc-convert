from fileconverter import FileConverter
from pathlib import PurePath

import datetime
import re
import csv
import helperfunctions


class CsvConverter(FileConverter):
    def __init__(self, f):
        super().__init__(f)
        self.operation = 'none'
        self.__check_format()  # format validation

    def set_operation(self, o):
        if not o in ['update','create','delete']:
            raise RuntimeError("Invalid operation type: " + str(o))
        self.operation = o

    def convert(self, out_dir):
        """
        This function converts a valid CSV file to an XML
        """

        if self.operation == 'none':
            raise RuntimeError("Please select the operation type")

        self.out_dir = out_dir
        csv_file = self.file_path
        mo_attributes = ['class', 'version', 'distName', 'id']

        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%dT%H-%M-%S')
        out_file_name = re.sub('.csv', '', PurePath(csv_file).name) + '-' + timestamp + '.xml'
        xml_file = PurePath(out_dir, out_file_name)

        # try opening the XML file for writing and the CSV file
        # for reading.
        # the caller should handle the exception
        with open(xml_file, 'w') as xmlfile, open(csv_file, 'r') as csvfile:

            # write standard XML information at the top
            xmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            xmlfile.write('<!DOCTYPE raml SYSTEM \'raml20.dtd\'>\n')
            xmlfile.write('<raml version="2.0" xmlns="raml20.xsd">\n')
            xmlfile.write('\t<cmData type="actual">\n')
            xmlfile.write('\t' * 2 + '<header>\n')
            xmlfile.write(
                '\t' * 3 + '<log dateTime="' + now.strftime('%Y-%m-%dT%H:%M:%S') + '" action="created" appInfo="ActualExporter">InternalValues are used</log>\n')
            xmlfile.write('\t' * 2 + '</header>\n')

            reader = csv.DictReader(csvfile)
            for row in reader:

                # remove non-printable chars from dict keys
                tmp_dict = {}
                for key in row.keys():
                    new_key = helperfunctions.removeNonPrintable(key)
                    if not new_key == key:
                        tmp_dict[key] = new_key

                for old_key in tmp_dict.keys():
                    row[tmp_dict[old_key]] = row.pop(old_key)

                # the Managed Object node is of the form
                # <managedObject class="MRBTS" version="FL16" distName="PLMN-PLMN/MRBTS-1111/LNBTS-1111" id="1111111">
                mo_line = '\t' * 2 + '<managedObject class="' + row[
                    'class'] + '" operation="' + self.operation + '" version="' + row['version'] + '" distName="' + row[
                              'distName'] + '" id="' + row['id'] + '">\n'
                xmlfile.write(mo_line)

                # rest of the parameters
                for parameter_name in row:
                    if not parameter_name in mo_attributes:
                        if row[parameter_name] == self.missing_val_str:
                            # This parameter is not available for this managedObject
                            continue
                        elif '{}' in parameter_name:
                            # a list
                            xmlfile.write('\t' * 3 + '<list name="' + re.sub('{}', '', parameter_name) + '">\n')
                            xmlfile.write(self.__generate_list(row[parameter_name]))
                            xmlfile.write('\t' * 3 + '</list>\n')
                        else:
                            # formal <p..> .. </p>
                            xmlfile.write(
                                '\t' * 3 + '<p name="' + parameter_name + '">' + row[parameter_name] + '</p>\n')

                xmlfile.write('\t' * 2 + '</managedObject>\n')

            # standard XML information
            xmlfile.write('\t</cmData>\n')
            xmlfile.write('</raml>\n')

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
            csv_columns = header.split(',')

        # make sure csv_values is not shorter than test_values
        # and the CSV file has all the necessary fields in it
        if len(csv_columns) < len(required_columns) or required_columns != csv_columns[:len(required_columns)]:
            raise RuntimeError("Unsupported CSV format")

    def __generate_list(self, raw_str):
        """
        This functions converts a string which is of {param1=123;param2=456}{param1=789;param2=000}
        format into given XML tree

         list name='....'
           |
           +--item1
           |   |
           |   +--p1 name='...'
           |   |
           |   +--p2 name='...'
           |
           +--item2
           |   |
           |   +--p1 name='...'
           |   |
           |   +--p2 name='...'

        :param raw_str: string value
        :return: generated string for the list structure
        """
        s = ''

        # just in case there is nay whitespace characters in the input string
        trimmed = re.sub(' ','',raw_str)
        for list_item in trimmed.split('}{'):
            # remove any curly brackets
            # tmp has param1=123;param2=456;param3=789 format
            tmp = re.sub('[{}]','',list_item)

            if ':' in tmp:
                # so, we have a normal list with key:value pairs
                s = s.join('\t'*4 + '<list>\n')
                for i in tmp.split(';'):
                    p,v = i.split(':')
                    s = s.join('\t'*5 + '<p name="' + p + '">' + v + '</p>\n')
                s = s.join('\t'*4 + '</list>\n')
            else:
                # just values within <p>...</p> tags
                s = s.join('\t'*5 + '<p>' + tmp + '</p>\n')

        return s