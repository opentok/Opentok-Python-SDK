import unittest
from six import text_type, u

from opentok import Client, Session, Roles, MediaModes
from .helpers import token_decoder


class SessionTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.session_id = u(
            "1_MX4xMjM0NTZ-flNhdCBNYXIgMTUgMTQ6NDI6MjMgUERUIDIwMTR-MC40OTAxMzAyNX4"
        )
        self.opentok = Client(self.api_key, self.api_secret)

    def test_generate_token(self):
        session = Session(
            self.opentok, self.session_id, media_mode=MediaModes.routed, location=None
        )
        token = session.generate_token()
        assert isinstance(token, text_type)
        assert token_decoder(token, self.api_secret)[u("session_id")] == self.session_id

    def test_generate_role_token(self):
        session = Session(
            self.opentok, self.session_id, media_mode=MediaModes.routed, location=None
        )
        token = session.generate_token(role=Roles.moderator)
        assert isinstance(token, text_type)
        assert token_decoder(token, self.api_secret)[u("session_id")] == self.session_id
        assert token_decoder(token, self.api_secret)[u("role")] == u("moderator")
