import unittest

import indor.input_parser as parser


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

        self.assertCountEqual(parsed, expected)

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

        self.assertCountEqual(actual, expected)

    def test_escaped_strings(self):
        to_be_parsed = """
                # Our first working test
                GET
                    http://api.geonames.org/postalCodeLookupJSON,
                PARAMS
                    postalcode "50316"
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

        self.assertCountEqual(parsed, expected)

    def test_quoted_expression_as_one(self):
        to_be_parsed = """
                GET
                    http://api.geonames.org/postalCodeLookupJSON,
                PARAMS
                    postalcode "really
                    long.
                    and. #no comment
                    \\\"snarky

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
                    "snarky

                    /% no comment %/


                    example.""",
                    "username",
                    "indor"
                ]
            ]
        ]

        self.assertCountEqual(actual, expected)

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

        self.assertCountEqual(actual, expected)

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

        self.assertCountEqual(actual, expected)

    def test_repeats(self):
        to_be_parsed = """
                DEFINE BASE = http://httpbin.org

                GET @BASE@.
                ASSERT RESPONSE STATUS OK.

                REPEAT FOR
                {
                    "run1a": {"url": "http://www.wp.pl", "expected_code": 200},
                    "run1b": {"url": "http://ww.wp.pl", "expected_code": 404}
                }
                    GET $url$.
                    ASSERT RESPONSE STATUS $expected_code$.
                END REPEAT


                POST @BASE@.
                ASSERT RESPONSE STATUS OK.

                REPEAT FOR
                {
                    "run2a": {"url": "http://www.onet.pl", "expected_code": 200},
                    "run2b": {"url": "http://ww.onet.pl", "expected_code": 404}
                }
                    GET $url$.
                    ASSERT RESPONSE STATUS $expected_code$.
                END REPEAT
                """
        actual = parser.parse(to_be_parsed)

        expected = [
            [
                "GET",
                "http://httpbin.org"
            ],
            [
                "ASSERT",
                "RESPONSE",
                "STATUS",
                "OK"
            ],
            [
                "GET",
                "http://www.wp.pl"
            ],
            [
                "ASSERT",
                "RESPONSE",
                "STATUS",
                "200"
            ],
            [
                "GET",
                "http://ww.wp.pl"
            ],
            [
                "ASSERT",
                "RESPONSE",
                "STATUS",
                "404"
            ],
            [
                "POST",
                "http://httpbin.org"
            ],
            [
                "ASSERT",
                "RESPONSE",
                "STATUS",
                "OK"
            ],
            [
                "GET",
                "http://www.onet.pl"
            ],
            [
                "ASSERT",
                "RESPONSE",
                "STATUS",
                "200"
            ],
            [
                "GET",
                "http://ww.onet.pl"
            ],
            [
                "ASSERT",
                "RESPONSE",
                "STATUS",
                "404"
            ]
        ]

        self.assertCountEqual(actual, expected)

    def test_repeated_scenarios(self):
        to_be_parsed = """
                REPEAT FOR
                {
                    "run1": {"url": "http://www.onet.pl", "expected_code": 200},
                    "run2": {"url": "http://ww.onet.pl", "expected_code": 404}
                }
                    SCENARIO "Test 1 with repeats" FLAGS heavy important.
                        GET $url$.
                        ASSERT RESPONSE STATUS $expected_code$.
                END REPEAT
                """
        actual = parser.parse(to_be_parsed)

        expected = [
            [
                "REPEATED_SCENARIO",
                "run1",
                "Test 1 with repeats",
                "FLAGS",
                "heavy",
                "important"
            ],
            [
                "GET",
                "http://www.onet.pl"
            ],
            [
                "ASSERT",
                "RESPONSE",
                "STATUS",
                "200"
            ],
            [
                "REPEATED_SCENARIO",
                "run2",
                "Test 1 with repeats",
                "FLAGS",
                "heavy",
                "important"
            ],
            [
                "GET",
                "http://ww.onet.pl"
            ],
            [
                "ASSERT",
                "RESPONSE",
                "STATUS",
                "404"
            ]
        ]

        self.assertCountEqual(actual, expected)

    def test_defines(self):
        to_be_parsed = """
                DEFINE URL = http://api.geonames.org/postalCodeLookupJSON
                DEFINE POST = http://api.geonames.org/postalCodeLookupXML
                DEFINE SOME_TEXT = username indor

                DEFINE BASE = http://httpbin.org

                GET
                    @URL@,
                PARAMS
                    postalcode 41800,
                    @SOME_TEXT@.

                POST @POST@.

                DELETE @BASE@/delete.
                """

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
            ],
            [
                "DELETE",
                "http://httpbin.org/delete"
            ]
        ]

        self.assertCountEqual(actual, expected)

    def test_nested_defines(self):
        to_be_parsed = """
                DEFINE BASE = http://httpbin.org
                DEFINE URL2 = @BASE@/post

                GET @BASE@.
                POST @URL2@.
                """

        actual = parser.parse(to_be_parsed)
        expected = [
            [
                "GET",
                "http://httpbin.org"
            ],
            [
                "POST",
                "http://httpbin.org/post"
            ]
        ]

        self.assertCountEqual(actual, expected)
