import unittest
from six import text_type, u, b, PY2, PY3
from nose.tools import raises
from sure import expect
import httpretty
from .validate_jwt import validate_jwt_header

from opentok import OpenTok, OpenTokException, RequestError, AuthError, NotFoundError, __version__

class OpenTokForceDisconnectTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        self.session_id = u('session_id')
        self.connection_id = u('connection_id')
        self.opentok = OpenTok(self.api_key, self.api_secret)

    def register_uri(self, status):
        httpretty.register_uri(httpretty.DELETE, u('https://api.opentok.com/v2/partner/{}/session/{}/connection/{}').format(self.api_key, self.session_id, self.connection_id),
                               status=status)

    def verify_headers(self):
        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)

    def verify_body(self):
        body = httpretty.last_request().body
        expect(body).to.be.false

    @httpretty.activate
    def test_force_disconnect(self):
        self.register_uri(200)

        self.opentok.force_disconnect(self.session_id, self.connection_id)

        self.verify_headers()
        self.verify_body()

    def verify_exception(self, status, exception, session_id, connection_id):
        self.register_uri(status)

        self.assertRaises(exception, self.opentok.force_disconnect, session_id, connection_id)

    @httpretty.activate
    def test_force_disconnect_empty(self):
        self.verify_exception(200, OpenTokException, None, None)
        expect(httpretty.has_request()).to.be.false

    @httpretty.activate
    def test_force_disconnect_bad_request(self):
        self.verify_exception(400, RequestError, self.session_id, self.connection_id)

    @httpretty.activate
    def test_force_disconnect_not_found(self):
        self.verify_exception(404, NotFoundError, self.session_id, self.connection_id)

    @httpretty.activate
    def test_force_disconnect_unauthorized(self):
        self.verify_exception(403, AuthError, self.session_id, self.connection_id)
