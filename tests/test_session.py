import unittest
from six import text_type, u, b, PY2, PY3
from nose.tools import raises
import httpretty
import textwrap
import json
from expects import *

from .validate_jwt import validate_jwt_header
from opentok import OpenTok, Session, Roles, MediaModes, __version__, Stream
from .helpers import token_decoder, token_signature_validator

class SessionTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        self.session_id = u('1_MX4xMjM0NTZ-flNhdCBNYXIgMTUgMTQ6NDI6MjMgUERUIDIwMTR-MC40OTAxMzAyNX4')
        self.opentok = OpenTok(self.api_key, self.api_secret)

    def test_generate_token(self):
        session = Session(self.opentok, self.session_id, media_mode=MediaModes.routed, location=None)
        token = session.generate_token()
        assert isinstance(token, text_type)
        assert token_decoder(token)[u('session_id')] == self.session_id
        assert token_signature_validator(token, self.api_secret)

    def test_generate_role_token(self):
        session = Session(self.opentok, self.session_id, media_mode=MediaModes.routed, location=None)
        token = session.generate_token(role=Roles.moderator)
        assert isinstance(token, text_type)
        assert token_decoder(token)[u('session_id')] == self.session_id
        assert token_decoder(token)[u('role')] == u('moderator')
        assert token_signature_validator(token, self.api_secret)

    @httpretty.activate
    def test_signal_from_session(self):
        data = {
            u('type'): u('type test'),
            u('data'): u('test data')
        }

        session = Session(self.opentok, self.session_id, media_mode=MediaModes.routed, location=None)

        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/project/{0}/session/{1}/signal').format(self.api_key, self.session_id),
                               body=textwrap.dedent(u("""\
                                       {
                                          "type": "type test",
                                          "data": "test data"
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        session.signal(data)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode('utf-8'))
        expect(body).to(have_key(u('type'), u('type test')))
        expect(body).to(have_key(u('data'), u('test data')))

    @httpretty.activate
    def test_signal_with_connection_id_from_session(self):
        data = {
            u('type'): u('type test'),
            u('data'): u('test data')
        }

        connection_id = u('da9cb410-e29b-4c2d-ab9e-fe65bf83fcaf')
        session = Session(self.opentok, self.session_id, media_mode=MediaModes.routed, location=None)

        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/project/{0}/session/{1}/connection/{2}/signal').format(self.api_key, self.session_id, connection_id),
                               body=textwrap.dedent(u("""\
                                       {
                                          "type": "type test",
                                          "data": "test data"
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        session.signal(data, connection_id)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode('utf-8'))
        expect(body).to(have_key(u('type'), u('type test')))
        expect(body).to(have_key(u('data'), u('test data')))

    @httpretty.activate
    def test_get_stream_from_session(self):
        stream_id = u('8b732909-0a06-46a2-8ea8-074e64d43422')
        session = Session(self.opentok, self.session_id, media_mode=MediaModes.routed, location=None)
        stream = Stream({
            u('id'): stream_id,
            u('videoType'): u('camera'),
            u('name'): u('stream name'),
            u('layoutClassList'): ['full']
        })

        httpretty.register_uri(
            httpretty.GET,
            u('https://api.opentok.com/v2/project/{0}/session/{1}/stream/{2}').format(self.api_key, session.session_id, stream_id),
            body=textwrap.dedent(u("""\
                   {
                      "id": "8b732909-0a06-46a2-8ea8-074e64d43422",
                      "videoType": "camera",
                      "name": "stream name",
                      "layoutClassList": ["full"]
                    }""")),
            status=200,
            content_type=u('application/json')
        )

        stream_response = session.get_stream(stream_id)
        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        expect(stream_response).to(be_an(Stream))
        expect(stream_response).to(have_property(u('id'), stream.id))
        expect(stream_response).to(have_property(u('videoType'), stream.videoType))
        expect(stream_response).to(have_property(u('name'), stream.name))
        expect(stream_response).to(have_property(u('layoutClassList'), stream.layoutClassList))
        expect(list(stream_response.layoutClassList)).to(have_length(1))

    @httpretty.activate
    def test_force_disconnect_from_session(self):
        """ Method to test force disconnect functionality using a Session instance """
        session = Session(self.opentok, self.session_id, media_mode=MediaModes.routed, location=None)
        connection_id = u('CONNECTIONID')

        httpretty.register_uri(
            httpretty.DELETE,
            u('https://api.opentok.com/v2/project/{0}/session/{1}/connection/{2}').format(
                self.api_key,
                self.session_id,
                connection_id
            ),
            status=200,
            content_type=u('application/json')
        )

        session.force_disconnect(connection_id)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
