# This file is used to test the library code
from xml.dom import minidom
from XcFunctions import *
import os

if __name__ == '__main__':

    doc = minidom.parse("/home/fnoyanisi/code/python/read-xml/LNCEL_short.xml")

    if examineXmlFormat(doc):
        l = createManagedObjectDict(doc)

        if not len(l) == 0:
            convertXmlToCsv(doc,os.getcwd() + '/',l)
            print("Done - xml to csv")

    if examineCsvFormat("/home/fnoyanisi/code/python/read-xml/MRBTS.csv"):
        print("Done - csv to xml")
        convertCsv2Xml("/home/fnoyanisi/code/python/read-xml/MRBTS.csv","/home/fnoyanisi/code/python/read-xml/MRBTS_custom.xml")
    else:
        print("not done - csv to xml")
