# base class for more complex entries in the XML file
# this can be subclassed by a managed object or a list
class XmlEntry:
    name = ""
    propertyNames = []
    propertyValues = {}

    def __init__(self, n):
        self.name = n

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