import unittest
from six import u
from nose.tools import raises
import httpretty
import requests

from opentok import OpenTok, OpenTokException

def _raise_timeout(*args):
    raise requests.Timeout('Timeout occurred')

class OpenTokSessionCreationTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        httpretty.enable()
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/session/create'),
                               body=_raise_timeout,
                               status=200,
                               content_type=u('text/xml'))

    def tearDown(self):
        httpretty.disable()

    @raises(OpenTokException)
    def test_timeout(self):
        opentok = OpenTok(self.api_key, self.api_secret, timeout=1)
        opentok.create_session()
