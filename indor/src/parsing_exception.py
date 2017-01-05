class ParsingException(Exception):
    def __init__(self, parsing_object, message):
        self.parsing_object = parsing_object
        self.message = message
