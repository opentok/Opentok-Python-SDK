import unittest
from six import text_type, u, b, PY2, PY3
from nose.tools import raises

from opentok import OpenTok, Session, Roles, MediaModes
from .helpers import token_decoder, token_signature_validator


class SessionTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.session_id = u(
            "1_MX4xMjM0NTZ-flNhdCBNYXIgMTUgMTQ6NDI6MjMgUERUIDIwMTR-MC40OTAxMzAyNX4"
        )
        self.opentok = OpenTok(self.api_key, self.api_secret)

    def test_generate_token(self):
        session = Session(
            self.opentok, self.session_id, media_mode=MediaModes.routed, location=None
        )
        token = session.generate_token()
        assert isinstance(token, text_type)
        assert token_decoder(token)[u("session_id")] == self.session_id
        assert token_signature_validator(token, self.api_secret)

    def test_generate_role_token(self):
        session = Session(
            self.opentok, self.session_id, media_mode=MediaModes.routed, location=None
        )
        token = session.generate_token(role=Roles.moderator)
        assert isinstance(token, text_type)
        assert token_decoder(token)[u("session_id")] == self.session_id
        assert token_decoder(token)[u("role")] == u("moderator")
        assert token_signature_validator(token, self.api_secret)
