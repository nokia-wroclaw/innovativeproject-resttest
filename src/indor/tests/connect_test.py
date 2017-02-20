import unittest

import requests

import indor.input_parser as input_parser
from indor.command_classes.connect import get_allow_redirects, get_auth
from indor.tools import extract_section_by_name

API_SAMPLE_URL = "http://api.sample.pl"
METHOD = "GET"


class TestConnect(unittest.TestCase):
    def test_basic_auth(self):
        parsed_input = next(input_parser.parse("%s %s, AUTH sampleUsername samplePassword." % (METHOD, API_SAMPLE_URL)))
        auth = get_auth(parsed_input)

        self.assertIsInstance(auth, requests.auth.HTTPBasicAuth)

    def test_basic_auth2(self):
        parsed_input = next(input_parser.parse("GET http://api.sample.pl, AUTH BASIC sampleUsername samplePassword."))
        auth = get_auth(parsed_input)

        self.assertIsInstance(auth, requests.auth.HTTPBasicAuth)

    def test_digest_auth(self):
        parsed_input = next(input_parser.parse("GET http://api.sample.pl, AUTH DIGEST sampleUsername samplePassword."))
        auth = get_auth(parsed_input)

        self.assertIsInstance(auth, requests.auth.HTTPDigestAuth)

    def test_none_auth(self):
        parsed_input = next(input_parser.parse("GET http://api.sample.pl."))
        auth = get_auth(parsed_input)

        self.assertEqual(auth, None)

    def test_if_exists_keyword_allow_redirects_then_allow_redirects(self):
        connect_data = [
            [
                "GET",
                "http://api.sample.pl"
            ],
            [
                "ALLOW",
                "REDIRECTS"
            ]
        ]

        self.assertTrue(get_allow_redirects(connect_data))

    def test_if_not_exists_keyword_allow_redirects_then_does_not_allow_redirects(self):
        connect_data = [
            "GET",
            "http://api.sample.pl"
        ]

        self.assertFalse(get_allow_redirects(connect_data))

    def test_extract_section_by_name(self):
        self.assertEqual(None, extract_section_by_name([["PARAMS", "sth", "sth", "sth", "sth"], ["ALLOW", "REDIRECTS"]],
                                                       "BADNAME"))

        self.assertEqual([], extract_section_by_name([["PARAMS", "sth", "sth", "sth", "sth"], ["ALLOW", "REDIRECTS"]],
                                                     "ALLOW REDIRECTS"))

        self.assertEqual(["sth", "sth", "sth", "sth"], extract_section_by_name([["PARAMS", "sth", "sth", "sth", "sth"],
                                                                                ["ALLOW", "REDIRECTS"]], "PARAMS"))
