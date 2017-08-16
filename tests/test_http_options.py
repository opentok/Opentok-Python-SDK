import unittest
from six import text_type, u, b, PY2, PY3
from six.moves.urllib.parse import parse_qs
from nose.tools import raises
from sure import expect
import httpretty

from opentok import OpenTok, Session, MediaModes, OpenTokException, __version__

class OpenTokSessionCreationTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        httpretty.enable()
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/session/create'),
                               body=u('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'),
                               status=200,
                               content_type=u('text/xml'))

    def tearDown(self):
        httpretty.disable()

    def test_timeout(self):
        # TODO: tell httpretty to timeout
        opentok = OpenTok(self.api_key, self.api_secret, timeout=5)

        session = opentok.create_session()

        # TODO: expect an exception
