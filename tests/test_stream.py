import unittest
from six import u
from opentok import Client, Stream, StreamList, __version__, SetStreamClassError
import httpretty
import textwrap
from expects import *

from .validate_jwt import validate_jwt_header


class OpenTokStreamTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.opentok = Client(self.api_key, self.api_secret)
        self.session_id = u("SESSIONID")
        self.stream_id = u("8b732909-0a06-46a2-8ea8-074e64d43422")

    @httpretty.activate
    def test_get_stream(self):
        stream = Stream(
            {
                u("id"): u("8b732909-0a06-46a2-8ea8-074e64d43422"),
                u("videoType"): u("camera"),
                u("name"): u(""),
                u("layoutClassList"): ["full"],
            }
        )

        httpretty.register_uri(
            httpretty.GET,
            u("https://api.opentok.com/v2/project/{0}/session/{1}/stream/{2}").format(
                self.api_key, self.session_id, self.stream_id
            ),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "id": "8b732909-0a06-46a2-8ea8-074e64d43422",
                            "videoType": "camera",
                            "name": "",
                            "layoutClassList": ["full"]
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        stream_response = self.opentok.get_stream(self.session_id, self.stream_id)
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        expect(stream_response).to(be_an(Stream))
        expect(stream_response).to(have_property(u("id"), stream.id))
        expect(stream_response).to(have_property(u("videoType"), stream.videoType))
        expect(stream_response).to(have_property(u("name"), stream.name))
        expect(stream_response).to(
            have_property(u("layoutClassList"), stream.layoutClassList)
        )
        expect(list(stream_response.layoutClassList)).to(have_length(1))

    @httpretty.activate
    def test_get_stream_with_name(self):
        stream = Stream(
            {
                u("id"): u("8b732909-0a06-46a2-8ea8-074e64d43422"),
                u("videoType"): u("camera"),
                u("name"): u("stream name"),
                u("layoutClassList"): ["full"],
            }
        )

        httpretty.register_uri(
            httpretty.GET,
            u("https://api.opentok.com/v2/project/{0}/session/{1}/stream/{2}").format(
                self.api_key, self.session_id, self.stream_id
            ),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "id": "8b732909-0a06-46a2-8ea8-074e64d43422",
                            "videoType": "camera",
                            "name": "stream name",
                            "layoutClassList": ["full"]
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        stream_response = self.opentok.get_stream(self.session_id, self.stream_id)
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        expect(stream_response).to(be_an(Stream))
        expect(stream_response).to(have_property(u("id"), stream.id))
        expect(stream_response).to(have_property(u("videoType"), stream.videoType))
        expect(stream_response).to(have_property(u("name"), stream.name))
        expect(stream_response).to(
            have_property(u("layoutClassList"), stream.layoutClassList)
        )
        expect(list(stream_response.layoutClassList)).to(have_length(1))

    @httpretty.activate
    def test_get_stream_list(self):
        httpretty.register_uri(
            httpretty.GET,
            u("https://api.opentok.com/v2/project/{0}/session/{1}/stream").format(
                self.api_key, self.session_id
            ),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "count": 2,
                            "items": [
                                {
                                "id": "8b732909-0a06-46a2-8ea8-074e64d43422",
                                "videoType": "camera",
                                "name": "stream1",
                                "layoutClassList": ["full"]
                                },
                                {
                                "id": "7b732909-0a06-46a2-8ea8-074e64d43423",
                                "videoType": "camera",
                                "name": "stream2",
                                "layoutClassList": ["full"]
                                }
                            ]
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        stream_list = self.opentok.list_streams(self.session_id)
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        expect(stream_list).to(be_an(StreamList))
        expect(stream_list).to(have_property(u("count"), 2))
        expect(list(stream_list.items)).to(have_length(2))

    @httpretty.activate
    def test_set_stream_class_lists(self):
        """Test set stream class functionality"""
        payload = [
            {
                "id": "7b09ec3c-26f9-43d7-8197-f608f13d4fb6",
                "layoutClassList": ["focus"],
            },
            {"id": "567bc941-6ea0-4c69-97fc-70a740b68976", "layoutClassList": ["top"]},
            {
                "id": "307dc941-0450-4c09-975c-705740d08970",
                "layoutClassList": ["bottom"],
            },
        ]

        httpretty.register_uri(
            httpretty.PUT,
            u("https://api.opentok.com/v2/project/{0}/session/{1}/stream").format(
                self.api_key, self.session_id
            ),
            status=200,
            content_type=u("application/json"),
        )

        self.opentok.set_stream_class_lists(self.session_id, payload)

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )

    @httpretty.activate
    def test_set_stream_class_lists_throws_exception(self):
        """Test invalid request in set stream class list"""

        # invalid payload
        payload = [{"id": "7b09ec3c-26f9-43d7-8197-f608f13d4fb6"}]

        httpretty.register_uri(
            httpretty.PUT,
            u("https://api.opentok.com/v2/project/{0}/session/{1}/stream").format(
                self.api_key, self.session_id
            ),
            status=400,
            content_type=u("application/json"),
        )

        self.assertRaises(
            SetStreamClassError,
            self.opentok.set_stream_class_lists,
            self.session_id,
            payload,
        )
