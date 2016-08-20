import unittest
import json
from six import text_type, u, b, PY2, PY3
from nose.tools import raises
from expects import *
import httpretty
import textwrap
from .validate_jwt import validate_jwt_header

from opentok import OpenTok, OpenTokException, RequestError, AuthError, NotFoundError, __version__

class OpenTokSignalTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        self.session_id = u('session_id')
        self.connection_id = u('connection_id')
        self.signal_type = u("SIGNAL_TYPE")
        self.signal_data = u("SIGNAL_DATA")
        self.payload = { 'type': self.signal_type, 'data': self.signal_data }
        self.opentok = OpenTok(self.api_key, self.api_secret)

    def register_uri(self, status, connection, payload):
        uri = u('https://api.opentok.com/v2/partner/{0}/session/{1}/signal').format(
            self.api_key, self.session_id)
        if connection:
            uri = u('https://api.opentok.com/v2/partner/{0}/session/{1}/connection/{2}/signal').format(
                self.api_key, self.session_id, self.connection_id)

        httpretty.register_uri(httpretty.POST, uri,
                               body=u(json.dumps(payload)),
                               status=status)

    def verify_headers(self):
        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))

    def verify_body(self, signal_type, signal_data):
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode('utf-8'))
        if signal_type:
            expect(body).to(have_key(u('type'), signal_type))
        if signal_data:
            expect(body).to(have_key(u('data'), signal_data))

    def verify_signal(self, connection, payload):
        self.register_uri(200, connection, payload)

        self.opentok.signal(self.session_id, self.connection_id if connection else None, payload);

        self.verify_headers()
        self.verify_body(payload.get('type'), payload.get('data'))

    @httpretty.activate
    def test_signal_session(self):
        self.verify_signal(False, { 'type': self.signal_type, 'data': self.signal_data })

    @httpretty.activate
    def test_signal_session_no_type(self):
        self.verify_signal(False, { 'data': self.signal_data })

    @httpretty.activate
    def test_signal_session_no_data(self):
        self.verify_signal(False, { 'type': self.signal_type })

    @httpretty.activate
    def test_signal_connection(self):
        self.verify_signal(True, { 'type': self.signal_type, 'data': self.signal_data })

    @httpretty.activate
    def test_signal_connection_no_type(self):
        self.verify_signal(True, { 'data': self.signal_data })

    @httpretty.activate
    def test_signal_connection_no_data(self):
        self.verify_signal(True, { 'type': self.signal_type })

    def verify_exception(self, status, exception, session_id, connection_id, payload):
        self.register_uri(status, True, payload)

        self.assertRaises(exception, self.opentok.signal, session_id, connection_id, payload)

    @httpretty.activate
    def test_signal_no_session(self):
        self.verify_exception(200, OpenTokException, None, None, self.payload)
        expect(httpretty.has_request()).to(be_false)

    @httpretty.activate
    def test_signal_no_payload(self):
        self.verify_exception(200, OpenTokException, self.session_id, None, None)
        expect(httpretty.has_request()).to(be_false)

    @httpretty.activate
    def test_signal_bad_request(self):
        self.verify_exception(400, RequestError, self.session_id, self.connection_id, self.payload)

    @httpretty.activate
    def test_signal_not_found(self):
        self.verify_exception(404, NotFoundError, self.session_id, self.connection_id, self.payload)

    @httpretty.activate
    def test_signal_unauthorized(self):
        self.verify_exception(403, AuthError, self.session_id, self.connection_id, self.payload)
