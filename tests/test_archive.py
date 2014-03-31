import unittest
from six import text_type, u, b, PY2, PY3
from nose.tools import raises
from sure import expect
import httpretty
import textwrap
import json
import datetime
import pytz

from opentok import OpenTok, Archive, __version__

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
            u('url'): None,
        })
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/partner/{0}/archive/{1}/stop').format(self.api_key, archive_id),
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
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive.stop()

        expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        expect(httpretty.last_request().headers[u('content-type')]).to.equal(u('application/json'))
        expect(archive).to.be.an(Archive)
        expect(archive).to.have.property(u('id')).being.equal(archive_id)
        expect(archive).to.have.property(u('name')).being.equal(u(''))
        expect(archive).to.have.property(u('status')).being.equal(u('stopped'))
        expect(archive).to.have.property(u('session_id')).being.equal(u('SESSIONID'))
        expect(archive).to.have.property(u('partner_id')).being.equal(123456)
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395183243, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(1395183243, datetime.timezone.utc)
        expect(archive).to.have.property(u('created_at')).being.equal(created_at)
        expect(archive).to.have.property(u('size')).being.equal(0)
        expect(archive).to.have.property(u('duration')).being.equal(0)
        expect(archive).to.have.property(u('url')).being.equal(None)

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
            u('url'): None,
        })
        httpretty.register_uri(httpretty.DELETE, u('https://api.opentok.com/v2/partner/{0}/archive/{1}').format(self.api_key, archive_id),
                               body=u(''),
                               status=204)

        archive.delete()

        expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        expect(httpretty.last_request().headers[u('content-type')]).to.equal(u('application/json'))
        # TODO: test that the object is invalidated

