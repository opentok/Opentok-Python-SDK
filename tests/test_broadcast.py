import unittest
import textwrap
import httpretty

from six import u
from expects import *
from opentok import Client, Broadcast, __version__, BroadcastError
from .validate_jwt import validate_jwt_header


class OpenTokBroadcastTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.opentok = Client(self.api_key, self.api_secret)
        self.session_id = u("2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4")

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
        expect(list(broadcast.broadcastUrls)).to(have_length(2))
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
        expect(list(broadcast.broadcastUrls)).to(have_length(2))
        expect(list(broadcast.broadcastUrls["rtmp"])).to(have_length(2))

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
                                "hls" : "http://server/fakepath/playlist.m3u8",
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
        expect(list(broadcast.broadcastUrls)).to(have_length(2))
        expect(list(broadcast.broadcastUrls["rtmp"])).to(have_length(2))

    @httpretty.activate
    def test_set_broadcast_layout(self):
        """ Test set_broadcast_layout() functionality """
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
    def test_set_custom_broadcast_layout(self):
        """ Test set a custom broadcast layout specifying the 'stylesheet' parameter """
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
        """ Test invalid request in set broadcast layout """
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
