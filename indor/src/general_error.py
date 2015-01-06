__author__ = 'Damian Mirecki'

GENERAL_ERROR_PARSE_FAILED = "Format wczytanego pliku jest niepoprawny: "

class GeneralError:
    def __init__(self, msg):
        self.message = msg;