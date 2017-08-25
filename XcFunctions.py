from pathlib import PurePath
from xml.dom import minidom
import HelperFunctions
import csv, re, datetime

# This is the string to be used if a parameter is missing for the current managedObject
rest_val_str = '#N/A'

def examineXmlFormat(xml_doc):
    """
    This function checks whether the inout XML file has a supported file format.
    Expected XML DOM :
    raml
      |
      +--cmData
           |
           +--managedObject

    :param xml_doc: a valid XML document object returned by minidom.parse()
    :return: True if the file format is valid, False otherwise
    """
    raml_nodes = xml_doc.getElementsByTagName("raml")
    if raml_nodes == None or not raml_nodes[0].hasChildNodes():
        return False

    # find cmData
    for cmData_node in raml_nodes[0].childNodes:
        if cmData_node.nodeName == "cmData":
            break
        else:
            cmData_node = None

    if cmData_node == None or not cmData_node.hasChildNodes():
        return False

    # at least one managedObject node must exist
    for mo_node in cmData_node.childNodes:
        if mo_node.nodeName == "managedObject":
            break
        else:
            mo_node = None

    if mo_node == None or not mo_node.hasChildNodes():
        return False

    return True

def createManagedObjectDict(xml_doc):
    """
    This function finds managedObject nodes in the XML file and
    creates a dictionary for each managedObject class

    :param xml_doc: a valid XML document object returned by minidom.parse()
    :return: a dictionary containing a list of available parameters for each
             managedObject class
    """
    mo_list = xml_doc.getElementsByTagName("managedObject")

    # 'managedObject class' : [list of available parameters]
    header = {}

    for mo in mo_list:
        mo_class = mo.getAttribute("class")
        if not mo_class in header:
            # if this mo_class does not exist, create a new entry in the
            # dictionary with managedObject class being the key and an
            # empty list as the value
            header[mo_class]=[]

        # for list items, a set of curly brackets is appended at the end
        # of the parameter name
        for p in mo.childNodes:
            if p.nodeName == 'p' or p.nodeName == 'list':
                parameter_name = p.getAttribute("name")
                if p.nodeName == 'list':
                    parameter_name = parameter_name + '{}'
                if not parameter_name in header[mo_class]:
                    header[mo_class].append(parameter_name)

    return header

def convertXmlToCsv(xml_doc, csv_path, header_dict):
    """
    This function converts an XML file to one or several CSV files
    depending on the number of managedObject classes in the XML file.

    :param xml_doc: a valid XML document object returned by minidom.parse()
    :param csv_path: path to output CSV file
    :param header_dict: a dictionary retrned by createManagedObjectDict()
    :return: no value is returned
    """
    mo_list = xml_doc.getElementsByTagName("managedObject")

    # header_dict -> 'managedObject class' : [list of available parameters]
    for mo_class in header_dict:
        #full path for the CSV file
        path_to_csv_file = PurePath(csv_path, mo_class + '.csv')

        # a header for the CSV file
        # add some additional attributes from managedObject node
        # to the begining of the list containing the parameter names
        csv_header= header_dict.get(mo_class)
        csv_header.insert(0,'class')
        csv_header.insert(1,'version')
        csv_header.insert(2,'distName')
        csv_header.insert(3,'id')

        # Open the CSV file and write the data in it
        with open(path_to_csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_header, restval=rest_val_str)

            writer.writeheader()

            for mo in mo_list:
                if mo.getAttribute("class") == mo_class:
                    parameter_dict = {}

                    # attributes for mamangedObject
                    parameter_dict['class']=mo_class
                    parameter_dict['version'] = mo.getAttribute("version")
                    parameter_dict['distName'] = mo.getAttribute("distName")
                    parameter_dict['id'] = mo.getAttribute("id")

                    # rest of the parameters
                    for p in mo.childNodes:
                        if p.nodeName == 'p':
                            parameter_name = p.getAttribute("name")
                            parameter_value = p.firstChild.data
                            parameter_dict[parameter_name] = parameter_value
                        elif p.nodeName == 'list':
                            t=()
                            t = HelperFunctions.listXml2Csv(p)
                            parameter_dict[t[0]] = t[1]
                        else:
                            pass

                    # write into the CSV file
                    writer.writerow(parameter_dict)

def examineCsvFormat(csv_file):
    """
    This function checks whether the input CSV file has a recognized format

    :param csv_file: path to CSV file
    :return: True if the file format is okay, False otherwise
    """

    header=''
    try:
        with open(csv_file) as csvfile:
            header = csvfile.readline()
    except OSError:
        return False

    if len(header) == 0:
        return False

    # these are the attributes (or column names in the CSV file) that
    # any CVS file has to have in order to be converted into an XML
    test_values = ['class','version','distName','id']
    csv_values = []

    if not ',' in header:
        return False
    else:
        csv_values = header.split(',')

    # make sure csv_values is not shorter than test_values
    # and the CSV file has all the necessary fields in it
    if len(csv_values) < len(test_values) or test_values != csv_values[:len(test_values)]:
        return False

    return True

def convertCsv2Xml(csv_file, xml_file):
    """
    This function converts a valid CSV file to an XML

    :param csv_file: path to input CSV file
    :param xml_file: path to output XML file
    :return: No value is returned
    """
    mo_attributes = ['class', 'version', 'distName', 'id']

    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%dT%H:%M:%S')

    # try opening the XML file for writing and the CSV file
    # for reading.
    # the caller should handle the exception
    with open(xml_file,'w') as xmlfile, open(csv_file,'r') as csvfile:

        # write standard XML information at the top
        xmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        xmlfile.write('<!DOCTYPE raml SYSTEM \'raml20.dtd\'>\n')
        xmlfile.write('<raml version="2.0" xmlns="raml20.xsd">\n')
        xmlfile.write('\t<cmData type="actual">\n')
        xmlfile.write('\t'*2 + '<header>\n')
        xmlfile.write('\t'*3 + '<log dateTime="' + timestamp +'" action="created" appInfo="ActualExporter">InternalValues are used</log>\n')
        xmlfile.write('\t'*2 + '</header>\n')

        reader = csv.DictReader(csvfile)
        for row in reader:
            # the Managed Object node is of the form
            # <managedObject class="MRBTS" version="FL16" distName="PLMN-PLMN/MRBTS-1111/LNBTS-1111" id="1111111">
            mo_line = '\t'*2 + '<managedObject class="' + row['class'] + '" version="' + row['version'] +'" distName="' + row['distName'] + '" id="' + row['id'] + '">\n'
            xmlfile.write(mo_line)

            # rest of the parameters
            for parameter_name in row:
                if not parameter_name in mo_attributes:
                    if row[parameter_name] == rest_val_str:
                        # This parameter is not available for this managedObject
                        continue
                    elif '{}' in parameter_name:
                        # a list
                        xmlfile.write('\t'*3 + '<list name="' + re.sub('{}','',parameter_name) + '">\n')
                        HelperFunctions.listCsv2Xml(row[parameter_name], xmlfile)
                        xmlfile.write('\t'*3 + '</list>\n')
                    else:
                        # formal <p..> .. </p>
                        xmlfile.write('\t'*3 + '<p name="' + parameter_name + '">' + row[parameter_name] + '</p>\n')

            xmlfile.write('\t'*2 + '</managedObject>\n')

        # standard XML information
        xmlfile.write('\t</cmData>\n')
        xmlfile.write('</raml>\n')
