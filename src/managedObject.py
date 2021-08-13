# represents a managedObject entry in an XML file of the form
#     <managedObject class="..." version="....." distName="...." id="....">
#       <p name="xxx">...</p>
#       <p name="yyy">...</p>
#       <p name="zzz">...</p>
#       <list name="aaaa">
#           <item>
#               <p name="xxx">...</p>
#               ....
#           </item>
#       </list>
#       ....
#     </managedObject>
#

# base class for compex entries in the XML file
# this could be a managed object or a list
class XmlEntry:
    name = ""
    propertyNames = []
    propertyValues = {}

    def __init__(self, n):
        self.name = n

    def add_properties(self, p):
        self.propertyValues = p
        for key in p:
            self.propertyNames.append(key)

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


class List(XmlEntry):
    pass


class ManagedObject(XmlEntry):
    moClass = ""
    version = ""
    distName = ""
    id = ""

    # constructor
    def __init__(self, m, v, d, i, n):
        super().__init__(n)
        self.version = v
        self.distName = d
        self.id = i