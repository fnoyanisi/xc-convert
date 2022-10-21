"""
Reads the data from DB and writes into an XML file
"""
from src.exporter.fileexporter import FileExporter
from pathlib import PurePath

import re
import datetime
import src.utils as utils


# o - path to the output directory
# d - valid DBManager instance
class XmlExporter(FileExporter):
    def __init__(self, o, d):
        super().__init__(o, d)

        self.out_dir = o
        self.dbm = d

    def write(self, table_name):
        if self.operation is None:
            raise RuntimeError("Please select the operation type")

        mo_attributes = ['class', 'version', 'distName', 'id']

        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%dT%H-%M-%S')
        out_file_name = table_name.rsplit('_', 1)[0] + '_' + timestamp + '.xmlds'
        path_to_xml_file = PurePath(self.out_dir, out_file_name)

        # try opening the XML file for writing the data
        # the caller should handle the exception
        with open(path_to_xml_file, 'w') as xmlfile:
            # write standard XML information at the top
            xmlfile.write('<?xmlds version="1.0" encoding="UTF-8"?>\n')
            xmlfile.write('<!DOCTYPE raml SYSTEM \'raml20.dtd\'>\n')
            xmlfile.write('<raml version="2.0" xmlns="raml20.xsd">\n')
            xmlfile.write('\t<cmData type="actual">\n')
            xmlfile.write('\t' * 2 + '<header>\n')
            xmlfile.write(
                '\t' * 3 + '<log dateTime="' + now.strftime('%Y-%m-%dT%H:%M:%S') +
                '" action="created" appInfo="ActualExporter">InternalValues are used</log>\n'
            )
            xmlfile.write('\t' * 2 + '</header>\n')

            reader = self.dbm.get_rows(table_name)
            for row in reader:

                # remove non-printable chars from dict keys
                tmp_dict = {}
                for key in row.keys():
                    new_key = utils.remove_non_printable(key)
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
                    if parameter_name not in mo_attributes:
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

    @staticmethod
    def __generate_list(raw_str):
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

        # just in case there is any whitespace characters in the input string
        trimmed = re.sub(' ', '', raw_str)
        for list_item in trimmed.split('};{'):
            # remove any curly brackets
            # tmp has param1=123;param2=456;param3=789 format
            tmp = re.sub('[{}]', '', list_item)

            if ':' in tmp:
                # we have a normal list with key:value pairs
                s = s + '\t'*4 + '<item>\n'
                for i in tmp.split(';'):
                    p,v = i.split(':')
                    s = s + '\t'*5 + '<p name="' + p + '">' + v + '</p>\n'
                s = s + '\t'*4 + '</item>\n'
            else:
                # just values within <p>...</p> tags
                # some values may be of the form
                # <list ...>
                #   <p>xxxx</p>
                #   <p>yyyy</p>
                # </list>
                # and these are captured by the "#rand_name#" placeholder when
                # converting the XML to CSV. These values will appear as
                # xxxx;yyyy
                # in the CSV file, which needs further processing before writing
                if ";" in tmp:
                    arr = tmp.split(";")
                    for a in arr:
                        s = s + '\t'*5 + '<p>' + a + '</p>\n'
                else:
                    s = s + '\t'*5 + '<p>' + tmp + '</p>\n'
        return s
