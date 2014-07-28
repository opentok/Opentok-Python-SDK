import unittest
from six import u
from sure import expect
import httpretty
import textwrap
import os

from opentok import OpenTok, ArchiveList, OpenTokException

class OpenTokArchiveTest(unittest.TestCase):

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

        self.session_id = u('SESSIONID')
        self.archive_id = u('ARCHIVEID')

    def httpretty_enable(self):
        if self.mock:
            httpretty.enable()

    def httpretty_disable(self):
        if self.mock:
            httpretty.disable()

    def test_start_archive(self):
        self.httpretty_enable()

        if self.mock:
            httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/partner/{0}/archive').format(self.api_key),
                                   status=404,
                                   content_type=u('application/json'))
        expect(self.opentok.start_archive).when.called_with(self.session_id).to.throw(OpenTokException)
        expect(self.opentok.start_archive).when.called_with(self.session_id).to.throw('Session not found')
        self.httpretty_disable()

    def test_stop_archive(self):
        self.httpretty_enable()

        if self.mock:
            httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/v2/partner/{0}/archive/{1}/stop').format(self.api_key, self.archive_id),
                               status=404,
                               content_type=u('application/json'))

        expect(self.opentok.stop_archive).when.called_with(self.archive_id).to.throw(OpenTokException)
        expect(self.opentok.stop_archive).when.called_with(self.archive_id).to.throw('Archive not found')
        self.httpretty_disable()

    def test_delete_archive(self):
        self.httpretty_enable()

        if self.mock:
            httpretty.register_uri(httpretty.DELETE, u('https://api.opentok.com/v2/partner/{0}/archive/{1}').format(self.api_key, self.archive_id),
                               body=u(''),
                               status=404)

        expect(self.opentok.delete_archive).when.called_with(self.archive_id).to.throw(OpenTokException)
        expect(self.opentok.delete_archive).when.called_with(self.archive_id).to.throw('Archive not found')
        self.httpretty_disable()

    def test_get_archives(self):
        self.httpretty_enable()

        if self.mock:
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
        expect(archive_list).to.be.an(ArchiveList)
        expect(archive_list).to.have.property(u('count')).to.be.greater_than(1)
        assert expect(archive_list).to_not.have.length_of(0)
        self.httpretty_disable()

    def test_get_archives_with_count(self):
        self.httpretty_enable()

        if self.mock:
            httpretty.register_uri(httpretty.GET, u('https://api.opentok.com/v2/partner/{0}/archive').format(self.api_key),
                               body=textwrap.dedent(u("""\
                                       {
                                          "count" : 2,
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
        expect(archive_list).to.be.an(ArchiveList)
        expect(archive_list).to.have.property(u('count')).to.be.greater_than(1)
        assert expect(archive_list).to.have.length_of(2)
        self.httpretty_disable()

    def test_find_archives_with_offset_and_count(self):
        self.httpretty_enable()

        if self.mock:
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
        expect(archive_list).to.be.an(ArchiveList)
        expect(archive_list).to.have.property(u('count')).to.be.greater_than(5)
        expect(list(archive_list.items)).to.have.length_of(4)
        self.httpretty_disable()
