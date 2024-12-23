import unittest
from six import text_type, u, b, PY2, PY3
from expects import *

from opentok import Client, __version__
import time
from jwt import decode


class JwtCustomClaimsTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.session_id = u(
            "1_MX4xMjM0NTZ-flNhdCBNYXIgMTUgMTQ6NDI6MjMgUERUIDIwMTR-MC40OTAxMzAyNX4"
        )
        self.opentok = Client(self.api_key, self.api_secret)

    def test_livetime_custom_claim(self):
        self.opentok.jwt_livetime = 5  # Token will expire 5 minutes in the future
        jwt_token = self.opentok._create_jwt_auth_header()
        claims = decode(jwt_token, self.api_secret, algorithms=[u("HS256")])
        expect(claims).to(have_key(u("exp")))
        expect(int(claims[u("exp")])).to(
            be_above(int(time.time()) + (60 * 4))
        )  # above of 4 min
        expect(int(claims[u("exp")])).to(
            be_below(int(time.time()) + (60 * 6))
        )  # below of 6 min
