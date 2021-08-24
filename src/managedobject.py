"""
represents a managedObject entry in an XML file of the form
     <managedObject class="..." version="....." distName="...." id="....">
       <p name="xxx">...</p>
       <p name="yyy">...</p>
       <p name="zzz">...</p>
       <list name="aaaa">
           <item>
               <p name="xxx">...</p>
               ....
           </item>
       </list>
       ....
     </managedObject>
"""
from xmlentry import XmlEntry


class List(XmlEntry):
    def __init__(self, n):
        super().__init__(n + '{}')


class ManagedObject(XmlEntry):
    # uses XmlEntry.name as the moClass value
    moClass = ""
    version = ""
    distName = ""
    id = ""

    # constructor
    def __init__(self, n, v, d, i):
        super().__init__(n)
        self.version = v
        self.distName = d
        self.id = i
        self.moClass = self.name
