__author__ = 'Damian Mirecki'

GENERAL_ERROR_PARSE_FAILED = "Format wczytanego pliku jest niepoprawny: "
GENERAL_ERROR_FILE_NOT_FOUND = 'File not found: '
GENERAL_ERROR_UNKNOWN_ERROR = 'Unknown error occured.'


class GeneralError:
    def __init__(self, msg):
        self.message = msg;