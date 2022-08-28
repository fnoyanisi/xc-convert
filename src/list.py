"""
represents a list entry in an XML DOM of the form
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
from xmlentry import XmlEntryType

class List(XmlEntry):
    def __init__(self, n):
        # name of a "list" is appended with a "{}"
        # to distinguish it from normal parameter-value pairs
        super().__init__(n + '{}', XmlEntryType.LIST)

    def __str__(self):
        s = ''
        has_item = False
        for key,val in self.propertyValues.items():
            if key =='' :
                s = str(val)
                has_item = True
            elif '{}' not in key:
                # normal entry
                sep = ':' if len(key) > 0 else ''
                s = s + key + sep + val + ';'
            else:
                # nested list
                s = s + key + str(val)

        # do not add curly braces if the only thing in
        # the List is an item, which has its own curly
        # braces around it
        if has_item and len(self.propertyValues) == 1:
            return s
        else:
            return '{' + s[:-1] + '}'