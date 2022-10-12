import string


def remove_non_printable(s):
    s = ''.join([x for x in s if x in string.printable])
    return s