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

from opentok import OpenTok, Archive, __version__, OutputModes, ArchiveResolution

class OpenTokArchiveResolutionTest(unittest.TestCase):
    def test_parse_SD(self):
        self.assertEqual(ArchiveResolution.fromValue("640x480"), ArchiveResolution.SD)

    def test_parse_HD(self):
        self.assertEqual(ArchiveResolution.fromValue("1280x720"), ArchiveResolution.HD)

    def test_parse_None(self):
        self.assertEqual(ArchiveResolution.fromValue(None), None)

class OpenTokArchiveTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        self.opentok = OpenTok(self.api_key, self.api_secret)

    @httpretty.activate
    def test_stop_archive(self):
        archive_id = u('ARCHIVEID')
        archive = Archive(self.opentok, {
            u('createdAt'): 1395183243556,
            u('duration'): 0,
            u('id'): archive_id,
            u('name'): u(''),
            u('partnerId'): 123456,
            u('reason'): u(''),
            u('sessionId'): u('SESSIONID'),
            u('size'): 0,
            u('status'): u('started'),
            u('hasAudio'): True,
            u('hasVideo'): True,
            u('outputMode'): OutputModes.composed.value,
            u('url'): None,
        })
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/project/{0}/archive/{1}/stop').format(self.api_key, archive_id),
                               body=textwrap.dedent(u("""\
                                       {
                                          "createdAt" : 1395183243556,
                                          "duration" : 0,
                                          "id" : "ARCHIVEID",
                                          "name" : "",
                                          "partnerId" : 123456,
                                          "reason" : "",
                                          "sessionId" : "SESSIONID",
                                          "size" : 0,
                                          "status" : "stopped",
                                          "hasAudio": true,
                                          "hasVideo": false,
                                          "outputMode": "composed",
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive.stop()

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
        expect(archive).to(have_property(u('has_audio'), True))
        expect(archive).to(have_property(u('has_video'), False))
        expect(archive).to(have_property(u('output_mode'), OutputModes.composed))
        expect(archive).to(have_property(u('url'), None))

    @httpretty.activate
    def test_delete_archive(self):
        archive_id = u('ARCHIVEID')
        archive = Archive(self.opentok, {
            u('createdAt'): 1395183243556,
            u('duration'): 0,
            u('id'): archive_id,
            u('name'): u(''),
            u('partnerId'): 123456,
            u('reason'): u(''),
            u('sessionId'): u('SESSIONID'),
            u('size'): 0,
            u('status'): u('available'),
            u('hasAudio'): True,
            u('hasVideo'): True,
            u('outputMode'): OutputModes.composed.value,
            u('url'): None,
        })
        httpretty.register_uri(httpretty.DELETE, u('https://api.opentok.com/v2/project/{0}/archive/{1}').format(self.api_key, archive_id),
                               body=u(''),
                               status=204)

        archive.delete()

        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        # TODO: test that the object is invalidated
