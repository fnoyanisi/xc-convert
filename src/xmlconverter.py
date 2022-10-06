"""
Converts an XML file to
    - CSV
"""
from pathlib import PurePath
import csv, datetime
from xml.dom import minidom

import xml
import random

from fileconverter import FileConverter
from managedobject import ManagedObject
from list import List
from item import Item


class XmlConverter(FileConverter):
    headers = {}    # 'managedObject class' : [list of available parameters]
    doc = None      # XML doc object

    def __init__(self, f):
        super().__init__(f)
        self.__check_format()   # format validation

    def convert(self, out_dir):
        """
        This method converts an XML file to one or several CSV files
        depending on the number of managedObject classes in the XML file.
        """

        self.out_dir = out_dir
        self.headers = {}

        # step 1
        # create the headers dictionary
        list_of_managedObjects = self.doc.getElementsByTagName("managedObject")

        for mo in list_of_managedObjects:
            mo_class = mo.getAttribute("class")
            if mo_class not in self.headers:
                # if this mo_class does not exist, create a new entry in the
                # dictionary with managedObject class being the key and an
                # empty list as the value
                self.headers[mo_class] = []

            # for the list items, a set of curly brackets is appended at the end
            # of the parameter name
            for p in mo.childNodes:
                if p.nodeName == 'p' or p.nodeName == 'list':
                    parameter_name = p.getAttribute("name")
                    if p.nodeName == 'list':
                        parameter_name = parameter_name + '{}'
                    if not parameter_name in self.headers[mo_class]:
                        self.headers[mo_class].append(parameter_name)

        # step 2
        # perform the XML to CSV conversion operation
        for mo_class in self.headers:
            # full path for the CSV file - append a date like 20210813 at the end
            now = datetime.datetime.now()
            timestamp = now.strftime('%Y-%m-%dT%H-%M-%S')
            out_file_name = mo_class + "-" + str(timestamp) + '.csv'
            path_to_csv_file = PurePath(self.out_dir, out_file_name)

            # a header for the CSV file
            # add some additional attributes from managedObject node
            # to the beginning of the list containing the parameter names
            csv_header = self.headers.get(mo_class)
            csv_header.insert(0, 'class')
            csv_header.insert(1, 'version')
            csv_header.insert(2, 'distName')
            csv_header.insert(3, 'id')

            # Open the CSV file and write the data in to it
            with open(path_to_csv_file, 'w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=csv_header, restval=self.missing_val_str)

                # write the header line into the CSV file
                writer.writeheader()

                # OK, now iterate through the managedObject list and write a separate CSV file for
                # each one.
                # If the input XML includes data for different managedObject classes,
                # a separate CSV file will be created for each one of them
                for mo_entry in list_of_managedObjects:
                    if mo_entry.getAttribute("class") == mo_class:
                        mo = ManagedObject(mo_class,
                                           mo_entry.getAttribute("version"),
                                           mo_entry.getAttribute("distName"),
                                           mo_entry.getAttribute("id")
                                           )

                        # now, get the rest of the parameters
                        for p in mo_entry.childNodes:
                            if p.nodeName == 'p':
                                # a usual node like <p name="..."> blah </p>
                                mo.add_property(p.getAttribute("name"), p.firstChild.data)
                            elif p.nodeName == 'list':
                                # we have a list to process
                                list_entry = self.__read_list(p)
                                mo.add_property(list_entry.name, list_entry)
                            else:
                                # I don't know what this entry is, so skipping
                                pass

                        # write the object into the CSV file
                        writer.writerow(mo.get_values())

    """
    This function converts an XML list, whose structure is given below,
    to a List object

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

    :param node_p: valid XML node
    :return: a List object representing the list entry in the XML file
    """
    def __read_list(self, node_p):
        mo_list = List(node_p.getAttribute("name"))

        # string are immutable, so use a list, and then join()
        for item in node_p.childNodes:
            if item.nodeName == 'item':
                item_node = self.__read_item(item)
                mo_list.add_property(item_node.name, item_node)
            elif item.nodeName == 'p':
                for item_p in item.childNodes:
                    # use a random name for parameter values without a name
                    # to avoid consecutive values overwriting on each other
                    n = "#rand_name#" + str(random.randint(0, 1000000000))
                    mo_list.add_property(n, item_p.data)
        return mo_list

    """
    Iterates over an "item" node and creates the relevant
    object
            +--item1
            |
            +--p1 name='...'
            |
            +--p2 name='...'
    """
    def __read_item(self, node_p):
        item = Item()
        for item_elem in node_p.childNodes:
            if item_elem.nodeName == 'p':
                # normal property
                item.add_property(item_elem.getAttribute("name"), item_elem.firstChild.data)
            elif item_elem.nodeName == 'list':
                # nested list
                inner_list = self.__read_list(item_elem)
                item.add_property(inner_list.name, inner_list)
            else:
                # unknown node type, skip
                pass
        return item

    """
    Validate the XML file format

    This method checks whether the inout XML file has a supported file format.
    Expected XML DOM :
    raml
      |
      +--cmData
           |
           +--managedObject

    :param xml_doc: a valid XML document object returned by minidom.parse()
    :return: True if the file format is valid, False otherwise
    """
    def __check_format(self):
        # check 1
        # can the XML parser work on the file?
        try:
            self.doc = minidom.parse(self.file_path)
        except xml.parsers.expat.ExpatError as e:
            raise RuntimeError("Unsupported XML format")

        # check 2
        # check the DOM
        raml_nodes = self.doc.getElementsByTagName("raml")
        if raml_nodes is None or not raml_nodes[0].hasChildNodes():
            raise RuntimeError("Unsupported XML format")

        # check 3
        # find cmData
        cmData_node = None
        for cmData_node in raml_nodes[0].childNodes:
            if cmData_node.nodeName == "cmData":
                break
            else:
                cmData_node = None

        if cmData_node is None or not cmData_node.hasChildNodes():
            raise RuntimeError("Unsupported XML format")

        # check 4
        # at least one managedObject node must exist
        mo_node = None
        for mo_node in cmData_node.childNodes:
            if mo_node.nodeName == "managedObject":
                break
            else:
                mo_node = None

        if mo_node is None or not mo_node.hasChildNodes():
            raise RuntimeError("Unsupported XML format")