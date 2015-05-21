import unittest
from six import text_type, u, b, PY2, PY3
from six.moves.urllib.parse import parse_qs
from nose.tools import raises
from sure import expect
import httpretty
import os
from opentok import OpenTok, Session, MediaModes, OpenTokException, __version__

class OpenTokSessionCreationTest(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ.get('API_KEY') or u('123456')
        self.api_secret = (os.environ.get('API_SECRET') or
            u('1234567890abcdef1234567890abcdef1234567890'))
        self.api_url = os.environ.get('API_URL')
        self.mock = not (os.environ.get('API_MOCK') == 'FALSE')

        if self.mock or self.api_url is None:
            self.opentok = OpenTok(self.api_key, self.api_secret)
        else:
            self.opentok = OpenTok(self.api_key, self.api_secret, api_url = self.api_url)

    def httpretty_enable(self):
        if self.mock:
            httpretty.enable()

    def httpretty_disable(self):
        if self.mock:
            httpretty.disable()

    def test_create_default_session(self):
        self.httpretty_enable()
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/session/create'),
                               body=u('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'),
                               status=200,
                               content_type=u('text/xml'))

        session = self.opentok.create_session()
        if self.mock:
            expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
            expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
            expect(httpretty.last_request().body).to.equal(b('p2p.preference=enabled'))

        expect(session).to.be.a(Session)
        if self.mock:
            expect(session).to.have.property(u('session_id')).being.equal(u('1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg'))
        expect(session).to.have.property(u('media_mode')).being.equal(MediaModes.relayed)
        expect(session).to.have.property(u('location')).being.equal(None)
        self.httpretty_disable()

    def test_create_routed_session(self):
        self.httpretty_enable()
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/session/create'),
                               body=u('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'),
                               status=200,
                               content_type=u('text/xml'))

        session = self.opentok.create_session(media_mode=MediaModes.routed)

        if self.mock:
            expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
            expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
            expect(httpretty.last_request().body).to.equal(b('p2p.preference=disabled'))

        expect(session).to.be.a(Session)
        if self.mock:
            expect(session).to.have.property(u('session_id')).being.equal(u('1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg'))
        expect(session).to.have.property(u('media_mode')).being.equal(MediaModes.routed)
        expect(session).to.have.property(u('location')).being.equal(None)
        self.httpretty_disable()

    def test_create_session_with_location_hint(self):
        self.httpretty_enable()
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/session/create'),
                               body=u('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'),
                               status=200,
                               content_type=u('text/xml'))

        session = self.opentok.create_session(location='12.34.56.78')

        if self.mock:
            expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
            expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        # ordering of keys is non-deterministic, must parse the body to see if it is correct
            body = parse_qs(httpretty.last_request().body)
            expect(body).to.have.key(b('location')).being.equal([b('12.34.56.78')])
            expect(body).to.have.key(b('p2p.preference')).being.equal([b('enabled')])

        expect(session).to.be.a(Session)
        if self.mock:
            expect(session).to.have.property(u('session_id')).being.equal(u('1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg'))
        expect(session).to.have.property(u('media_mode')).being.equal(MediaModes.relayed)
        expect(session).to.have.property(u('location')).being.equal(u('12.34.56.78'))
        self.httpretty_disable()

    def test_create_routed_session_with_location_hint(self):
        self.httpretty_enable()
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/session/create'),
                               body=u('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'),
                               status=200,
                               content_type=u('text/xml'))

        session = self.opentok.create_session(location='12.34.56.78', media_mode=MediaModes.routed)

        if self.mock:
            expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
            expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        
            # ordering of keys is non-deterministic, must parse the body to see if it is correct
            body = parse_qs(httpretty.last_request().body)
            expect(body).to.have.key(b('location')).being.equal([b('12.34.56.78')])
            expect(body).to.have.key(b('p2p.preference')).being.equal([b('disabled')])

        expect(session).to.be.a(Session)
        if self.mock:
            expect(session).to.have.property(u('session_id')).being.equal(u('1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg'))
        expect(session).to.have.property(u('media_mode')).being.equal(MediaModes.routed)
        expect(session).to.have.property(u('location')).being.equal(u('12.34.56.78'))
        self.httpretty_disable()

    # TODO: all the cases that throw exceptions
    # TODO: custom api_url requests
