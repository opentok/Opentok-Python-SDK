import unittest
from six import text_type, u
from nose.tools import raises
import time

from opentok import OpenTok, Roles, OpenTokException

from .helpers import token_decoder, token_signature_validator

class OpenTokTokenGenerationTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        self.session_id = u('1_MX4xMjM0NTZ-flNhdCBNYXIgMTUgMTQ6NDI6MjMgUERUIDIwMTR-MC40OTAxMzAyNX4')
        self.opentok = OpenTok(self.api_key, self.api_secret)

    def test_generate_plain_token(self):
        token = self.opentok.generate_token(self.session_id)
        assert isinstance(token, text_type)
        assert token_decoder(token)[u('session_id')] == self.session_id
        assert token_signature_validator(token, self.api_secret)

    def test_generate_role_token(self):
        token = self.opentok.generate_token(self.session_id, Roles.moderator)
        assert isinstance(token, text_type)
        assert token_decoder(token)[u('role')] == Roles.moderator.value
        assert token_signature_validator(token, self.api_secret)
        token = self.opentok.generate_token(self.session_id, role=Roles.moderator)
        assert isinstance(token, text_type)
        assert token_decoder(token)[u('role')] == Roles.moderator.value
        assert token_signature_validator(token, self.api_secret)

    def test_generate_expires_token(self):
        expire_time = time.time()
        token = self.opentok.generate_token(self.session_id, expire_time=expire_time)
        assert isinstance(token, text_type)
        assert token_decoder(token)[u('expire_time')] == text_type(int(expire_time))
        assert token_signature_validator(token, self.api_secret)

    def test_generate_data_token(self):
        data = u('name=Johnny')
        token = self.opentok.generate_token(self.session_id, connection_data=data)
        assert isinstance(token, text_type)
        assert token_decoder(token)[u('connection_data')] == data
        assert token_signature_validator(token, self.api_secret)

    @raises(TypeError)
    def test_does_not_generate_token_without_params(self):
        token = self.opentok.generate_token()

    @raises(TypeError)
    def test_does_not_generate_token_without_session(self):
        token = self.opentok.generate_token(role=Roles.subscriber)

    # TODO: this requires decoding session_id to check for api_key
    def test_does_not_generate_token_invalid_session(self):
        pass

    # TODO: all the things that raise OpenTokException
