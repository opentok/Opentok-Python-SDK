# import time
# import urllib2
import unittest
from nose.tools import raises
# from xml.dom.minidom import parseString

from opentok import OpenTok #, OpenTokException

class OpenTokInitializationTest(unittest.TestCase):
    def setUp(self):
        self.api_key = '123456'
        self.api_secret = '1234567890abcdef1234567890abcdef1234567890'
        self.api_url = 'http://environment.example.com'

    def test_intialization(self):
        opentok = OpenTok(self.api_key, self.api_secret)
        assert isinstance(opentok, OpenTok)
        self.assertEquals(opentok.proxies, None)

    def test_set_proxies(self):
        opentok = OpenTok(self.api_key, self.api_secret)
        opentok.proxies = {'https': 'https://foo.bar'}
        self.assertEquals(opentok.proxies, {'https': 'https://foo.bar'})

    @raises(TypeError)
    def test_initialization_without_required_params(self):
        opentok = OpenTok()

    def test_initialization_with_api_url(self):
        opentok = OpenTok(self.api_key, self.api_secret, self.api_url)
        assert isinstance(opentok, OpenTok)

    def test_initialization_with_numeric_api_key(self):
        opentok = OpenTok(123456, self.api_secret)
        assert isinstance(opentok, OpenTok)

    def test_initialization_with_timeout(self):
        opentok = OpenTok(self.api_key, self.api_secret, timeout=5)
        assert isinstance(opentok, OpenTok)

if __name__ == '__main__':
        unittest.main()
