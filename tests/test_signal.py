import unittest
from six import text_type, u, b, PY2, PY3
from opentok import Client, Session, __version__
import httpretty
import json
import textwrap
from expects import *

from .validate_jwt import validate_jwt_header


class OpenTokSignalTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.opentok = Client(self.api_key, self.api_secret)
        self.session_id = u("SESSIONID")

    @httpretty.activate
    def test_signal(self):
        data = {u("type"): u("type test"), u("data"): u("test data")}

        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/v2/project/{0}/session/{1}/signal").format(
                self.api_key, self.session_id
            ),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "type": "type test",
                            "data": "test data"
                        }
                    """
                )
            ),
            status=204,
            content_type=u("application/json"),
        )

        self.opentok.send_signal(self.session_id, data)

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode("utf-8"))
        expect(body).to(have_key(u("type"), u("type test")))
        expect(body).to(have_key(u("data"), u("test data")))

    @httpretty.activate
    def test_signal_with_connection_id(self):
        data = {u("type"): u("type test"), u("data"): u("test data")}

        connection_id = u("da9cb410-e29b-4c2d-ab9e-fe65bf83fcaf")

        httpretty.register_uri(
            httpretty.POST,
            u(
                "https://api.opentok.com/v2/project/{0}/session/{1}/connection/{2}/signal"
            ).format(self.api_key, self.session_id, connection_id),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "type": "type test",
                            "data": "test data"
                        }
                    """
                )
            ),
            status=204,
            content_type=u("application/json"),
        )

        self.opentok.send_signal(self.session_id, data, connection_id)

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode("utf-8"))
        expect(body).to(have_key(u("type"), u("type test")))
        expect(body).to(have_key(u("data"), u("test data")))
