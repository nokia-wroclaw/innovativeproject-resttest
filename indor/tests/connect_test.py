import mock

__author__ = "Damian Mirecki"

import unittest
import requests
from connect import Connect


class TestConnect(unittest.TestCase):
    @mock.patch('src.result_collector.ResultCollector')
    def test_basic_auth(self, result_collector_mock):
        connect = Connect(result_collector_mock)
        connect.arguments = "GET http://api.sample.pl, AUTH sampleUsername samplePassword"
        auth = connect.get_auth()

        self.assertIsInstance(auth, requests.auth.HTTPBasicAuth)

    @mock.patch('src.result_collector.ResultCollector')
    def test_basic_auth2(self, result_collector_mock):
        connect = Connect(result_collector_mock)
        connect.arguments = "GET http://api.sample.pl, AUTH BASIC sampleUsername samplePassword"
        auth = connect.get_auth()

        self.assertIsInstance(auth, requests.auth.HTTPBasicAuth)

    @mock.patch('src.result_collector.ResultCollector')
    def test_digest_auth(self, result_collector_mock):
        connect = Connect(result_collector_mock)
        connect.arguments = "GET http://api.sample.pl, AUTH DIGEST sampleUsername samplePassword"
        auth = connect.get_auth()

        self.assertIsInstance(auth, requests.auth.HTTPDigestAuth)

    @mock.patch('src.result_collector.ResultCollector')
    def test_none_auth(self, result_collector_mock):
        connect = Connect(result_collector_mock)
        connect.arguments = "GET http://api.sample.pl"
        auth = connect.get_auth()

        self.assertEqual(auth, [])

    @mock.patch('src.result_collector.ResultCollector')
    def test_if_exists_keyword_allow_redirects_then_allow_redirects(self, result_collector_mock):
        connect = Connect(result_collector_mock)
        connect.arguments = "GET http://api.sample.pl, ALLOW REDIRECTS"

        self.assertTrue(connect.get_allow_redirects())

    @mock.patch('src.result_collector.ResultCollector')
    def test_if_not_exists_keyword_allow_redirects_then_does_not_allow_redirects(self,
                                                                                 result_collector_mock):
        connect = Connect(result_collector_mock)
        connect.arguments = "GET http://api.sample.pl"

        self.assertFalse(connect.get_allow_redirects())