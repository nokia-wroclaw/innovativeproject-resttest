__author__ = "Damian Mirecki"

import unittest

import requests

from connect import extract_section_by_name, get_allow_redirects, get_auth
import input_parser


class TestConnect(unittest.TestCase):
    def test_basic_auth(self):
        parsed_input = input_parser.parse("GET http://api.sample.pl, AUTH sampleUsername samplePassword.")[0]
        auth = get_auth(parsed_input)

        self.assertIsInstance(auth, requests.auth.HTTPBasicAuth)

    def test_basic_auth2(self):
        parsed_input = input_parser.parse("GET http://api.sample.pl, AUTH BASIC sampleUsername samplePassword.")[0]
        auth = get_auth(parsed_input)

        self.assertIsInstance(auth, requests.auth.HTTPBasicAuth)

    def test_digest_auth(self):
        parsed_input = input_parser.parse("GET http://api.sample.pl, AUTH DIGEST sampleUsername samplePassword.")[0]
        auth = get_auth(parsed_input)

        self.assertIsInstance(auth, requests.auth.HTTPDigestAuth)

    def test_none_auth(self):
        parsed_input = input_parser.parse("GET http://api.sample.pl.")[0]
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