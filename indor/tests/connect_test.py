__author__ = "Damian Mirecki"

import unittest
import requests
from connect import Connect


class TestConnect(unittest.TestCase):
    def test_basic_auth(self):
        connect = Connect()
        connect.arguments = "GET http://api.sample.pl, AUTH sampleUsername samplePassword"
        auth = connect.get_auth()

        self.assertIsInstance(auth, requests.auth.HTTPBasicAuth)

    def test_basic_auth2(self):
        connect = Connect()
        connect.arguments = "GET http://api.sample.pl, AUTH BASIC sampleUsername samplePassword"
        auth = connect.get_auth()

        self.assertIsInstance(auth, requests.auth.HTTPBasicAuth)

    def test_digest_auth(self):
        connect = Connect()
        connect.arguments = "GET http://api.sample.pl, AUTH DIGEST sampleUsername samplePassword"
        auth = connect.get_auth()

        self.assertIsInstance(auth, requests.auth.HTTPDigestAuth)

    def test_none_auth(self):
        connect = Connect()
        connect.arguments = "GET http://api.sample.pl"
        auth = connect.get_auth()

        self.assertEqual(auth, [])