import unittest
from six import text_type, u, b, PY2, PY3
from nose.tools import raises
from expects import *
import httpretty
import textwrap
import json
import datetime
import pytz
from .validate_jwt import validate_jwt_header

from opentok import OpenTok, Archive, ArchiveList, OutputModes, OpenTokException, __version__

class OpenTokArchiveApiTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        self.session_id = u('SESSIONID')
        self.opentok = OpenTok(self.api_key, self.api_secret)

    @httpretty.activate
    def test_start_archive(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/project/{0}/archive').format(self.api_key),
                               body=textwrap.dedent(u("""\
                                       {
                                          "createdAt" : 1395183243556,
                                          "duration" : 0,
                                          "id" : "30b3ebf1-ba36-4f5b-8def-6f70d9986fe9",
                                          "name" : "",
                                          "partnerId" : 123456,
                                          "reason" : "",
                                          "sessionId" : "SESSIONID",
                                          "size" : 0,
                                          "status" : "started",
                                          "hasAudio": true,
                                          "hasVideo": true,
                                          "outputMode": "composed",
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.start_archive(self.session_id)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode('utf-8'))
        expect(body).to(have_key(u('name'), None))
        expect(body).to(have_key(u('sessionId'), u('SESSIONID')))
        expect(archive).to(be_an(Archive))
        expect(archive).to(have_property(u('id'), u('30b3ebf1-ba36-4f5b-8def-6f70d9986fe9')))
        expect(archive).to(have_property(u('name'), u('')))
        expect(archive).to(have_property(u('status'), u('started')))
        expect(archive).to(have_property(u('session_id'), u('SESSIONID')))
        expect(archive).to(have_property(u('partner_id'), 123456))
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395183243, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(1395183243, datetime.timezone.utc)
        expect(archive).to(have_property(u('created_at'), created_at))
        expect(archive).to(have_property(u('size'), 0))
        expect(archive).to(have_property(u('duration'), 0))
        expect(archive).to(have_property(u('has_audio'), True))
        expect(archive).to(have_property(u('has_video'), True))
        expect(archive).to(have_property(u('url'), None))

    @httpretty.activate
    def test_start_archive_with_name(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/project/{0}/archive').format(self.api_key),
                               body=textwrap.dedent(u("""\
                                       {
                                          "createdAt" : 1395183243556,
                                          "duration" : 0,
                                          "id" : "30b3ebf1-ba36-4f5b-8def-6f70d9986fe9",
                                          "name" : "ARCHIVE NAME",
                                          "partnerId" : 123456,
                                          "reason" : "",
                                          "sessionId" : "SESSIONID",
                                          "size" : 0,
                                          "status" : "started",
                                          "hasAudio": true,
                                          "hasVideo": true,
                                          "outputMode": "composed",
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.start_archive(self.session_id, name=u('ARCHIVE NAME'))

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode('utf-8'))
        expect(body).to(have_key(u('sessionId'), u('SESSIONID')))
        expect(body).to(have_key(u('name'), u('ARCHIVE NAME')))
        expect(archive).to(be_an(Archive))
        expect(archive).to(have_property(u('id'), u('30b3ebf1-ba36-4f5b-8def-6f70d9986fe9')))
        expect(archive).to(have_property(u('name'), ('ARCHIVE NAME')))
        expect(archive).to(have_property(u('status'), u('started')))
        expect(archive).to(have_property(u('session_id'), u('SESSIONID')))
        expect(archive).to(have_property(u('partner_id'), 123456))
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395183243, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(1395183243, datetime.timezone.utc)
        expect(archive).to(have_property(u('created_at'), equal(created_at)))
        expect(archive).to(have_property(u('size'), equal(0)))
        expect(archive).to(have_property(u('duration'), equal(0)))
        expect(archive).to(have_property(u('url'), equal(None)))

    @httpretty.activate
    def test_start_archive_with_standard_resolution(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/project/{0}/archive').format(self.api_key),
                               body=textwrap.dedent(u("""\
                                       {
                                          "createdAt" : 1395183243556,
                                          "duration" : 0,
                                          "id" : "30b3ebf1-ba36-4f5b-8def-6f70d9986fe9",
                                          "name" : "ARCHIVE NAME",
                                          "partnerId" : 123456,
                                          "reason" : "",
                                          "sessionId" : "SESSIONID",
                                          "size" : 0,
                                          "status" : "started",
                                          "hasAudio": true,
                                          "hasVideo": true,
                                          "outputMode": "composed",
                                          "url" : null,
                                          "resolution": "640x480"
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.start_archive(self.session_id, resolution="640x480")

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode('utf-8'))
        expect(body).to(have_key(u('sessionId'), u('SESSIONID')))
        expect(body).to(have_key(u('resolution'), u('640x480')))
        expect(archive).to(be_an(Archive))
        expect(archive).to(have_property(u('id'), u('30b3ebf1-ba36-4f5b-8def-6f70d9986fe9')))
        expect(archive).to(have_property(u('resolution'), "640x480"))
        expect(archive).to(have_property(u('status'), u('started')))
        expect(archive).to(have_property(u('session_id'), u('SESSIONID')))
        expect(archive).to(have_property(u('partner_id'), 123456))
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395183243, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(1395183243, datetime.timezone.utc)
        expect(archive).to(have_property(u('created_at'), equal(created_at)))
        expect(archive).to(have_property(u('size'), equal(0)))
        expect(archive).to(have_property(u('duration'), equal(0)))
        expect(archive).to(have_property(u('url'), equal(None)))

    @httpretty.activate
    def test_start_archive_with_hd_resolution(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/project/{0}/archive').format(self.api_key),
                               body=textwrap.dedent(u("""\
                                       {
                                          "createdAt" : 1395183243556,
                                          "duration" : 0,
                                          "id" : "30b3ebf1-ba36-4f5b-8def-6f70d9986fe9",
                                          "name" : "ARCHIVE NAME",
                                          "partnerId" : 123456,
                                          "reason" : "",
                                          "sessionId" : "SESSIONID",
                                          "size" : 0,
                                          "status" : "started",
                                          "hasAudio": true,
                                          "hasVideo": true,
                                          "outputMode": "composed",
                                          "url" : null,
                                          "resolution": "1280x720"
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.start_archive(self.session_id, resolution="1280x720")

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode('utf-8'))
        expect(body).to(have_key(u('sessionId'), u('SESSIONID')))
        expect(body).to(have_key(u('resolution'), u('1280x720')))
        expect(archive).to(be_an(Archive))
        expect(archive).to(have_property(u('id'), u('30b3ebf1-ba36-4f5b-8def-6f70d9986fe9')))
        expect(archive).to(have_property(u('resolution'), "1280x720"))
        expect(archive).to(have_property(u('status'), u('started')))
        expect(archive).to(have_property(u('session_id'), u('SESSIONID')))
        expect(archive).to(have_property(u('partner_id'), 123456))
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395183243, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(1395183243, datetime.timezone.utc)
        expect(archive).to(have_property(u('created_at'), equal(created_at)))
        expect(archive).to(have_property(u('size'), equal(0)))
        expect(archive).to(have_property(u('duration'), equal(0)))
        expect(archive).to(have_property(u('url'), equal(None)))

    def test_start_archive_individual_and_resolution_throws_error(self):
        self.assertRaises(OpenTokException,
            self.opentok.start_archive,
            session_id=self.session_id,
            output_mode=OutputModes.individual,
            resolution="640x480")

        self.assertRaises(OpenTokException,
            self.opentok.start_archive,
            session_id=self.session_id,
            output_mode=OutputModes.individual,
            resolution="1280x720")

    @httpretty.activate
    def test_start_voice_archive(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/project/{0}/archive').format(self.api_key),
                               body=textwrap.dedent(u("""\
                                       {
                                          "createdAt" : 1395183243556,
                                          "duration" : 0,
                                          "id" : "30b3ebf1-ba36-4f5b-8def-6f70d9986fe9",
                                          "name" : "ARCHIVE NAME",
                                          "partnerId" : 123456,
                                          "reason" : "",
                                          "sessionId" : "SESSIONID",
                                          "size" : 0,
                                          "status" : "started",
                                          "hasAudio": true,
                                          "hasVideo": false,
                                          "outputMode": "composed",
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.start_archive(self.session_id, name=u('ARCHIVE NAME'), has_video=False)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode('utf-8'))
        expect(body).to(have_key(u('sessionId'), u('SESSIONID')))
        expect(body).to(have_key(u('name'), u('ARCHIVE NAME')))
        expect(archive).to(be_an(Archive))
        expect(archive).to(have_property(u('id'), u('30b3ebf1-ba36-4f5b-8def-6f70d9986fe9')))
        expect(archive).to(have_property(u('name'), ('ARCHIVE NAME')))
        expect(archive).to(have_property(u('status'), u('started')))
        expect(archive).to(have_property(u('session_id'), u('SESSIONID')))
        expect(archive).to(have_property(u('partner_id'), 123456))
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395183243, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(1395183243, datetime.timezone.utc)
        expect(archive).to(have_property(u('created_at'), created_at))
        expect(archive).to(have_property(u('size'), 0))
        expect(archive).to(have_property(u('duration'), 0))
        expect(archive).to(have_property(u('has_audio'), True))
        expect(archive).to(have_property(u('has_video'), False))
        expect(archive).to(have_property(u('url'), None))

    @httpretty.activate
    def test_start_individual_archive(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/project/{0}/archive').format(self.api_key),
                               body=textwrap.dedent(u("""\
                                       {
                                          "createdAt" : 1395183243556,
                                          "duration" : 0,
                                          "id" : "30b3ebf1-ba36-4f5b-8def-6f70d9986fe9",
                                          "name" : "ARCHIVE NAME",
                                          "partnerId" : 123456,
                                          "reason" : "",
                                          "sessionId" : "SESSIONID",
                                          "size" : 0,
                                          "status" : "started",
                                          "hasAudio": true,
                                          "hasVideo": true,
                                          "outputMode": "individual",
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.start_archive(self.session_id, name=u('ARCHIVE NAME'), output_mode=OutputModes.individual)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode('utf-8'))
        expect(body).to(have_key(u('sessionId'), u('SESSIONID')))
        expect(body).to(have_key(u('name'), u('ARCHIVE NAME')))
        expect(archive).to(be_an(Archive))
        expect(archive).to(have_property(u('id'), u('30b3ebf1-ba36-4f5b-8def-6f70d9986fe9')))
        expect(archive).to(have_property(u('name'), ('ARCHIVE NAME')))
        expect(archive).to(have_property(u('status'), u('started')))
        expect(archive).to(have_property(u('session_id'), u('SESSIONID')))
        expect(archive).to(have_property(u('partner_id'), 123456))
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395183243, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(1395183243, datetime.timezone.utc)
        expect(archive).to(have_property(u('created_at'), created_at))
        expect(archive).to(have_property(u('size'), 0))
        expect(archive).to(have_property(u('duration'), 0))
        expect(archive).to(have_property(u('has_audio'), True))
        expect(archive).to(have_property(u('has_video'), True))
        expect(archive).to(have_property(u('output_mode'), OutputModes.individual))
        expect(archive).to(have_property(u('url'), None))

    @httpretty.activate
    def test_start_composed_archive(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/project/{0}/archive').format(self.api_key),
                               body=textwrap.dedent(u("""\
                                       {
                                          "createdAt" : 1395183243556,
                                          "duration" : 0,
                                          "id" : "30b3ebf1-ba36-4f5b-8def-6f70d9986fe9",
                                          "name" : "ARCHIVE NAME",
                                          "partnerId" : 123456,
                                          "reason" : "",
                                          "sessionId" : "SESSIONID",
                                          "size" : 0,
                                          "status" : "started",
                                          "hasAudio": true,
                                          "hasVideo": true,
                                          "outputMode": "composed",
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.start_archive(self.session_id, name=u('ARCHIVE NAME'), output_mode=OutputModes.composed)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode('utf-8'))
        expect(body).to(have_key(u('sessionId'), u('SESSIONID')))
        expect(body).to(have_key(u('name'), u('ARCHIVE NAME')))
        expect(archive).to(be_an(Archive))
        expect(archive).to(have_property(u('id'), u('30b3ebf1-ba36-4f5b-8def-6f70d9986fe9')))
        expect(archive).to(have_property(u('name'), ('ARCHIVE NAME')))
        expect(archive).to(have_property(u('status'), u('started')))
        expect(archive).to(have_property(u('session_id'), u('SESSIONID')))
        expect(archive).to(have_property(u('partner_id'), 123456))
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395183243, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(1395183243, datetime.timezone.utc)
        expect(archive).to(have_property(u('created_at'), created_at))
        expect(archive).to(have_property(u('size'), 0))
        expect(archive).to(have_property(u('duration'), 0))
        expect(archive).to(have_property(u('has_audio'), True))
        expect(archive).to(have_property(u('has_video'), True))
        expect(archive).to(have_property(u('output_mode'), OutputModes.composed))
        expect(archive).to(have_property(u('url'), None))

    @httpretty.activate
    def test_stop_archive(self):
        archive_id = u('30b3ebf1-ba36-4f5b-8def-6f70d9986fe9')
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/project/{0}/archive/{1}/stop').format(self.api_key, archive_id),
                               body=textwrap.dedent(u("""\
                                       {
                                          "createdAt" : 1395183243000,
                                          "duration" : 0,
                                          "id" : "30b3ebf1-ba36-4f5b-8def-6f70d9986fe9",
                                          "name" : "",
                                          "partnerId" : 123456,
                                          "reason" : "",
                                          "sessionId" : "SESSIONID",
                                          "size" : 0,
                                          "status" : "stopped",
                                          "hasAudio": true,
                                          "hasVideo": true,
                                          "outputMode": "composed",
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.stop_archive(archive_id)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        expect(archive).to(be_an(Archive))
        expect(archive).to(have_property(u('id'), archive_id))
        expect(archive).to(have_property(u('name'), u('')))
        expect(archive).to(have_property(u('status'), u('stopped')))
        expect(archive).to(have_property(u('session_id'), u('SESSIONID')))
        expect(archive).to(have_property(u('partner_id'), 123456))
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395183243, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(1395183243, datetime.timezone.utc)
        expect(archive).to(have_property(u('created_at'), created_at))
        expect(archive).to(have_property(u('size'), 0))
        expect(archive).to(have_property(u('duration'), 0))
        expect(archive).to(have_property(u('url'), None))

    @httpretty.activate
    def test_delete_archive(self):
        archive_id = u('30b3ebf1-ba36-4f5b-8def-6f70d9986fe9')
        httpretty.register_uri(httpretty.DELETE, u('https://api.opentok.com/v2/project/{0}/archive/{1}').format(self.api_key, archive_id),
                               body=u(''),
                               status=204)

        self.opentok.delete_archive(archive_id)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))

    @httpretty.activate
    def test_find_archive(self):
        archive_id = u('f6e7ee58-d6cf-4a59-896b-6d56b158ec71')
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/project/{0}/archive/{1}').format(self.api_key, archive_id),
                               body=textwrap.dedent(u("""\
                                       {
                                          "createdAt" : 1395187836000,
                                          "duration" : 62,
                                          "id" : "f6e7ee58-d6cf-4a59-896b-6d56b158ec71",
                                          "name" : "",
                                          "partnerId" : 123456,
                                          "reason" : "",
                                          "sessionId" : "SESSIONID",
                                          "size" : 8347554,
                                          "status" : "available",
                                          "hasAudio": true,
                                          "hasVideo": true,
                                          "outputMode": "composed",
                                          "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2Ff6e7ee58-d6cf-4a59-896b-6d56b158ec71%2Farchive.mp4?Expires=1395194362&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.get_archive(archive_id)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        expect(archive).to(be_an(Archive))
        expect(archive).to(have_property(u('id'), archive_id))
        expect(archive).to(have_property(u('name'), u('')))
        expect(archive).to(have_property(u('status'), u('available')))
        expect(archive).to(have_property(u('session_id'), u('SESSIONID')))
        expect(archive).to(have_property(u('partner_id'), 123456))
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395187836, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(1395187836, datetime.timezone.utc)
        expect(archive).to(have_property(u('created_at'), created_at))
        expect(archive).to(have_property(u('size'), 8347554))
        expect(archive).to(have_property(u('duration'), 62))
        expect(archive).to(have_property(u('url'), u('http://tokbox.com.archive2.s3.amazonaws.com/123456%2Ff6e7ee58-d6cf-4a59-896b-6d56b158ec71%2Farchive.mp4?Expires=1395194362&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')))

    @httpretty.activate
    def test_find_archives(self):
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/project/{0}/archive').format(self.api_key),
                               body=textwrap.dedent(u("""\
                                       {
                                          "count" : 6,
                                          "items" : [ {
                                            "createdAt" : 1395187930000,
                                            "duration" : 22,
                                            "id" : "ef546c5a-4fd7-4e59-ab3d-f1cfb4148d1d",
                                            "name" : "",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 2909274,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "outputMode": "composed",
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2Fef546c5a-4fd7-4e59-ab3d-f1cfb4148d1d%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          }, {
                                            "createdAt" : 1395187910000,
                                            "duration" : 14,
                                            "id" : "5350f06f-0166-402e-bc27-09ba54948512",
                                            "name" : "",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 1952651,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "outputMode": "composed",
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2F5350f06f-0166-402e-bc27-09ba54948512%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          }, {
                                            "createdAt" : 1395187836000,
                                            "duration" : 62,
                                            "id" : "f6e7ee58-d6cf-4a59-896b-6d56b158ec71",
                                            "name" : "",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 8347554,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "outputMode": "composed",
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2Ff6e7ee58-d6cf-4a59-896b-6d56b158ec71%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          }, {
                                            "createdAt" : 1395183243000,
                                            "duration" : 544,
                                            "id" : "30b3ebf1-ba36-4f5b-8def-6f70d9986fe9",
                                            "name" : "",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 78499758,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "outputMode": "composed",
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2F30b3ebf1-ba36-4f5b-8def-6f70d9986fe9%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          }, {
                                            "createdAt" : 1394396753000,
                                            "duration" : 24,
                                            "id" : "b8f64de1-e218-4091-9544-4cbf369fc238",
                                            "name" : "showtime again",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 2227849,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "outputMode": "composed",
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2Fb8f64de1-e218-4091-9544-4cbf369fc238%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          }, {
                                            "createdAt" : 1394321113000,
                                            "duration" : 1294,
                                            "id" : "832641bf-5dbf-41a1-ad94-fea213e59a92",
                                            "name" : "showtime",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 42165242,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "outputMode": "composed",
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2F832641bf-5dbf-41a1-ad94-fea213e59a92%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          } ]
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive_list = self.opentok.get_archives()

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        expect(archive_list).to(be_an(ArchiveList))
        expect(archive_list).to(have_property(u('count'), 6))
        expect(list(archive_list.items)).to(have_length(6))
        # TODO: we could inspect each item in the list

    @httpretty.activate
    def test_find_archives_with_offset(self):
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/project/{0}/archive').format(self.api_key),
                               body=textwrap.dedent(u("""\
                                       {
                                          "count" : 6,
                                          "items" : [ {
                                            "createdAt" : 1395183243000,
                                            "duration" : 544,
                                            "id" : "30b3ebf1-ba36-4f5b-8def-6f70d9986fe9",
                                            "name" : "",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 78499758,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2F30b3ebf1-ba36-4f5b-8def-6f70d9986fe9%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          }, {
                                            "createdAt" : 1394396753000,
                                            "duration" : 24,
                                            "id" : "b8f64de1-e218-4091-9544-4cbf369fc238",
                                            "name" : "showtime again",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 2227849,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2Fb8f64de1-e218-4091-9544-4cbf369fc238%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          }, {
                                            "createdAt" : 1394321113000,
                                            "duration" : 1294,
                                            "id" : "832641bf-5dbf-41a1-ad94-fea213e59a92",
                                            "name" : "showtime",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 42165242,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2F832641bf-5dbf-41a1-ad94-fea213e59a92%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          } ]
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive_list = self.opentok.get_archives(offset=3)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        expect(httpretty.last_request()).to(have_property(u('querystring'), {
            u('offset'): [u('3')]
        }))
        expect(archive_list).to(be_an(ArchiveList))
        expect(archive_list).to(have_property(u('count'), 6))
        expect(list(archive_list.items)).to(have_length(3))
        # TODO: we could inspect each item in the list

    @httpretty.activate
    def test_find_archives_with_count(self):
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/project/{0}/archive').format(self.api_key),
                               body=textwrap.dedent(u("""\
                                       {
                                          "count" : 6,
                                          "items" : [ {
                                            "createdAt" : 1395187930000,
                                            "duration" : 22,
                                            "id" : "ef546c5a-4fd7-4e59-ab3d-f1cfb4148d1d",
                                            "name" : "",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 2909274,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2Fef546c5a-4fd7-4e59-ab3d-f1cfb4148d1d%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          }, {
                                            "createdAt" : 1395187910000,
                                            "duration" : 14,
                                            "id" : "5350f06f-0166-402e-bc27-09ba54948512",
                                            "name" : "",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 1952651,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2F5350f06f-0166-402e-bc27-09ba54948512%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          } ]
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive_list = self.opentok.get_archives(count=2)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        expect(httpretty.last_request()).to(have_property(u('querystring'), {
            u('count'): [u('2')]
        }))
        expect(archive_list).to(be_an(ArchiveList))
        expect(archive_list).to(have_property(u('count'), 6))
        expect(list(archive_list.items)).to(have_length(2))
        # TODO: we could inspect each item in the list

    @httpretty.activate
    def test_find_archives_with_offset_and_count(self):
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/project/{0}/archive').format(self.api_key),
                               body=textwrap.dedent(u("""\
                                       {
                                          "count" : 6,
                                          "items" : [ {
                                            "createdAt" : 1395187836000,
                                            "duration" : 62,
                                            "id" : "f6e7ee58-d6cf-4a59-896b-6d56b158ec71",
                                            "name" : "",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 8347554,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2Ff6e7ee58-d6cf-4a59-896b-6d56b158ec71%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          }, {
                                            "createdAt" : 1395183243000,
                                            "duration" : 544,
                                            "id" : "30b3ebf1-ba36-4f5b-8def-6f70d9986fe9",
                                            "name" : "",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 78499758,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2F30b3ebf1-ba36-4f5b-8def-6f70d9986fe9%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          }, {
                                            "createdAt" : 1394396753000,
                                            "duration" : 24,
                                            "id" : "b8f64de1-e218-4091-9544-4cbf369fc238",
                                            "name" : "showtime again",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 2227849,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2Fb8f64de1-e218-4091-9544-4cbf369fc238%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          }, {
                                            "createdAt" : 1394321113000,
                                            "duration" : 1294,
                                            "id" : "832641bf-5dbf-41a1-ad94-fea213e59a92",
                                            "name" : "showtime",
                                            "partnerId" : 123456,
                                            "reason" : "",
                                            "sessionId" : "SESSIONID",
                                            "size" : 42165242,
                                            "status" : "available",
                                            "hasAudio": true,
                                            "hasVideo": true,
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2F832641bf-5dbf-41a1-ad94-fea213e59a92%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          } ]
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive_list = self.opentok.get_archives(count=4, offset=2)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        expect(httpretty.last_request()).to(have_property(u('querystring'), {
            u('offset'): [u('2')],
            u('count'): [u('4')]
        }))
        expect(archive_list).to(be_an(ArchiveList))
        expect(archive_list).to(have_property(u('count'), 6))
        expect(list(archive_list.items)).to(have_length(4))
        # TODO: we could inspect each item in the list

    @httpretty.activate
    def test_find_paused_archive(self):
        archive_id = u('f6e7ee58-d6cf-4a59-896b-6d56b158ec71')
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/project/{0}/archive/{1}').format(self.api_key, archive_id),
                               body=textwrap.dedent(u("""\
                                       {
                                          "createdAt" : 1395187836000,
                                          "duration" : 62,
                                          "id" : "f6e7ee58-d6cf-4a59-896b-6d56b158ec71",
                                          "name" : "",
                                          "partnerId" : 123456,
                                          "reason" : "",
                                          "sessionId" : "SESSIONID",
                                          "size" : 8347554,
                                          "status" : "paused",
                                          "hasAudio": true,
                                          "hasVideo": true,
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.get_archive(archive_id)

        expect(archive).to(be_an(Archive))
        expect(archive).to(have_property(u('status'), u('paused')))

    @httpretty.activate
    def test_find_expired_archive(self):
        archive_id = u('f6e7ee58-d6cf-4a59-896b-6d56b158ec71')
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/project/{0}/archive/{1}').format(self.api_key, archive_id),
                               body=textwrap.dedent(u("""\
                                       {
                                          "createdAt" : 1395187836000,
                                          "duration" : 62,
                                          "id" : "f6e7ee58-d6cf-4a59-896b-6d56b158ec71",
                                          "name" : "",
                                          "partnerId" : 123456,
                                          "reason" : "",
                                          "sessionId" : "SESSIONID",
                                          "size" : 8347554,
                                          "status" : "expired",
                                          "hasAudio": true,
                                          "hasVideo": true,
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.get_archive(archive_id)

        expect(archive).to(be_an(Archive))
        expect(archive).to(have_property(u('status'), u('expired')))

    @httpretty.activate
    def test_find_archive_with_unknown_properties(self):
        archive_id = u('f6e7ee58-d6cf-4a59-896b-6d56b158ec71')
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/project/{0}/archive/{1}').format(self.api_key, archive_id),
                               body=textwrap.dedent(u("""\
                                       {
                                          "createdAt" : 1395187836000,
                                          "duration" : 62,
                                          "id" : "f6e7ee58-d6cf-4a59-896b-6d56b158ec71",
                                          "name" : "",
                                          "partnerId" : 123456,
                                          "reason" : "",
                                          "sessionId" : "SESSIONID",
                                          "size" : 8347554,
                                          "status" : "expired",
                                          "url" : null,
                                          "hasAudio": true,
                                          "hasVideo": true,
                                          "notarealproperty" : "not a real value"
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.get_archive(archive_id)

        expect(archive).to(be_an(Archive))
