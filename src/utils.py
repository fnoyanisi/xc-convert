"""
Some utility methods

Copyright (c) 2017-2022 Fehmi Noyan ISI. All rights reserved.
See the LICENSE file for the end user license agreement.
"""

import string


# removes non-printable chars from the str
def remove_non_printable(s):
    s = ''.join([x for x in s if x in string.printable])
    return s


# trims the string "s" if its length > w and
# replaces the last three characters with "..."
def trim_str(s, w):
    if len(s) > w:
        return s[:w - 3] + "..."
    else:
        return s
