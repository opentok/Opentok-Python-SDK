import unittest
from six import text_type, u, b, PY2, PY3
from nose.tools import raises
from sure import expect
import httpretty
import json
import datetime
import pytz
from .validate_jwt import validate_jwt_header

from opentok import OpenTok, Callback, CallbackList, RequestError, OpenTokException, AuthError, NotFoundError, __version__

class OpenTokCallbackApiTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        self.session_id = u('SESSIONID')
        self.group = u('GROUP')
        self.event = u('EVENT')
        self.url = u('URL')
        self.callback_id = u('CALLBACK_ID')
        self.created_at = 1395183243000
        self.callback = {
            'id': self.callback_id,
            'createdAt': self.created_at,
            'event': self.event,
            'group': self.group,
            'url': self.url,
        }
        self.opentok = OpenTok(self.api_key, self.api_secret)

    def verify_headers(self):
        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)

    def verify_callback(self, callback):
        expect(callback).to.be.an(Callback)
        expect(callback).to.have.property(u('id')).being.equal(self.callback_id)
        expect(callback).to.have.property(u('group')).being.equal(self.group)
        expect(callback).to.have.property(u('event')).being.equal(self.event)
        expect(callback).to.have.property(u('url')).being.equal(self.url)
        if PY2:
            created_at = datetime.datetime.fromtimestamp(self.created_at / 1000, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(self.created_at / 1000, datetime.timezone.utc)
        expect(callback).to.have.property(u('created_at')).being.equal(created_at)

    # Register Callback Suite

    def register_register_uri(self, status):
        url = u('https://api.opentok.com/v2/partner/{}/callback').format(self.api_key)
        httpretty.register_uri(httpretty.POST, url,
                               body=u(json.dumps(self.callback)),
                               content_type=u('application/json'),
                               status=status)

    def verify_register_body(self):
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode('utf-8'))
        expect(body).to.have.key(u('group')).being.equal(self.group)
        expect(body).to.have.key(u('event')).being.equal(self.event)
        expect(body).to.have.key(u('url')).being.equal(self.url)

    @httpretty.activate
    def test_register_callback(self):
        self.register_register_uri(200)

        callback = self.opentok.register_callback(self.group, self.event, self.url)

        self.verify_headers()
        self.verify_register_body()
        self.verify_callback(callback)

    def verify_register_exception(self, status, exception, event, group, url):
        self.register_register_uri(status)

        self.assertRaises(exception, self.opentok.register_callback, event, group, url)

    @httpretty.activate
    def test_register_empty_group(self):
        self.verify_register_exception(200, OpenTokException, None, self.event, self.url)
        expect(httpretty.has_request()).to.be.false

    @httpretty.activate
    def test_register_empty_event(self):
        self.verify_register_exception(200, OpenTokException, self.group, None, self.url)
        expect(httpretty.has_request()).to.be.false

    @httpretty.activate
    def test_register_empty_url(self):
        self.verify_register_exception(200, OpenTokException, self.group, self.event, None)
        expect(httpretty.has_request()).to.be.false

    @httpretty.activate
    def test_register_bad_request(self):
        self.verify_register_exception(400, RequestError, self.group, self.event, self.url)

    @httpretty.activate
    def test_register_bad_request(self):
        self.verify_register_exception(404, NotFoundError, self.group, self.event, self.url)

    @httpretty.activate
    def test_register_unauthorized(self):
        self.verify_register_exception(403, AuthError, self.group, self.event, self.url)

    # Unregister Callback Suite

    def register_unregister_uri(self, status):
        url = u('https://api.opentok.com/v2/partner/{}/callback/{}').format(self.api_key, self.callback_id)
        httpretty.register_uri(httpretty.DELETE, url,
                               body=u(json.dumps(self.callback)),
                               content_type=u('application/json'),
                               status=status)

    def verify_unregister_body(self):
        body = httpretty.last_request().body
        expect(body).to.be.false

    def verify_unregister_exception(self, status, exception, callback_id):
        self.register_unregister_uri(status)

        self.assertRaises(exception, self.opentok.unregister_callback, callback_id)

    @httpretty.activate
    def test_unregister_callback(self):
        self.register_unregister_uri(200)

        self.opentok.unregister_callback(self.callback_id)

        self.verify_headers()
        self.verify_unregister_body()

    @httpretty.activate
    def test_unregister_empty(self):
        self.verify_unregister_exception(200, OpenTokException, None)

    @httpretty.activate
    def test_unregister_bad_request(self):
        self.verify_unregister_exception(400, RequestError, self.callback_id)

    @httpretty.activate
    def test_unregister_not_found(self):
        self.verify_unregister_exception(404, NotFoundError, self.callback_id)

    @httpretty.activate
    def test_unregister_unauthorized(self):
        self.verify_unregister_exception(403, AuthError, self.callback_id)

    # Get Callbacks Suite

    def register_list_uri(self, status):
        url = u('https://api.opentok.com/v2/partner/{}/callback').format(self.api_key, self.callback_id)
        httpretty.register_uri(httpretty.GET, url,
                               body=u(json.dumps([self.callback])),
                               content_type=u('application/json'),
                               status=status)

    def verify_list_body(self):
        body = httpretty.last_request().body
        expect(body).to.be.false

    def verify_callback_list(self, callbacks):
        expect(callbacks).to.be.an(CallbackList)
        expect(list(callbacks.items)).to.have.length_of(1)

        self.verify_callback(callbacks.items[0])

    def verify_list_exception(self, status, exception):
        self.register_list_uri(status)

        self.assertRaises(exception, self.opentok.get_callbacks)

    @httpretty.activate
    def test_get_callbacks(self):
        self.register_list_uri(200)

        callbacks = self.opentok.get_callbacks()

        self.verify_headers()
        self.verify_list_body()
        self.verify_callback_list(callbacks)

    @httpretty.activate
    def test_unregister_bad_request(self):
        self.verify_list_exception(400, RequestError)

    @httpretty.activate
    def test_unregister_unauthorized(self):
        self.verify_list_exception(403, AuthError)