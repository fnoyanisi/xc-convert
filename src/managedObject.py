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
import XmlEntry


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