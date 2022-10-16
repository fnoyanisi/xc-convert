from xml.dom import minidom

import xml
import random

from fileimporter import FileImporter
from managedobject import ManagedObject
from list import List
from item import Item


class XmlImporter(FileImporter):
    # keeps a list of all the parameters available under each
    # managedObject class in the form of a dict
    # 'managedObject class' : [list of available parameters]
    mo_parameters = None
    doc = None  # XML doc object

    def __init__(self, f, d):
        super().__init__(f, d)
        self.__check_format()  # format validation

    def read(self):
        self.mo_parameters = {}

        list_of_managedObjects = self.__populate_parameters()

        # perform the XML to CSV conversion operation
        for mo_class in self.mo_parameters:
            # column_names is a list of parameters which the current
            # mo_class has
            # we add some standard columns to the list manually
            column_names = self.mo_parameters.get(mo_class)
            column_names.insert(0, 'class')
            column_names.insert(1, 'version')
            column_names.insert(2, 'distName')
            column_names.insert(3, 'id')

            # create a table in DB for each managedObject class
            self.dbm.create_table(mo_class, column_names)

            # iterate through the managedObject and update DB with the values
            for mo_entry in list_of_managedObjects:
                values = []
                if mo_entry.getAttribute("class") == mo_class:
                    mo = ManagedObject(mo_class,
                                       mo_entry.getAttribute("version"),
                                       mo_entry.getAttribute("distName"),
                                       mo_entry.getAttribute("id")
                                       )

                    # get the rest of the parameters
                    for p in mo_entry.childNodes:
                        if p.nodeName == 'p':
                            # a usual node like <p name="..."> blah </p>
                            mo.add_property(p.getAttribute("name"), p.firstChild.data)
                        elif p.nodeName == 'list':
                            # we have a list to process
                            list_entry = self.__read_list(p)
                            mo.add_property(list_entry.name, list_entry)
                        else:
                            # don't know what this entry is, skipping
                            pass

                    values.append(mo.get_values())

                # write the entry into the DB
                self.dbm.insert_values(mo_class, values)

    # method to populate self.headers dictionary and returns a list of
    # all the managed objects
    def __populate_parameters(self):
        # list_of_managedObjects is the list of all managedObjects in the XML file
        list_of_managedObjects = self.doc.getElementsByTagName("managedObject")

        for mo in list_of_managedObjects:
            mo_class = mo.getAttribute("class")
            if mo_class not in self.mo_parameters:
                # if this mo_class does not exist, create a new entry in the
                # dictionary with managedObject class being the key and an
                # empty list as the value
                self.mo_parameters[mo_class] = []

            # for the list items, a set of curly brackets is appended
            # at the end of the parameter name
            for p in mo.childNodes:
                if p.nodeName == 'p' or p.nodeName == 'list':
                    parameter_name = p.getAttribute("name")
                    if p.nodeName == 'list':
                        parameter_name = parameter_name + '{}'
                    if parameter_name not in self.mo_parameters[mo_class]:
                        self.mo_parameters[mo_class].append(parameter_name)
        return list_of_managedObjects

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