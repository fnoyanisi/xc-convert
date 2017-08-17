# This file is used to test the library code
from XcFunctions import *

if __name__ == '__main__':

    doc = minidom.parse("test/LNCEL_short.xml")

    if examineXmlFormat(doc):
        l = createManagedObjectDict(doc)

        if not len(l) == 0:
            convertXmlToCsv(doc,'test/',l)
            print("Done - xml to csv")

    if examineCsvFormat("test/MRBTS.csv"):
        print("Done - csv to xml")
        convertCsv2Xml("test/MRBTS.csv","test/MRBTS_custom.xml")
    else:
        print("not done - csv to xml")
