GENERAL_ERROR_PARSE_FAILED = "The given file has invalid format: "
GENERAL_ERROR_FILE_NOT_FOUND = 'File not found: '
GENERAL_ERROR_UNKNOWN_ERROR = 'Unexpected error occured'


class GeneralError:
    def __init__(self, msg):
        self.message = msg