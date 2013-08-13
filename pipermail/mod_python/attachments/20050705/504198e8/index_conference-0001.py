import os
from elementtree import ElementTree
import cElementTree


def index(req):
    _conference_name = 'Welcome at our conference'

    file_name = "/home/mmokrejs/public_html/conference/somexmlfile.xml"
    if os.path.isfile(file_name):
        try:
            _xml_def = ElementTree.parse(file_name) # ._root
        except IOError, e:
            raise IOError, "cElementTree.parse(" + str(file_name) + ")._root failed with: " + str(e)
    else:
        raise RuntimeError, "No such file %s.<br>\n" % file_name
    s = ""
    s += "<HTML>\n"
    s += "<HEAD>\n"
    s += "  <TITLE>Testcase for 'file() constructor not accessible in restricted mode' error</TITLE>\n"
    s += "  <LINK rel=\"stylesheet\" type=\"text/css\" href=\"styles/style.css\">\n"
    s += "</HEAD>\n"
    s += "<BODY>Testcase works fine and has parsed contents of %s file.\n" % file_name
    s += "</BODY>\n"
    s += "</HTML>\n"
    
    return s
