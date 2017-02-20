from .indor_exceptions import ClassPropertyNotFound
from .xml_tree_factory import XmlTreeFactory
from .xml_tree import XmlTree


class XmlTreeRegister(type(XmlTree)):
    def __init__(cls, name, bases, dic):
        cls.property_name_for_printer = 'pretty_name'
        if cls.property_name_for_printer not in dic:
            raise ClassPropertyNotFound(name, cls.property_name_for_printer)
        super(XmlTreeRegister, cls).__init__(name, bases, dic)
        XmlTreeFactory().add_class(name, cls)
