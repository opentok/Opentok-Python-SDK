import unittest
from six import text_type, u, b, PY2, PY3
from nose.tools import raises
from sure import expect
import httpretty
import textwrap
import json

from opentok import OpenTok, Archive, __version__

class OpenTokArchiveApiTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        self.session_id = u('SESSIONID')
        # self.api_key = u('854511')
        # self.api_secret = u('***REMOVED***')
        # self.session_id = u('2_MX44NTQ1MTF-flR1ZSBOb3YgMTIgMDk6NDA6NTkgUFNUIDIwMTN-MC43NjU0Nzh-')
        self.opentok = OpenTok(self.api_key, self.api_secret)

    @httpretty.activate
    def test_start_archive(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/partner/{0}/archive').format(self.api_key),
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
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.start_archive(self.session_id)
        #print(archive.json())

        expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        expect(httpretty.last_request().headers[u('content-type')]).to.equal(u('application/json'))
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode('utf-8'))
        expect(body).to.have.key(u('name')).being.equal(None)
        expect(body).to.have.key(u('sessionId')).being.equal(u('SESSIONID'))
        expect(archive).to.be.an(Archive)
        expect(archive).to.have.property(u('id')).being.equal(u('30b3ebf1-ba36-4f5b-8def-6f70d9986fe9'))
        expect(archive).to.have.property(u('name')).being.equal(u(''))
        expect(archive).to.have.property(u('status')).being.equal(u('started'))
        expect(archive).to.have.property(u('session_id')).being.equal(u('SESSIONID'))
        expect(archive).to.have.property(u('partner_id')).being.equal(123456)
        #expect(archive).to.have.property(u('created_at')).being.equal(None)
        expect(archive).to.have.property(u('size')).being.equal(0)
        expect(archive).to.have.property(u('duration')).being.equal(0)
        expect(archive).to.have.property(u('url')).being.equal(None)
