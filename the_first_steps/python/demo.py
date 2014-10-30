# coding=utf-8
__author__ = 'Damian Mirecki'

import unittest
import xml.etree.ElementTree as ET

import requests


class Demo(unittest.TestCase):
    def test_raises(self):
        self.assertRaises(requests.exceptions.Timeout, requests.get, "http://api.geonames.org/postalCodeSearch",
                          timeout=0.001)

    def test_xml(self):
        payload = {
            'postalcode': '50316',
            'username': 'indor'
        }

        r = requests.get("http://api.geonames.org/postalCodeSearch", params=payload)

        self.assertEqual('UTF-8', r.encoding)
        self.assertEqual(200, r.status_code)
        self.assertTrue(r.status_code == requests.codes.ok)

        self.assertTrue('content-length' in r.headers)
        self.assertLess(int(r.headers['content-length']), 3000)

        self.assertTrue('content-type' in r.headers)
        self.assertRegexpMatches(r.headers['content-type'], '.*xml.*')

        root = ET.fromstring(r.content)

        self.assertXmlHasWroclaw(root)

    def test_json(self):
        payload = {
            'postalcode': '50316',
            'username': 'indor'
        }

        r = requests.get("http://api.geonames.org/postalCodeSearchJSON", params=payload)

        self.assertRegexpMatches(r.headers['content-type'], '.*json.*')

        json = r.json()

        self.assertJsonHasWroclaw(json)

    def assertJsonHasWroclaw(self, json, msg=None):
        if all(element['placeName'] != u'Wrocław' for element in iter(json['postalCodes'])):
            raise self.failureException(msg)

    def assertXmlHasWroclaw(self, root, msg=None):
        if all(element.text != u'Wrocław' for element in root.findall("./code/name")):
            raise self.failureException(msg)


if __name__ == '__main__':
    unittest.main()