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

class list:
    name = ""
    properties = {}

class managedObject:
    moClass = ""
    version = ""
    distName = ""
    id = ""
    propertyValues = {}
    propertyNames = []

    # constructor
    def __init__(self, m, v, d, i):
        self.moClass = m
        self.version = v
        self.distName = d
        self.id = i

    # adds a new property to this managed object
    def addProperty(self, pname, pval):
        self.propertyNames.append(pname)
        self.propertyValues[pname] = pval

    # checks whether this managed object has a property with
    # name = pname
    def hasProperty(self, pname):
        if pname in self.propertyName:
            return True
        else:
            return False

    # returns the value of a property
    def getProperty(self, pname):
        if pname in self.propertyName:
            return self.propertyValues[pname]
        else:
            return None