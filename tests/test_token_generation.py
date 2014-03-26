import unittest
from six import text_type
from nose.tools import raises

from opentok import OpenTok

class OpenTokTokenGenerationTest(unittest.TestCase):
    def setUp(self):
        self.api_key = '123456'
        self.api_secret = '1234567890abcdef1234567890abcdef1234567890'
        self.session_id = '1_MX4xMjM0NTZ-flNhdCBNYXIgMTUgMTQ6NDI6MjMgUERUIDIwMTR-MC40OTAxMzAyNX4'
        self.opentok = OpenTok(self.api_key, self.api_secret)

    def test_generate_plain_token(self):
        token = self.opentok.generate_token(self.session_id)
        assert isinstance(token, text_type)
