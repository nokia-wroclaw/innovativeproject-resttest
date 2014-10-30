from pyparsing import *
from assertions import *

__author__ = 'Damian Mirecki'

def makeReqest(tokens):
    AbstractAction.request = requests.get(tokens[0])
    AbstractAction.result = AbstractAction.request.json()

def assertResponseIs(tokens):
    a = globals()["AssertResponseIs" + tokens[0].title()]()
    a.check()

def assertSuccess():
    a = AssertSuccess()
    a.check()

def assertContains(tokens):
    for token in tokens:
        a = AssertContainsKey(token[0])
        a.check()

        a = AssertContainsValueWithType(token[0], token[1])
        a.check()


def parse(fileName):
    ParserElement.setDefaultWhitespaceChars(" \t")

    newline                     = Suppress("\n")
    isLiteral                   = Suppress("is")

    response                    = Literal("response")
    success                     = Literal("success")
    assertionHead               = Literal("Assert")

    httpAddress                 = Word(alphanums + ":/.?&=")


    open_action                 = (Suppress("Open") + httpAddress)\
        .setParseAction(makeReqest)

    assertionResponseIs         = (Suppress(assertionHead + response + isLiteral) + oneOf("JSON XML", caseless=True))\
        .setParseAction(assertResponseIs)

    assertionSuccess            = Suppress(assertionHead + success)\
        .setParseAction(assertSuccess)

    assertionContains           = (Suppress(assertionHead + response + "contains" + "'{" + newline)
                                   + OneOrMore(Group(Word(alphanums) + Suppress(":") + Suppress("<") + Word(alphanums) + Suppress(">")) + Suppress(Optional(',')) + newline)
                                   + Suppress("}'"))\
        .setParseAction(assertContains)


    action                      = OneOrMore((open_action | assertionSuccess | assertionResponseIs | assertionContains) + newline)

    return action.parseFile(fileName)
