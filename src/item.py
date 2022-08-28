"""
represents an item entry in an XML DOM of the form
       <list name="aaaa">
           <item>
               <p name="xxx">...</p>
               ....
           </item>
           <item>
            ...
            ...
            </item>
       </list>
"""
from xmlentry import XmlEntry

class Item(XmlEntry):
    def __init__(self):
        # "item" nodes do not have a name
        # hence not passing an explicit name string
        super().__init__('{}')

    def __str__(self):
        s = ''
        for key,val in self.propertyValues.items():
            if '{}' not in key:
                # normal entry
                sep = ':' if len(key) > 0 else ''
                s = s + key + sep + val + ';'
            else:
                # nested list or item
                s = s + key + str(val)
        return '{' + s[:-1] + '}'