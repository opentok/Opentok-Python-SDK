import pytest
import unittest
from six import text_type, u
import time
import datetime
import calendar

from opentok import Client, Roles, OpenTokException

from .helpers import token_decoder, token_signature_validator


class OpenTokTokenGenerationTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.session_id = u(
            "1_MX4xMjM0NTZ-flNhdCBNYXIgMTUgMTQ6NDI6MjMgUERUIDIwMTR-MC40OTAxMzAyNX4"
        )
        self.opentok = Client(self.api_key, self.api_secret)

    def test_generate_plain_token_t1(self):
        token = self.opentok.generate_token(self.session_id, use_jwt=False)
        assert isinstance(token, text_type)
        assert token_decoder(token)[u("session_id")] == self.session_id
        assert token_signature_validator(token, self.api_secret)

    def test_generate_plain_token_jwt(self):
        token = self.opentok.generate_token(self.session_id)
        assert isinstance(token, text_type)
        assert token_decoder(token, self.api_secret)[u("session_id")] == self.session_id

    def test_generate_plain_token_jwt_vonage_wrapper(self):
        self.api_secret = './tests/fake_data/dummy_private_key.txt'
        vonage_wrapper = Client(self.api_key, self.api_secret)
        public_key = ""
        with open('./tests/fake_data/dummy_public_key.txt', 'r') as file:
            public_key = file.read()

        token = vonage_wrapper.generate_token(self.session_id)
        assert isinstance(token, text_type)
        assert token_decoder(token, public_key)[u("session_id")] == self.session_id

    def test_generate_role_token(self):
        token = self.opentok.generate_token(self.session_id, Roles.moderator)
        assert isinstance(token, text_type)
        assert token_decoder(token, self.api_secret)[u("role")] == Roles.moderator.value

        token = self.opentok.generate_token(self.session_id, role=Roles.moderator)
        assert isinstance(token, text_type)
        assert token_decoder(token, self.api_secret)[u("role")] == Roles.moderator.value

        token = self.opentok.generate_token(self.session_id, Roles.publisher_only)
        assert token_decoder(token, self.api_secret)["role"] == Roles.publisher_only.value

    def test_generate_expires_token(self):
        # an integer is a valid argument
        expire_time = int(time.time()) + 100
        token = self.opentok.generate_token(self.session_id, expire_time=expire_time)
        assert isinstance(token, text_type)
        print(token_decoder(token, self.api_secret))
        assert token_decoder(token, self.api_secret)[u("exp")] == expire_time
        # anything that can be coerced into an integer is also valid
        expire_time = text_type(int(time.time()) + 100)
        token = self.opentok.generate_token(self.session_id, expire_time=expire_time)
        assert isinstance(token, text_type)
        assert token_decoder(token, self.api_secret)[u("exp")] == int(expire_time)
        # a datetime object is also valid
        expire_time = datetime.datetime.fromtimestamp(
            time.time(), datetime.timezone.utc
        ) + datetime.timedelta(days=1)
        token = self.opentok.generate_token(self.session_id, expire_time=expire_time)
        assert isinstance(token, text_type)
        assert token_decoder(token, self.api_secret)[u("exp")] == calendar.timegm(
            expire_time.utctimetuple()
        )

    def test_generate_data_token(self):
        data = u("name=Johnny")
        token = self.opentok.generate_token(self.session_id, data=data)
        assert isinstance(token, text_type)
        assert token_decoder(token, self.api_secret)[u("connection_data")] == data

    def test_generate_initial_layout_class_list(self):
        initial_layout_class_list = [u("focus"), u("small")]
        token = self.opentok.generate_token(
            self.session_id, initial_layout_class_list=initial_layout_class_list
        )
        assert isinstance(token, text_type)
        assert sorted(
            token_decoder(token, self.api_secret)[u("initial_layout_class_list")].split(
                u(" ")
            )
        ) == sorted(initial_layout_class_list)

    def test_generate_no_data_token(self):
        token = self.opentok.generate_token(self.session_id)
        assert isinstance(token, text_type)
        assert u("connection_data") not in token_decoder(token, self.api_secret)

    def test_does_not_generate_token_without_params(self):
        with pytest.raises(TypeError):
            self.opentok.generate_token()

    def test_does_not_generate_token_without_session(self):
        with pytest.raises(TypeError):
            self.opentok.generate_token(role=Roles.subscriber)

    def test_does_not_generate_token_invalid_session(self):
        with pytest.raises(OpenTokException):
            self.opentok.generate_token(u("NOT A REAL SESSIONID"))

    def test_does_not_generate_token_without_api_key_match(self):
        with pytest.raises(OpenTokException):
            # this session_id has the wrong api_key
            session_id = u(
                "1_MX42NTQzMjF-flNhdCBNYXIgMTUgMTQ6NDI6MjMgUERUIDIwMTR-MC40OTAxMzAyNX4"
            )
            self.opentok.generate_token(session_id)
