
__author__ = 'Bartek'

from xml_tree import XmlTree
import xml.etree.ElementTree as ET
from xml_tree_register import XmlTreeRegister
import xml2json

class TextXml(XmlTree):
    __metaclass__ = XmlTreeRegister

    pretty_name = "TEXT XML"

    def parse(self, xml):
        return ET.fromstring(xml)


class TextJson(XmlTree):
    __metaclass__ = XmlTreeRegister

    pretty_name = "TEXT JSON"

    def parse(self, xml):
        return xml2json.json2elem(xml, ET.Element)

    # method form stackoverflow
    # stackoverflow.com/questions/8988775/convert-json-to-xml-in-python
