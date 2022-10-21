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
from src.xmlds.xmlentry import XmlEntry
from src.xmlds.xmlentry import XmlEntryType

class List(XmlEntry):
    def __init__(self, n):
        # name of a "list" is appended with a "{}"
        # to distinguish it from normal parameter-value pairs
        super().__init__(n + '{}', XmlEntryType.LIST)

    def __str__(self):
        s = ''
        has_item = False
        # key - name of the XmlEntry
        # val - XmlEntry itself
        for key,val in self.propertyValues.items():

            # this if-else statement should cover all
            # the possible cases, hence a separate "else"
            # fallback block is not needed
            if not hasattr(val, 'type'):
                # normal entry
                # if the name/key has "#rand_name#" in it,
                # ignore it
                if "#rand_name#" in key:
                    key = ""

                sep = ':' if len(key) > 0 else ''
                s = s + key + sep + val + ';'
            elif val.type == XmlEntryType.ITEM:
                s = s + str(val) + ';'
                has_item = True
            elif val.type == XmlEntryType.LIST:
                # nested list
                s = s + key + str(val)

        # do not add curly braces if the only thing in
        # the List is an item, which has its own curly
        # braces around it
        if has_item and len(self.propertyValues) == 1:
            return s[:-1]
        else:
            return '{' + s[:-1] + '}'