# base class for more complex entries in the XML file
# this can be subclassed by a managed object, a list or an item
from enum import Enum


# enumeration type to distinguish different types of XmlEntries
class XmlEntryType(Enum):
    PARAMETER = 1
    ITEM = 2
    LIST = 3
    MANAGEDOBJECT = 4

# n -   name of the XML entry. For parameters, this is the internal name of the
#       parameter. For lists, this is the internal name of the list appended with
#       '{}' characters at the end to indicate this is a list item.
#       No names, or empty string, is used for item entries.
# t -   this parameter should be of type Types
class XmlEntry:
    def __init__(self, n, t):
        self.name = n
        self.type = t
        self.propertyNames = []
        self.propertyValues = {}

    def add_properties(self, p):
        if isinstance(p, list):
            self.propertyValues = p
            for key in p:
                self.propertyNames.append(key)
        else:
            raise RuntimeError("expecting a list type")

    def add_property(self, pname, pval):
        self.propertyNames.append(pname)
        self.propertyValues[pname] = pval

    def has_property(self, pname):
        if pname in self.propertyNames:
            return True
        else:
            return False

    def get_property(self, pname):
        if pname in self.propertyNames:
            return self.propertyValues[pname]
        else:
            return None