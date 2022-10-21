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
from xmlentry import XmlEntryType

import random

class Item(XmlEntry):
    def __init__(self):
        # "item" nodes do not have a name but
        # we assign a name of the form "item#...."
        # to distinguish individual items from one
        # another. It's just an internal value that is
        # not used anywhere else
        # current implementation uses a random int with
        # a slight but non-zero chance of collision
        n = '{item#' + str(random.randint(0, 1000000000)) + '}'
        super().__init__(n, XmlEntryType.ITEM)

    def __str__(self):
        s = ''
        for key,val in self.propertyValues.items():
            if '{}' not in key:
                # normal entry
                # if the name/key has "#rand_name#" in it,
                # ignore it
                if "#rand_name#" in key:
                    key = ""

                sep = ':' if len(key) > 0 else ''
                s = s + key + sep + val + ';'
            else:
                # nested list or item
                s = s + key + str(val)
        return '{' + s[:-1] + '}'