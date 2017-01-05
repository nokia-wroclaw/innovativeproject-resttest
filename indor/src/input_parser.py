from pyparsing import *
import json

from . import indor_exceptions

# TODO - Tomasz Wlisłocki - Uprościć tego regexa
# TODO - Sławomir Domagała - ja go tu tylko przeniosłem :P
# TODO - Damian Mirecki, Bartosz Zięba - kto jest autorem? :D
word = Regex('[a-zA-Z0-9.><=:/$&+;?@|^*()%!-_]*[a-zA-Z0-9><=:/$&+;?@|^*()%!-]')
expression_in_bracket = originalTextFor(nestedExpr("{", "}"))
quoted_string = QuotedString(quoteChar='"', multiline=True, escChar='\\', unquoteResults=True)
token = expression_in_bracket | quoted_string | word


def flatten_list(x):
    """
    :param x:
    :type x: list
    :return:
    :rtype: list
    """
    if len(x) == 1:
        return x[0]
    return x


def parse_constants(input_data):
    # Getting all defined macros
    const_definition = Suppress("DEFINE") + word + Suppress("=") + empty + restOfLine
    constants = list(const_definition.searchString(input_data))
    print(constants)

    # Replacing consts values in input text
    constants_replaced = input_data

    # Replacing with reverse order so that consts declared earlier were more important
    for key, value in constants[::-1]:
        const = Literal("@") + Literal(key) + Literal("@")
        const.setParseAction(replaceWith(value))
        constants_replaced = const.transformString(constants_replaced)

    # Removing consts definitions
    const_definition.setParseAction(replaceWith(""))
    return const_definition.transformString(constants_replaced)


def parse_repeat_statement(start, length, tokens):
    repetitions_json, commands = list(tokens)
    try:
        repetitions = json.loads(repetitions_json)
    except:
        raise indor_exceptions.InvalidRepeatParameters(repetitions_json)

    parsed_string = ""

    for repetition_name, repetition_params in repetitions.items():
        scenario = Literal("SCENARIO")
        scenario.setParseAction(replaceWith('REPEATED_SCENARIO "' + str(repetition_name) + '"'))

        repetition = scenario.transformString(commands)
        for param_name, param_value in repetition_params.items():
            param = Literal("$") + Literal(param_name) + Literal("$")
            param.setParseAction(replaceWith(param_value))
            repetition = param.transformString(repetition)

        parsed_string += repetition

    return parsed_string


def parse_repeats(input_data):
    # repeats_definition = nestedExpr("REPEAT FOR", "END REPEAT")
    repeats_definition = Suppress("REPEAT FOR") + expression_in_bracket + SkipTo("END REPEAT") + Suppress("END REPEAT")

    repeats_definition.setParseAction(parse_repeat_statement)

    return repeats_definition.transformString(input_data)


def parse(input_data):
    consts_replaced = parse_constants(input_data)

    hashmark = '#'
    multi_line_comment_start = '/%'
    multi_line_comment_end = '%/'

    inline_comment = hashmark + restOfLine
    multi_line_comment = nestedExpr(multi_line_comment_start, multi_line_comment_end)
    comment = multi_line_comment | inline_comment

    repeats_parsed = parse_repeats(consts_replaced)

    sub_command = Group(OneOrMore(token) + Optional(Literal(",").suppress()))
    command = Group(OneOrMore(sub_command) + ("." + LineEnd()).suppress())

    parser = OneOrMore(command)
    parser.ignore(comment)

    all_commands = parser.parseString(repeats_parsed).asList()
    return map(flatten_list, all_commands)  # TW: Ta linijka kodu to piękno najczystszej postaci <3