import unittest
import textwrap
import httpretty

from six import u
from expects import *
from opentok import OpenTok, Broadcast, __version__
from .validate_jwt import validate_jwt_header

class OpenTokBroadcastTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        self.opentok = OpenTok(self.api_key, self.api_secret)
        self.session_id = u('2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4')

    @httpretty.activate
    def test_start_broadcast(self):
        """
        Test start_broadcast() method
        """
        httpretty.register_uri(
            httpretty.POST,
            u('https://api.opentok.com/v2/project/{0}/broadcast').format(self.api_key),
            body=textwrap.dedent(u("""\
                {
                    "id": "1748b7070a81464c9759c46ad10d3734",
                    "sessionId": "2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4",
                    "projectId": 100,
                    "createdAt": 1437676551000,
                    "updatedAt": 1437676551000,
                    "resolution": "640x480",
                    "status": "started",
                    "broadcastUrls": {
                        "hls" : "http://server/fakepath/playlist.m3u8",
                        "rtmp": {
                            "foo": {
                                "serverUrl": "rtmp://myfooserver/myfooapp",
                                "streamName": "myfoostream"
                            },
                            "bar": {
                                "serverUrl": "rtmp://mybarserver/mybarapp",
                                "streamName": "mybarstream"
                            }
                        }
                    }
                }""")),
            status=200,
            content_type=u('application/json')
        )

        options = {
            'layout': {
                'type': 'custom',
                'stylesheet': 'the layout stylesheet (only used with type == custom)'
            },
            'maxDuration': 5400,
            'outputs': {
                'hls': {},
                'rtmp': [{
                    'id': 'foo',
                    'serverUrl': 'rtmp://myfooserver/myfooapp',
                    'streamName': 'myfoostream'
                }, {
                    'id': 'bar',
                    'serverUrl': 'rtmp://mybarserver/mybarapp',
                    'streamName': 'mybarstream'
                }]
            },
            'resolution': '640x480'
        }

        broadcast = self.opentok.start_broadcast(self.session_id, options)
        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(
            u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        expect(broadcast).to(be_an(Broadcast))
        expect(broadcast).to(have_property(u('id'), u('1748b7070a81464c9759c46ad10d3734')))
        expect(broadcast).to(have_property(u('sessionId'), u('2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4')))
        expect(broadcast).to(have_property(u('projectId'), 100))
        expect(broadcast).to(have_property(u('createdAt'), 1437676551000))
        expect(broadcast).to(have_property(u('updatedAt'), 1437676551000))
        expect(broadcast).to(have_property(u('resolution'), u('640x480')))
        expect(broadcast).to(have_property(u('status'), u('started')))
        expect(list(broadcast.broadcastUrls)).to(have_length(2))
        expect(list(broadcast.broadcastUrls['rtmp'])).to(have_length(2))

    @httpretty.activate
    def test_start_broadcast_only_one_rtmp(self):
        """
        Test start_broadcast() method with only one rtmp
        """
        httpretty.register_uri(
            httpretty.POST,
            u('https://api.opentok.com/v2/project/{0}/broadcast').format(self.api_key),
            body=textwrap.dedent(u("""\
                {
                    "id": "1748b7070a81464c9759c46ad10d3734",
                    "sessionId": "2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4",
                    "projectId": 100,
                    "createdAt": 1437676551000,
                    "updatedAt": 1437676551000,
                    "resolution": "640x480",
                    "status": "started",
                    "broadcastUrls": {
                        "hls" : "http://server/fakepath/playlist.m3u8",
                        "rtmp": {
                            "foo": {
                                "serverUrl": "rtmp://myfooserver/myfooapp",
                                "streamName": "myfoostream"
                            },
                            "bar": {
                                "serverUrl": "rtmp://mybarserver/mybarapp",
                                "streamName": "mybarstream"
                            }
                        }
                    }
                }""")),
            status=200,
            content_type=u('application/json')
        )

        options = {
            'sessionId': '2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ',
            'layout': {
                'type': 'custom',
                'stylesheet': 'the layout stylesheet (only used with type == custom)'
            },
            'maxDuration': 5400,
            'outputs': {
                'rtmp': {
                    'id': 'my-id',
                    'serverUrl': 'rtmp://myserver/myapp',
                    'streamName': 'my-stream-name'
                }
            },
            'resolution': '640x480'
        }

        broadcast = self.opentok.start_broadcast(self.session_id, options)
        validate_jwt_header(self, httpretty.last_request().headers[u('x-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to(contain(
            u('OpenTok-Python-SDK/')+__version__))
        expect(httpretty.last_request().headers[u('content-type')]).to(equal(u('application/json')))
        expect(broadcast).to(be_an(Broadcast))
        expect(broadcast).to(have_property(u('id'), u('1748b7070a81464c9759c46ad10d3734')))
        expect(broadcast).to(have_property(u('sessionId'), u('2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4')))
        expect(broadcast).to(have_property(u('projectId'), 100))
        expect(broadcast).to(have_property(u('createdAt'), 1437676551000))
        expect(broadcast).to(have_property(u('updatedAt'), 1437676551000))
        expect(broadcast).to(have_property(u('resolution'), u('640x480')))
        expect(broadcast).to(have_property(u('status'), u('started')))
        expect(list(broadcast.broadcastUrls)).to(have_length(2))
        expect(list(broadcast.broadcastUrls['rtmp'])).to(have_length(2))
