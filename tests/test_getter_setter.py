import unittest
from six import u
from expects import *

from opentok import Client, __version__


class GetterSetterTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.session_id = u(
            "1_MX4xMjM0NTZ-flNhdCBNYXIgMTUgMTQ6NDI6MjMgUERUIDIwMTR-MC40OTAxMzAyNX4"
        )

        self.opentok = Client(self.api_key, self.api_secret)

    def test_getset_jwt_livetime(self):
        livetime = self.opentok.jwt_livetime
        self.opentok.jwt_livetime = 5
        assert self.opentok.jwt_livetime is not livetime