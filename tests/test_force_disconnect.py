import unittest
from six import u
from expects import *
import httpretty

from opentok import Client, __version__, AuthError, ForceDisconnectError
from .validate_jwt import validate_jwt_header


class OpenTokForceDisconnectTest(unittest.TestCase):
    """" Class that contains test for force disconnect functionality """

    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.opentok = Client(self.api_key, self.api_secret)
        self.session_id = u("SESSIONID")
        self.connection_id = u("CONNECTIONID")

    @httpretty.activate
    def test_force_disconnect(self):
        """ Method to test force disconnect functionality using an Client instance """

        httpretty.register_uri(
            httpretty.DELETE,
            u(
                "https://api.opentok.com/v2/project/{0}/session/{1}/connection/{2}"
            ).format(self.api_key, self.session_id, self.connection_id),
            status=204,
            content_type=u("application/json"),
        )

        self.opentok.force_disconnect(self.session_id, self.connection_id)

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )

    @httpretty.activate
    def test_throws_force_disconnect_exception(self):
        """ This method should throw a ForceDisconnectError """

        httpretty.register_uri(
            httpretty.DELETE,
            u(
                "https://api.opentok.com/v2/project/{0}/session/{1}/connection/{2}"
            ).format(self.api_key, self.session_id, self.connection_id),
            status=400,
            content_type=u("application/json"),
        )

        self.assertRaises(
            ForceDisconnectError,
            self.opentok.force_disconnect,
            self.session_id,
            self.connection_id,
        )

    @httpretty.activate
    def test_throws_auth_exception(self):
        """ This method should throw an AuthError """

        httpretty.register_uri(
            httpretty.DELETE,
            u(
                "https://api.opentok.com/v2/project/{0}/session/{1}/connection/{2}"
            ).format(self.api_key, self.session_id, self.connection_id),
            status=403,
            content_type=u("application/json"),
        )

        self.assertRaises(
            AuthError,
            self.opentok.force_disconnect,
            self.session_id,
            self.connection_id,
        )
