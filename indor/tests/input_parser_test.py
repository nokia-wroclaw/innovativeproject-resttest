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
                    username indor,
                HEADERS
                    sth sth.

                ASSERT RESPONSE STATUS OK."""

        parsed = parser.parse(to_be_parsed)

        expected = [
            [
                [
                    "GET",
                    "http://api.geonames.org/postalCodeLookupJSON"
                ],
                [
                    "PARAMS",
                    "postalcode",
                    "50316",
                    "username",
                    "indor"
                ],
                [
                    "HEADERS",
                    "sth",
                    "sth"
                ]
            ],
            [
                "ASSERT",
                "RESPONSE",
                "STATUS",
                "OK"
            ]
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
                [
                    "some",
                    "text",
                    "GET",
                    "http://api.org/"
                ],
                [
                    "PARAMS",
                    "username",
                    "indor"
                ]
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
                """

        parsed = parser.parse(to_be_parsed)

        expected = [
            [
                [
                    "GET",
                    "http://api.geonames.org/postalCodeLookupJSON"
                ],
                [
                    "PARAMS",
                    "postalcode",
                    "50316",
                    "username",
                    "indor indorowski,."
                ]
            ],
            [
                "ASSERT",
                "RESPONSE",
                "STATUS",
                "OK"
            ]
        ]

        self.assertItemsEqual(parsed, expected)

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
                [
                    "GET",
                    "http://api.geonames.org/postalCodeLookupJSON"
                ],
                [
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
        ]

        self.assertItemsEqual(actual, expected)

    def test_expression_in_braces_as_one(self):
        to_be_parsed = """
                GET
                    http://api.org/,
                JSON
                    {
                        "key": "value",
                        "key1": [
                            {"key": "no /%comment %/"},
                            {"key": "#no comment"}
                        ]
                    }
                    .
                """

        actual = parser.parse(to_be_parsed)

        expected = [
            [
                [
                    "GET",
                    "http://api.org/"
                ],
                [
                    "JSON",
                    """{
                        "key": "value",
                        "key1": [
                            {"key": "no /%comment %/"},
                            {"key": "#no comment"}
                        ]
                    }"""
                ]
            ]
        ]

        self.assertItemsEqual(actual, expected)

    def test_expression_in_quoted_braces(self):
        to_be_parsed = """
                GET
                    http://api.org/,
                PARAMS
                    username "pas{word}".
                """

        actual = parser.parse(to_be_parsed)

        expected = [
            [
                [
                    "GET",
                    "http://api.org/"
                ],
                [
                    "PARAMS",
                    "username",
                    "pas{word}"
                ]
            ]
        ]

        self.assertItemsEqual(actual, expected)


    def test_defines(self):
        to_be_parsed = """
                DEFINE URL = http://api.geonames.org/postalCodeLookupJSON
                DEFINE POST = http://api.geonames.org/postalCodeLookupXML
                DEFINE SOME_TEXT = username indor
                GET
                    @URL@,
                PARAMS
                    postalcode 41800,
                    @SOME_TEXT@.
                POST @POST@."""

        actual = parser.parse(to_be_parsed)
        expected = [
            [
                [
                    "GET",
                    "http://api.geonames.org/postalCodeLookupJSON"
                ],
                [
                    "PARAMS",
                    "postalcode",
                    "41800",
                ],
                [
                    "username",
                    "indor"
                ]
            ],
            [
                "POST",
                "http://api.geonames.org/postalCodeLookupXML"
            ]
        ]

        self.assertItemsEqual(actual, expected)


    def test_incompatible_with_grammar(self):
        to_be_parsed = """
                BAD EXAMPLE <>
            """

        # actual = parser.parse(to_be_parsed)
        #TODO implementation