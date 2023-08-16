import unittest
import textwrap
import httpretty
import json
import requests
from sure import expect

from six import u, PY2, PY3
from expects import *
from opentok import Client, Broadcast, __version__, BroadcastError
from opentok.broadcast import BroadcastStreamModes
from opentok.exceptions import BroadcastHLSOptionsError
from .validate_jwt import validate_jwt_header


class OpenTokBroadcastTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.opentok = Client(self.api_key, self.api_secret)
        self.session_id = u("2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4")
        self.stream1 = "kjhk-09898-kjn"
        self.stream2 = "jnn-99kjk-88734r"

    @httpretty.activate
    def test_start_broadcast(self):
        """
        Test start_broadcast() method
        """
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/v2/project/{0}/broadcast").format(self.api_key),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "id": "1748b7070a81464c9759c46ad10d3734",
                            "sessionId": "2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4",
                            "projectId": 100,
                            "createdAt": 1437676551000,
                            "updatedAt": 1437676551000,
                            "resolution": "640x480",
                            "status": "started",
                            "hasAudio": true,
                            "hasVideo": true,
                            "maxBitrate": 1000000,
                            "maxDuration": 5400,
                            "broadcastUrls": {
                                "hls" : "http://server/fakepath/playlist.m3u8",
                                "hlsStatus": "ready",
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
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        options = {
            "layout": {
                "type": "custom",
                "stylesheet": "the layout stylesheet (only used with type == custom)",
            },
            "maxDuration": 5400,
            "maxBitrate": 1000000,
            "outputs": {
                "hls": {},
                "rtmp": [
                    {
                        "id": "foo",
                        "serverUrl": "rtmp://myfooserver/myfooapp",
                        "streamName": "myfoostream",
                    },
                    {
                        "id": "bar",
                        "serverUrl": "rtmp://mybarserver/mybarapp",
                        "streamName": "mybarstream",
                    },
                ],
            },
            "resolution": "640x480",
        }

        broadcast = self.opentok.start_broadcast(self.session_id, options)
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode("utf-8"))

        expect(body).to(have_key(u("layout")))
        expect(broadcast).to(be_an(Broadcast))
        expect(broadcast).to(
            have_property(u("id"), u("1748b7070a81464c9759c46ad10d3734"))
        )
        expect(broadcast).to(
            have_property(u("sessionId"), u("2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4"))
        )
        expect(broadcast).to(have_property(u("projectId"), 100))
        expect(broadcast).to(have_property(u("createdAt"), 1437676551000))
        expect(broadcast).to(have_property(u("updatedAt"), 1437676551000))
        expect(broadcast).to(have_property(u("resolution"), u("640x480")))
        expect(broadcast).to(have_property(u("status"), u("started")))
        expect(broadcast).to(have_property("maxDuration", 5400))
        expect(broadcast).to(have_property("hasAudio", True))
        expect(broadcast).to(have_property("hasVideo", True))
        expect(broadcast).to(have_property("maxBitrate", 1000000))
        expect(broadcast.broadcastUrls["hlsStatus"]).to(equal("ready"))
        expect(list(broadcast.broadcastUrls)).to(have_length(3))
        expect(list(broadcast.broadcastUrls["rtmp"])).to(have_length(2))

    @httpretty.activate
    def test_start_broadcast_only_one_rtmp(self):
        """
        Test start_broadcast() method with only one rtmp
        """
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/v2/project/{0}/broadcast").format(self.api_key),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "id": "1748b7070a81464c9759c46ad10d3734",
                            "sessionId": "2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4",
                            "projectId": 100,
                            "createdAt": 1437676551000,
                            "updatedAt": 1437676551000,
                            "resolution": "640x480",
                            "status": "started",
                            "hasAudio": true,
                            "hasVideo": true,
                            "maxBitrate": 1000000,
                            "maxDuration": 5400,
                            "broadcastUrls": {
                                "hls": "http://server/fakepath/playlist.m3u8",
                                "hlsStatus": "connecting",
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
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        options = {
            "sessionId": "2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ",
            "layout": {
                "type": "custom",
                "stylesheet": "the layout stylesheet (only used with type == custom)",
            },
            "maxDuration": 5400,
            "outputs": {
                "rtmp": {
                    "id": "my-id",
                    "serverUrl": "rtmp://myserver/myapp",
                    "streamName": "my-stream-name",
                }
            },
            "resolution": "640x480",
        }

        broadcast = self.opentok.start_broadcast(self.session_id, options)
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        expect(broadcast).to(be_an(Broadcast))
        expect(broadcast).to(
            have_property(u("id"), u("1748b7070a81464c9759c46ad10d3734"))
        )
        expect(broadcast).to(
            have_property(u("sessionId"), u("2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4"))
        )
        expect(broadcast).to(have_property(u("projectId"), 100))
        expect(broadcast).to(have_property(u("createdAt"), 1437676551000))
        expect(broadcast).to(have_property(u("updatedAt"), 1437676551000))
        expect(broadcast).to(have_property(u("resolution"), u("640x480")))
        expect(broadcast).to(have_property(u("status"), u("started")))
        expect(broadcast.broadcastUrls["hlsStatus"]).to(equal("connecting"))
        expect(list(broadcast.broadcastUrls)).to(have_length(3))
        expect(list(broadcast.broadcastUrls["rtmp"])).to(have_length(2))

    @httpretty.activate
    def test_start_broadcast_with_screenshare_type(self):
        """
        Test start_broadcast() method
        """
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/v2/project/{0}/broadcast").format(self.api_key),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "id": "1748b7070a81464c9759c46ad10d3734",
                            "sessionId": "2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4",
                            "projectId": 100,
                            "createdAt": 1437676551000,
                            "updatedAt": 1437676551000,
                            "resolution": "640x480",
                            "status": "started",
                            "hasAudio": true,
                            "hasVideo": true,
                            "maxBitrate": 1000000,
                            "maxDuration": 5400,
                            "broadcastUrls": {
                                "hls" : "http://server/fakepath/playlist.m3u8",
                                "hlsStatus": "ready",
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
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        options = {
            "layout": {"screenshareType": "verticalPresentation"},
            "maxDuration": 5400,
            "outputs": {
                "hls": {},
                "rtmp": [
                    {
                        "id": "foo",
                        "serverUrl": "rtmp://myfooserver/myfooapp",
                        "streamName": "myfoostream",
                    },
                    {
                        "id": "bar",
                        "serverUrl": "rtmp://mybarserver/mybarapp",
                        "streamName": "mybarstream",
                    },
                ],
            },
            "resolution": "640x480",
        }

        broadcast = self.opentok.start_broadcast(self.session_id, options)
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode("utf-8"))

        expect(body).to(have_key("sessionId", self.session_id))
        expect(body).to(have_key("layout"))
        expect(body["layout"]).to(have_key("screenshareType"))
        expect(body["layout"]["screenshareType"]).to(equal("verticalPresentation"))
        expect(broadcast).to(be_an(Broadcast))
        expect(broadcast).to(
            have_property(u("id"), u("1748b7070a81464c9759c46ad10d3734"))
        )
        expect(broadcast).to(
            have_property(u("sessionId"), u("2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4"))
        )
        expect(broadcast).to(have_property(u("projectId"), 100))
        expect(broadcast).to(have_property(u("createdAt"), 1437676551000))
        expect(broadcast).to(have_property(u("updatedAt"), 1437676551000))
        expect(broadcast).to(have_property(u("resolution"), u("640x480")))
        expect(broadcast).to(have_property(u("status"), u("started")))
        expect(broadcast.broadcastUrls["hlsStatus"]).to(equal("ready"))
        expect(list(broadcast.broadcastUrls)).to(have_length(3))
        expect(list(broadcast.broadcastUrls["rtmp"])).to(have_length(2))

    @httpretty.activate
    def test_start_broadcast_audio_only(self):
        """
        Test start_broadcast() method
        """
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/v2/project/{0}/broadcast").format(self.api_key),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "id": "1748b7070a81464c9759c46ad10d3734",
                            "sessionId": "2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4",
                            "projectId": 100,
                            "createdAt": 1437676551000,
                            "updatedAt": 1437676551000,
                            "resolution": "640x480",
                            "status": "started",
                            "hasAudio": true,
                            "hasVideo": false,
                            "maxBitrate": 1000000,
                            "maxDuration": 5400,
                            "hasAudio": true,
                            "hasVideo": false,
                            "broadcastUrls": {
                                "hls": "http://server/fakepath/playlist.m3u8",
                                "hlsStatus": "live",
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
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        options = {
            "layout": {
                "type": "custom",
                "stylesheet": "the layout stylesheet (only used with type == custom)",
            },
            "maxDuration": 5400,
            "hasAudio": True,
            "hasVideo": False,
            "outputs": {
                "hls": {},
                "rtmp": [
                    {
                        "id": "foo",
                        "serverUrl": "rtmp://myfooserver/myfooapp",
                        "streamName": "myfoostream",
                    },
                    {
                        "id": "bar",
                        "serverUrl": "rtmp://mybarserver/mybarapp",
                        "streamName": "mybarstream",
                    },
                ],
            },
            "resolution": "640x480",
        }

        broadcast = self.opentok.start_broadcast(self.session_id, options)
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode("utf-8"))

        expect(body).to(have_key(u("layout")))
        expect(broadcast).to(be_an(Broadcast))
        expect(broadcast).to(
            have_property(u("id"), u("1748b7070a81464c9759c46ad10d3734"))
        )
        expect(broadcast).to(
            have_property(u("sessionId"), u("2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4"))
        )
        expect(broadcast).to(have_property(u("projectId"), 100))
        expect(broadcast).to(have_property(u("createdAt"), 1437676551000))
        expect(broadcast).to(have_property(u("updatedAt"), 1437676551000))
        expect(broadcast).to(have_property(u("hasAudio"), True))
        expect(broadcast).to(have_property(u("hasVideo"), False))
        expect(broadcast).to(have_property(u("resolution"), u("640x480")))
        expect(broadcast).to(have_property(u("status"), u("started")))
        expect(broadcast.broadcastUrls["hlsStatus"]).to(equal("live"))
        expect(list(broadcast.broadcastUrls)).to(have_length(3))
        expect(list(broadcast.broadcastUrls["rtmp"])).to(have_length(2))

    @httpretty.activate
    def test_start_broadcast_video_only(self):
        """
        Test start_broadcast() method
        """
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/v2/project/{0}/broadcast").format(self.api_key),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "id": "1748b7070a81464c9759c46ad10d3734",
                            "sessionId": "2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4",
                            "projectId": 100,
                            "createdAt": 1437676551000,
                            "updatedAt": 1437676551000,
                            "resolution": "640x480",
                            "status": "started",
                            "hasAudio": false,
                            "hasVideo": true,
                            "maxBitrate": 1000000,
                            "maxDuration": 5400,
                            "hasAudio": false,
                            "hasVideo": true,
                            "broadcastUrls": {
                                "hls": "http://server/fakepath/playlist.m3u8",
                                "hlsStatus": "ready",
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
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        options = {
            "layout": {
                "type": "custom",
                "stylesheet": "the layout stylesheet (only used with type == custom)",
            },
            "maxDuration": 5400,
            "hasAudio": False,
            "hasVideo": True,
            "outputs": {
                "hls": {},
                "rtmp": [
                    {
                        "id": "foo",
                        "serverUrl": "rtmp://myfooserver/myfooapp",
                        "streamName": "myfoostream",
                    },
                    {
                        "id": "bar",
                        "serverUrl": "rtmp://mybarserver/mybarapp",
                        "streamName": "mybarstream",
                    },
                ],
            },
            "resolution": "640x480",
        }

        broadcast = self.opentok.start_broadcast(self.session_id, options)
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        # non-deterministic json encoding. have to decode to test it properly
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode("utf-8"))

        expect(body).to(have_key(u("layout")))
        expect(broadcast).to(be_an(Broadcast))
        expect(broadcast).to(
            have_property(u("id"), u("1748b7070a81464c9759c46ad10d3734"))
        )
        expect(broadcast).to(
            have_property(u("sessionId"), u("2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4"))
        )
        expect(broadcast).to(have_property(u("projectId"), 100))
        expect(broadcast).to(have_property(u("createdAt"), 1437676551000))
        expect(broadcast).to(have_property(u("updatedAt"), 1437676551000))
        expect(broadcast).to(have_property(u("hasAudio"), False))
        expect(broadcast).to(have_property(u("hasVideo"), True))
        expect(broadcast).to(have_property(u("resolution"), u("640x480")))
        expect(broadcast).to(have_property(u("status"), u("started")))
        expect(broadcast.broadcastUrls["hlsStatus"]).to(equal("ready"))
        expect(list(broadcast.broadcastUrls)).to(have_length(3))
        expect(list(broadcast.broadcastUrls["rtmp"])).to(have_length(2))

    @httpretty.activate
    def test_start_broadcast_with_streammode_auto(self):
        url = f"https://api.opentok.com/v2/project/{self.api_key}/broadcast"

        httpretty.register_uri(
            httpretty.POST,
            url,
            responses=[
                httpretty.Response(
                    body=json.dumps({"stream_mode": "auto"}),
                    content_type="application/json",
                    status=200,
                )
            ],
        )

        broadcast = self.opentok.start_broadcast(
            session_id=self.session_id, options={"outputs": {"hls": {}}}
        )
        broadcast.stream_mode.should.equal(BroadcastStreamModes.auto)

    @httpretty.activate
    def test_add_broadcast_stream(self):
        broadcast_id = "BROADCASTID"
        url = f"https://api.opentok.com/v2/project/{self.api_key}/broadcast/{broadcast_id}/streams"
        httpretty.register_uri(
            httpretty.PATCH, url, responses=[httpretty.Response(body=u(""), status=204)]
        )

        response = self.opentok.add_broadcast_stream(
            broadcast_id=broadcast_id, stream_id=self.stream1
        )
        assert response == None

    @httpretty.activate
    def test_remove_broadcast_stream(self):
        broadcast_id = "BROADCASTID"
        url = f"https://api.opentok.com/v2/project/{self.api_key}/broadcast/{broadcast_id}/streams"
        httpretty.register_uri(
            httpretty.PATCH, url, responses=[httpretty.Response(body=u(""), status=204)]
        )

        response = self.opentok.add_broadcast_stream(
            broadcast_id=broadcast_id, stream_id=self.stream1
        )
        assert response == None

    @httpretty.activate
    def test_update_broadcast_auto(self):
        broadcast_id = u("BROADCASTID")
        url = f"https://api.opentok.com/v2/project/{self.api_key}/broadcast/{broadcast_id}/streams"

        payload = {
            "hasAudio": True,
            "hasVideo": True,
            "addStream": [self.stream1, self.stream2],
        }

        httpretty.register_uri(
            httpretty.PATCH,
            url,
            responses=[
                httpretty.Response(
                    body=json.dumps(payload),
                    content_type="application/json",
                    status=200,
                )
            ],
        )

        response = requests.patch(url)

        response.status_code.should.equal(200)
        response.json().should.equal(
            {
                "hasAudio": True,
                "hasVideo": True,
                "addStream": [self.stream1, self.stream2],
            }
        )

        response.headers["Content-Type"].should.equal("application/json")

    @httpretty.activate
    def test_update_broadcast_manual(self):
        broadcast_id = u("BROADCASTID")
        url = f"https://api.opentok.com/v2/project/{self.api_key}/broadcast/{broadcast_id}/streams"

        payload = {"hasAudio": True, "hasVideo": True, "addStream": [self.stream1]}

        httpretty.register_uri(
            httpretty.PATCH,
            url,
            responses=[
                httpretty.Response(
                    body=json.dumps(payload),
                    content_type="application/json",
                    status=200,
                )
            ],
        )

        response = requests.patch(url)

        response.status_code.should.equal(200)
        response.json().should.equal(
            {"hasAudio": True, "hasVideo": True, "addStream": [self.stream1]}
        )

        response.headers["Content-Type"].should.equal("application/json")

    @httpretty.activate
    def test_stop_broadcast(self):
        """
        Test stop_broadcast() method
        """
        broadcast_id = u("1748b7070a81464c9759c46ad10d3734")

        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/v2/project/{0}/broadcast/{1}/stop").format(
                self.api_key, broadcast_id
            ),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "id": "1748b7070a81464c9759c46ad10d3734",
                            "sessionId": "2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4",
                            "projectId": 100,
                            "createdAt": 1437676551000,
                            "updatedAt": 1437676551000,
                            "resolution": "640x480",
                            "broadcastUrls": null
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        broadcast = self.opentok.stop_broadcast(broadcast_id)
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        expect(broadcast).to(be_an(Broadcast))
        expect(broadcast).to(
            have_property(u("id"), u("1748b7070a81464c9759c46ad10d3734"))
        )
        expect(broadcast).to(
            have_property(u("sessionId"), u("2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4"))
        )
        expect(broadcast).to(have_property(u("projectId"), 100))
        expect(broadcast).to(have_property(u("createdAt"), 1437676551000))
        expect(broadcast).to(have_property(u("updatedAt"), 1437676551000))
        expect(broadcast).to(have_property(u("resolution"), u("640x480")))

    @httpretty.activate
    def test_get_broadcast(self):
        """
        Test get_broadcast() method
        """
        broadcast_id = u("1748b707-0a81-464c-9759-c46ad10d3734")

        httpretty.register_uri(
            httpretty.GET,
            u("https://api.opentok.com/v2/project/{0}/broadcast/{1}").format(
                self.api_key, broadcast_id
            ),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "id": "1748b707-0a81-464c-9759-c46ad10d3734",
                            "sessionId": "2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4",
                            "projectId": 100,
                            "createdAt": 1437676551000,
                            "updatedAt": 1437676551000,
                            "resolution": "640x480",
                            "broadcastUrls": {
                                "hls": "http://server/fakepath/playlist.m3u8",
                                "hlsStatus": "live",
                                "rtmp": {
                                    "foo": {
                                        "serverUrl": "rtmp://myfooserver/myfooapp",
                                        "streamName": "myfoostream",
                                        "status": "live"
                                    },
                                    "bar": {
                                        "serverUrl": "rtmp://mybarserver/mybarapp",
                                        "streamName": "mybarstream",
                                        "status": "live"
                                    }
                                }
                            },
                            "status": "started"
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        broadcast = self.opentok.get_broadcast(broadcast_id)
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        expect(broadcast).to(be_an(Broadcast))
        expect(broadcast).to(have_property(u("id"), broadcast_id))
        expect(broadcast).to(
            have_property(u("sessionId"), u("2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4"))
        )
        expect(broadcast).to(have_property(u("projectId"), 100))
        expect(broadcast).to(have_property(u("createdAt"), 1437676551000))
        expect(broadcast).to(have_property(u("updatedAt"), 1437676551000))
        expect(broadcast).to(have_property(u("resolution"), u("640x480")))
        expect(broadcast).to(have_property(u("status"), u("started")))
        expect(broadcast.broadcastUrls["hlsStatus"]).to(equal("live"))
        expect(list(broadcast.broadcastUrls)).to(have_length(3))
        expect(list(broadcast.broadcastUrls["rtmp"])).to(have_length(2))

    @httpretty.activate
    def test_set_broadcast_layout(self):
        """Test set_broadcast_layout() functionality"""
        broadcast_id = u("1748b707-0a81-464c-9759-c46ad10d3734")

        httpretty.register_uri(
            httpretty.PUT,
            u("https://api.opentok.com/v2/project/{0}/broadcast/{1}/layout").format(
                self.api_key, broadcast_id
            ),
            status=200,
            content_type=u("application/json"),
        )

        self.opentok.set_broadcast_layout(broadcast_id, "horizontalPresentation")

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )

    @httpretty.activate
    def test_set_broadcast_layout_with_screenshare_type(self):
        """Test set_broadcast_layout() functionality"""
        broadcast_id = u("1748b707-0a81-464c-9759-c46ad10d3734")

        httpretty.register_uri(
            httpretty.PUT,
            u("https://api.opentok.com/v2/project/{0}/broadcast/{1}/layout").format(
                self.api_key, broadcast_id
            ),
            status=200,
            content_type=u("application/json"),
        )

        self.opentok.set_broadcast_layout(
            broadcast_id, "bestFit", screenshare_type="horizontalPresentation"
        )

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        if PY2:
            body = json.loads(httpretty.last_request().body)
        if PY3:
            body = json.loads(httpretty.last_request().body.decode("utf-8"))

        expect(body).to(have_key(u("type"), u("bestFit")))
        expect(body).to_not(have_key(u("stylesheet")))
        expect(body).to(have_key(u("screenshareType"), u("horizontalPresentation")))

    @httpretty.activate
    def test_set_custom_broadcast_layout(self):
        """Test set a custom broadcast layout specifying the 'stylesheet' parameter"""
        broadcast_id = u("1748b707-0a81-464c-9759-c46ad10d3734")

        httpretty.register_uri(
            httpretty.PUT,
            u("https://api.opentok.com/v2/project/{0}/broadcast/{1}/layout").format(
                self.api_key, broadcast_id
            ),
            status=200,
            content_type=u("application/json"),
        )

        self.opentok.set_broadcast_layout(
            broadcast_id,
            "custom",
            "stream.instructor {position: absolute; width: 100%;  height:50%;}",
        )

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )

    @httpretty.activate
    def test_set_broadcast_layout_throws_exception(self):
        """Test invalid request in set broadcast layout"""
        broadcast_id = u("1748b707-0a81-464c-9759-c46ad10d3734")

        httpretty.register_uri(
            httpretty.PUT,
            u("https://api.opentok.com/v2/project/{0}/broadcast/{1}/layout").format(
                self.api_key, broadcast_id
            ),
            status=400,
            content_type=u("application/json"),
        )

        self.assertRaises(
            BroadcastError,
            self.opentok.set_broadcast_layout,
            broadcast_id,
            "horizontalPresentation",
        )

    def test_broadcast_hls_mutually_exclusive_options_error(self):
        """
        Test invalid options in start_broadcast() method raises a BroadcastHLSOptionsError.
        """

        options = {
            "layout": {
                "type": "custom",
                "stylesheet": "the layout stylesheet (only used with type == custom)",
            },
            "maxDuration": 5400,
            "outputs": {
                "hls": {"lowLatency": True, "dvr": True},
                "rtmp": [
                    {
                        "id": "foo",
                        "serverUrl": "rtmp://myfooserver/myfooapp",
                        "streamName": "myfoostream",
                    },
                    {
                        "id": "bar",
                        "serverUrl": "rtmp://mybarserver/mybarapp",
                        "streamName": "mybarstream",
                    },
                ],
            },
            "resolution": "640x480",
        }

        with self.assertRaises(BroadcastHLSOptionsError):
            self.opentok.start_broadcast(self.session_id, options)
