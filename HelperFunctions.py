from xml.dom import minidom
import re

def listXml2Csv(node_p):
    """
    This function converts an XML list, whose structure is given below,
    to {param1=123;param2=456}{param1=789;param2=000} format

     list name='....'
       |
       +--item1
       |   |
       |   +--p1 name='...'
       |   |
       |   +--p2 name='...'
       |
       +--item2
       |   |
       |   +--p1 name='...'
       |   |
       |   +--p2 name='...'

    :param node_p: valid XML node
    :return: a tuple whose first item is 'parameter_name' and second item is corresponding 'parameter_value'
    """
    parameter_name = node_p.getAttribute("name") + '{}'

    # string are immutable, so use a list, and then join()
    tmp = []
    parameter_value = ""
    for item in node_p.childNodes:
        if item.nodeName == 'item':
            tmp.append('{')

            for item_p in item.childNodes:
                if item_p.nodeName == 'p':
                    item_parameter_name = item_p.getAttribute("name")
                    item_parameter_value = item_p.firstChild.data
                    v = item_parameter_name + '=' + item_parameter_value + ';'
                    tmp.append(v)

            tmp.append('}')
            parameter_value = ''.join(tmp)

    if len(parameter_value) == 0:
        return (parameter_name,'')
    else:
    # finally, replace any ';}' with '}' and return
        return (parameter_name, re.sub(';}', '}', parameter_value))

def listCsv2Xml(raw_str, fd):
    """
    This functions converts a string which is of {param1=123;param2=456}{param1=789;param2=000}
    format into given XML tree

     list name='....'
       |
       +--item1
       |   |
       |   +--p1 name='...'
       |   |
       |   +--p2 name='...'
       |
       +--item2
       |   |
       |   +--p1 name='...'
       |   |
       |   +--p2 name='...'

    :param raw_str: string value
    :param fd: an open File Object with write permission
    :return: number of lines written into the file
    """
    w = 0

    # just in case there is nay whitespace characters in the input string
    trimmed = re.sub(' ','',raw_str)
    for list_item in trimmed.split('}{'):
        # remove and curly brackets
        # tmp has param1=123;param2=456;param3=789 format
        tmp = re.sub('[{}]','',list_item)

        fd.write('\t'*4 + '<list>\n')
        w += 1
        for i in tmp.split(';'):
            p,v = i.split('=')
            fd.write('\t'*5 + '<p name="' + p + '">' + v + '</p>\n')
            w += 1
        fd.write('\t'*4 + '</list>\n')
        w += 1

    return w