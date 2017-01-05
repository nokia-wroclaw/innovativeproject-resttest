ERROR_NUMBER_EXPECTED = "Oczekiwano liczby"
ERROR_WRONG_NUMBER_OF_ARGUMENTS = "Za mało argumentów"
ERROR_WRONG_CONTENT_TYPE = "Zły typ zawartości"
ERROR_RESPONSE_NOT_FOUND = "Brak odpowiedzi od testowanego serwera"
ERROR_CONNECTION_TIMEOUT = "Przekroczono zdefiniowany czas połączenia"
ERROR_INVALID_STATUS_CODE = "Niepoprawny kod statusu"
ERROR_TEST_CLASS_DOES_NOT_EXIST = "Klasa tesująca nie istnieje"
ERROR_WRONG_SYNTAX_IN = "Syntax error in "


class Result:
    def __init__(self, class_instance):
        self.pretty_name = class_instance.__class__.pretty_name


class Passed(Result):
    def __init__(self, class_instance):
        Result.__init__(self, class_instance)


class Failed(Result):
    def __init__(self, class_instance, expected, actual):
        Result.__init__(self, class_instance)
        self.expected = expected
        self.actual = actual


class Error(Result):
    def __init__(self, class_instance, short_message, extended_information=""):
        Result.__init__(self, class_instance)
        self.error = short_message
        self.extended_information = extended_information

    @classmethod
    def from_exception(cls, class_instance, exception):
        return cls(class_instance, str(exception))

    @classmethod
    def syntax_error(cls, class_instance, command, message):
        return cls(class_instance, ERROR_WRONG_SYNTAX_IN + ' '.join(command), message)


class ConnectionError(Result):
    def __init__(self, class_instance, short_message, extended_information=""):
        Result.__init__(self, class_instance)
        self.error = short_message
        self.extended_information = extended_information
