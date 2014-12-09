# coding=utf-8
__author__ = "Tomasz M. Wlisłocki"

import unittest
import input_parser as parser


class TestInputParser(unittest.TestCase):
    def test_basic_parse_1(self):
        to_be_parsed = """
                # Our first working test
                GET
                    http://api.geonames.org/postalCodeLookupJSON,
                PARAMS
                    postalcode 50316
                    username indor.

                ASSERT RESPONSE STATUS OK.
                ASSERT RESPONSE TYPE JSON.
                ASSERT RESPONSE EMPTY.
                ASSERT RESPONSE LENGTH > 200.
                """

        parsed = parser.parse(to_be_parsed)

        expected = [
            """GET http://api.geonames.org/postalCodeLookupJSON PARAMS postalcode 50316 username indor""".split(" "),
            """ASSERT RESPONSE STATUS OK""".split(" "),
            """ASSERT RESPONSE TYPE JSON""".split(" "),
            """ASSERT RESPONSE EMPTY""".split(" "),
            """ASSERT RESPONSE LENGTH > 200""".split(" ")
        ]

        self.assertItemsEqual(parsed, expected)

    def test_comments(self):
        to_be_parsed = """
                some text
                # Our first working test
                GET
                    http://api.org/,
                PARAMS
                    username indor.
                ASSERT RESPONSE TYPE JSON.
                /% asdfasfhasdkfas
                asddASDasd
                asdAKDHavsd
                ASDasdASD
                EWERQWERasadf
                asdfasd%/
                ASSERT RESPONSE /% Inline comment %/ EMPTY.
                ASSERT RESPONSE LENGTH > 200."""

        actual = parser.parse(to_be_parsed)

        expected = [
            [
                "some",
                "text",
                "GET",
                "http://api.org/",
                "PARAMS",
                "username",
                "indor"
            ],
            [
                "ASSERT",
                "RESPONSE",
                "TYPE",
                "JSON"
            ],
            [
                "ASSERT",
                "RESPONSE",
                "EMPTY"
            ],
            [
                "ASSERT",
                "RESPONSE",
                "LENGTH",
                ">",
                "200"
            ]
        ]

        self.assertItemsEqual(actual, expected)

    def test_escaped_strings(self):
        to_be_parsed = """
                # Our first working test
                GET
                    http://api.geonames.org/postalCodeLookupJSON,
                PARAMS
                    postalcode 50316
                    username "indor indorowski,.".

                ASSERT RESPONSE STATUS OK.
                ASSERT RESPONSE TYPE JSON.
                /% asdfasfhasdkfas
                asddASDasd
                asdAKDHavsd
                ASDasdASD
                EWERQWERasadf
                asdfasd%/
                ASSERT RESPONSE /% Inline comment %/ EMPTY.
                ASSERT RESPONSE LENGTH > 200.
                """

        parsed = parser.parse(to_be_parsed)

        expected = ["GET", """http://api.geonames.org/postalCodeLookupJSON""", "PARAMS", "postalcode", "50316",
                    "username", "indor indorowski,."]

        self.assertItemsEqual(parsed[0], expected)

    def test_quoted_expression_as_one(self):
        to_be_parsed = """
                GET
                    http://api.geonames.org/postalCodeLookupJSON,
                PARAMS
                    postalcode "really
                    long.
                    and. #no comment
                    snarky\"

                    /% no comment %/


                    example."
                    username indor."""

        actual = parser.parse(to_be_parsed)

        expected = [
            [
                "GET",
                "http://api.geonames.org/postalCodeLookupJSON",
                "PARAMS",
                "postalcode",
                """really
                    long.
                    and. #no comment
                    snarky\"

                    /% no comment %/


                    example.""",
                "username",
                "indor"
            ]
        ]

        self.assertItemsEqual(actual, expected)