import unittest
from six import text_type, u, b, PY2, PY3
from nose.tools import raises
from sure import expect
import httpretty
import textwrap
import json
import datetime
import pytz
import os

from opentok import OpenTok, Archive, ArchiveList, __version__

class OpenTokArchiveApiTest(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ.get('API_KEY') or u('123456')
        self.api_secret = (os.environ.get('API_SECRET') or
            u('1234567890abcdef1234567890abcdef1234567890'))
        self.api_url = os.environ.get('API_URL')
        # self.mock = not (os.environ.get('API_MOCK') == 'FALSE')

        self.opentok = OpenTok(self.api_key, self.api_secret)
        self.session_id = u('SESSIONID')

    def httpretty_enable(self):
        httpretty.enable()

    def httpretty_disable(self):
        httpretty.disable()

    def test_start_archive(self):
        self.httpretty_enable()
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
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395183243, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(1395183243, datetime.timezone.utc)
        expect(archive).to.have.property(u('created_at')).being.equal(created_at)
        expect(archive).to.have.property(u('size')).being.equal(0)
        expect(archive).to.have.property(u('duration')).being.equal(0)
        expect(archive).to.have.property(u('url')).being.equal(None)
        self.httpretty_disable()

    def test_start_archive_with_name(self):
        self.httpretty_enable()
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/partner/{0}/archive').format(self.api_key),
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
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.start_archive(self.session_id, name=u('ARCHIVE NAME'))

        expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        expect(httpretty.last_request().headers[u('content-type')]).to.equal(u('application/json'))
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode('utf-8'))
        expect(body).to.have.key(u('sessionId')).being.equal(u('SESSIONID'))
        expect(body).to.have.key(u('name')).being.equal(u('ARCHIVE NAME'))
        expect(archive).to.be.an(Archive)
        expect(archive).to.have.property(u('id')).being.equal(u('30b3ebf1-ba36-4f5b-8def-6f70d9986fe9'))
        expect(archive).to.have.property(u('name')).being.equal(u('ARCHIVE NAME'))
        expect(archive).to.have.property(u('status')).being.equal(u('started'))
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
        self.httpretty_disable()

    def test_stop_archive_1(self):
        self.httpretty_enable()
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
        self.httpretty_disable()

    def test_stop_archive_2(self):
        self.httpretty_enable()
        archive_id = u('30b3ebf1-ba36-4f5b-8def-6f70d9986fe9')
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/partner/{0}/archive/{1}/stop').format(self.api_key, archive_id),
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
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.stop_archive(archive_id)

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
        self.httpretty_disable()


    def test_delete_archive_1(self):
        self.httpretty_enable()
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
        self.httpretty_disable()
        # TODO: test that the object is invalidated

    def test_delete_archive_2(self):
        self.httpretty_enable()
        archive_id = u('30b3ebf1-ba36-4f5b-8def-6f70d9986fe9')
        httpretty.register_uri(httpretty.DELETE, u('https://api.opentok.com/v2/partner/{0}/archive/{1}').format(self.api_key, archive_id),
                               body=u(''),
                               status=204)

        self.opentok.delete_archive(archive_id)

        expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        expect(httpretty.last_request().headers[u('content-type')]).to.equal(u('application/json'))
        self.httpretty_disable()

    def test_find_archive(self):
        self.httpretty_enable()
        archive_id = u('f6e7ee58-d6cf-4a59-896b-6d56b158ec71')
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/partner/{0}/archive/{1}').format(self.api_key, archive_id),
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
                                          "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2Ff6e7ee58-d6cf-4a59-896b-6d56b158ec71%2Farchive.mp4?Expires=1395194362&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.get_archive(archive_id)

        expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        expect(httpretty.last_request().headers[u('content-type')]).to.equal(u('application/json'))
        expect(archive).to.be.an(Archive)
        expect(archive).to.have.property(u('id')).being.equal(archive_id)
        expect(archive).to.have.property(u('name')).being.equal(u(''))
        expect(archive).to.have.property(u('status')).being.equal(u('available'))
        expect(archive).to.have.property(u('session_id')).being.equal(u('SESSIONID'))
        expect(archive).to.have.property(u('partner_id')).being.equal(123456)
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395187836, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(1395187836, datetime.timezone.utc)
        expect(archive).to.have.property(u('created_at')).being.equal(created_at)
        expect(archive).to.have.property(u('size')).being.equal(8347554)
        expect(archive).to.have.property(u('duration')).being.equal(62)
        expect(archive).to.have.property(u('url')).being.equal(u('http://tokbox.com.archive2.s3.amazonaws.com/123456%2Ff6e7ee58-d6cf-4a59-896b-6d56b158ec71%2Farchive.mp4?Expires=1395194362&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'))
        self.httpretty_disable()

    def test_find_archives(self):
        self.httpretty_enable()
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/partner/{0}/archive').format(self.api_key),
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
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2F832641bf-5dbf-41a1-ad94-fea213e59a92%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          } ]
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive_list = self.opentok.get_archives()

        expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        expect(httpretty.last_request().headers[u('content-type')]).to.equal(u('application/json'))
        expect(archive_list).to.be.an(ArchiveList)
        expect(archive_list).to.have.property(u('count')).being.equal(6)
        expect(list(archive_list.items)).to.have.length_of(6)
        self.httpretty_disable()
        # TODO: we could inspect each item in the list

    def test_find_archives_with_offset(self):
        self.httpretty_enable()
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/partner/{0}/archive').format(self.api_key),
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
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2F832641bf-5dbf-41a1-ad94-fea213e59a92%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          } ]
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive_list = self.opentok.get_archives(offset=3)

        expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        expect(httpretty.last_request().headers[u('content-type')]).to.equal(u('application/json'))
        expect(httpretty.last_request()).to.have.property("querystring").being.equal({
            u('offset'): [u('3')]
        })
        expect(archive_list).to.be.an(ArchiveList)
        expect(archive_list).to.have.property(u('count')).being.equal(6)
        expect(list(archive_list.items)).to.have.length_of(3)
        self.httpretty_disable()
        # TODO: we could inspect each item in the list

    def test_find_archives_with_count(self):
        self.httpretty_enable()
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/partner/{0}/archive').format(self.api_key),
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
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2F5350f06f-0166-402e-bc27-09ba54948512%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          } ]
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive_list = self.opentok.get_archives(count=2)

        expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        expect(httpretty.last_request().headers[u('content-type')]).to.equal(u('application/json'))
        expect(httpretty.last_request()).to.have.property("querystring").being.equal({
            u('count'): [u('2')]
        })
        expect(archive_list).to.be.an(ArchiveList)
        expect(archive_list).to.have.property(u('count')).being.equal(6)
        expect(list(archive_list.items)).to.have.length_of(2)
        self.httpretty_disable()
        # TODO: we could inspect each item in the list

    def test_find_archives_with_offset_and_count(self):
        self.httpretty_enable()
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/partner/{0}/archive').format(self.api_key),
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
                                            "url" : "http://tokbox.com.archive2.s3.amazonaws.com/123456%2F832641bf-5dbf-41a1-ad94-fea213e59a92%2Farchive.mp4?Expires=1395188695&AWSAccessKeyId=AKIAI6LQCPIXYVWCQV6Q&Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                          } ]
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive_list = self.opentok.get_archives(count=4, offset=2)

        expect(httpretty.last_request().headers[u('x-tb-partner-auth')]).to.equal(self.api_key+u(':')+self.api_secret)
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        expect(httpretty.last_request().headers[u('content-type')]).to.equal(u('application/json'))
        expect(httpretty.last_request()).to.have.property("querystring").being.equal({
            u('offset'): [u('2')],
            u('count'): [u('4')]
        })
        expect(archive_list).to.be.an(ArchiveList)
        expect(archive_list).to.have.property(u('count')).being.equal(6)
        expect(list(archive_list.items)).to.have.length_of(4)
        self.httpretty_disable()
        # TODO: we could inspect each item in the list

    def test_find_expired_archive(self):
        self.httpretty_enable()
        archive_id = u('f6e7ee58-d6cf-4a59-896b-6d56b158ec71')
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/partner/{0}/archive/{1}').format(self.api_key, archive_id),
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
                                          "url" : null
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.get_archive(archive_id)

        expect(archive).to.be.an(Archive)
        expect(archive).to.have.property(u('status')).being.equal(u('expired'))

    def test_find_archive_with_unknown_properties(self):
        self.httpretty_enable()
        archive_id = u('f6e7ee58-d6cf-4a59-896b-6d56b158ec71')
        httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/partner/{0}/archive/{1}').format(self.api_key, archive_id),
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
                                          "notarealproperty" : "not a real value"
                                        }""")),
                               status=200,
                               content_type=u('application/json'))

        archive = self.opentok.get_archive(archive_id)

        expect(archive).to.be.an(Archive)
        self.httpretty_disable()
