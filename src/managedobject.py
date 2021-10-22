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

    def __str__(self):
        s = ''
        for key,val in self.propertyValues.items():
            if '{}' not in key:
                # normal entry
                sep = ':' if len(key) > 0 else ''
                s = s + key + sep + val + ';'
            else:
                # nested list
                s = s + key + str(val)
        return '{' + s[:-1] + '}'

class ManagedObject(XmlEntry):
    # uses XmlEntry.name as the moClass value
    # moClass = ""
    # version = ""
    # distName = ""
    # id = ""

    # constructor
    def __init__(self, n, v, d, i):
        super().__init__(n)
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