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

Copyright (c) 2017-2022 Fehmi Noyan ISI. All rights reserved.
See the LICENSE file for the end user license agreement.
"""
from src.xmlds.xmlentry import XmlEntry
from src.xmlds.xmlentry import XmlEntryType


class ManagedObject(XmlEntry):
    # constructor
    def __init__(self, n, v, d, i):
        super().__init__(n, XmlEntryType.MANAGEDOBJECT)
        self.version = v
        self.distName = d
        self.id = i
        self.moClass = self.name

    def get_values(self):
        # add moClass, version, distName and id
        # and return to the caller
        # concatenate two dictionaries
        d = {'class': self.moClass, 'version': self.version, 'distName': self.distName, 'id': self.id}
        d.update(self.propertyValues)
        return d