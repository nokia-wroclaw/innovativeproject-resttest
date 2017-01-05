__author__ = 'Bartek'

from .xml_tree import XmlTree
import xml.etree.ElementTree as ET
from .xml_tree_register import XmlTreeRegister
import json
from bs4 import BeautifulSoup


class TextXml(XmlTree, metaclass=XmlTreeRegister):
    pretty_name = "TEXT XML"

    def parse(self, xml):
        return ET.fromstring(xml)


class TextHtml(XmlTree, metaclass=XmlTreeRegister):
    pretty_name = "TEXT HTML"

    def parse(self, xml):
        return ET.fromstring(BeautifulSoup.prettify(xml))


class ApplicationJson(XmlTree, metaclass=XmlTreeRegister):
    pretty_name = "APPLICATION JSON"

    def parse(self, xml):
        json_obj = json.loads(xml)
        xml_string = self.json2xml(json_obj)
        return ET.fromstring(xml_string.encode('utf-8'))
    # method form stackoverflow
    # stackoverflow.com/questions/8988775/convert-json-to-xml-in-python
    def json2xml(self, json_obj, line_padding=""):
        result_list = list()

        json_obj_type = type(json_obj)

        if json_obj_type is list:
            for sub_elem in json_obj:
                result_list.append(self.json2xml(sub_elem, line_padding))

            return "\n".join(result_list)

        if json_obj_type is dict:
            for tag_name in json_obj:
                sub_obj = json_obj[tag_name]
                result_list.append("%s<%s>" % (line_padding, tag_name))
                result_list.append(self.json2xml(sub_obj, "\t" + line_padding))
                result_list.append("%s</%s>" % (line_padding, tag_name))

            return "\n".join(result_list)

        return "%s%s" % (line_padding, json_obj)