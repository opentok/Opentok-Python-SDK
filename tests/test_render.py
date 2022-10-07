import unittest
import textwrap
import httpretty
import json
import requests
from sure import expect

from six import u, PY2, PY3
from expects import *
from opentok import Client, Render, RenderList, __version__
from .validate_jwt import validate_jwt_header


class OpenTokRenderTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.opentok = Client(self.api_key, self.api_secret)
        self.session_id = u("2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4")
        self.token = u("1234-5678-9012")
        self.render_id = u("80abaf0d-25a3-4efc-968f-6268d620668d")

    @httpretty.activate
    def test_start_render(self):
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/v2/project/{0}/render").format(self.api_key),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "id": "1248e7070b81464c9789f46ad10e7764",
                            "sessionId": "2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4",
                            "projectId": "e2343f23456g34709d2443a234",
                            "createdAt": 1437676551000,
                            "updatedAt": 1437676551000,
                            "url": "https://webapp.customer.com",
                            "resolution": "1280x720",
                            "status": "started",
                            "streamId": "e32445b743678c98230f238" 
                        }
                    """
                )
            ),
            status=202,
            content_type=u("application/json"),
        )

        url = "https://webapp.customer.com"

        render = self.opentok.start_render(self.session_id, self.token, url)
        
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

        expect(body).to(have_key(u("token")))
        expect(render).to(be_a(Render))
        expect(render).to(
            have_property(u("id"), u("1248e7070b81464c9789f46ad10e7764"))
        )
        expect(render).to(
            have_property(u("sessionId"), u("2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4"))
        )
        expect(render).to(have_property(u("projectId"), u("e2343f23456g34709d2443a234")))
        expect(render).to(have_property(u("createdAt"), 1437676551000))
        expect(render).to(have_property(u("updatedAt"), 1437676551000))
        expect(render).to(have_property(u("resolution"), u("1280x720")))
        expect(render).to(have_property(u("status"), u("started")))
        expect(render).to(have_property(u("streamId"), u("e32445b743678c98230f238")))
    

    @httpretty.activate
    def test_get_render_status(self):
        httpretty.register_uri(
            httpretty.GET,
            u("https://api.opentok.com/v2/project/{0}/render/{1}").format(self.api_key, self.render_id),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "id": "80abaf0d-25a3-4efc-968f-6268d620668d",
                            "sessionId": "2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4",
                            "projectId": "e2343f23456g34709d2443a234",
                            "createdAt": 1437676551000,
                            "updatedAt": 1437676551000,
                            "url": "https://webapp.customer.com",
                            "resolution": "1280x720",
                            "status": "failed",
                            "reason":"Could not load URL"
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        render = self.opentok.get_render(self.render_id)
        
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        
        )

        expect(render).to(be_a(Render))
        expect(render).to(
            have_property(u("id"), u("80abaf0d-25a3-4efc-968f-6268d620668d"))
        )
        expect(render).to(
            have_property(u("sessionId"), u("2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4"))
        )
        expect(render).to(have_property(u("projectId"), u("e2343f23456g34709d2443a234")))
        expect(render).to(have_property(u("createdAt"), 1437676551000))
        expect(render).to(have_property(u("updatedAt"), 1437676551000))
        expect(render).to(have_property(u("resolution"), u("1280x720")))
        expect(render).to(have_property(u("status"), u("failed")))
        expect(render).to(have_property(u("reason"), u("Could not load URL")))

    @httpretty.activate
    def test_stop_render(self):
        httpretty.register_uri(
            httpretty.DELETE,
            u("https://api.opentok.com/v2/project/{0}/render/{1}").format(self.api_key, self.render_id),
            body="",
            status=200,
        )

        response = self.opentok.stop_render(self.render_id)
        
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )

        assert isinstance(response, requests.Response)
        assert response.status_code == 200

    @httpretty.activate
    def test_list_renders(self):
        httpretty.register_uri(
            httpretty.GET,
            u("https://api.opentok.com/v2/project/{0}/render").format(self.api_key),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "count":2,
                            "items":[
                                {
                                    "id":"80abaf0d-25a3-4efc-968f-6268d620668d",
                                    "sessionId":"1_MX4yNzA4NjYxMn5-MTU0NzA4MDUyMTEzNn5sOXU5ZnlWYXplRnZGblV4RUo3dXJpZk1-fg",
                                    "projectId":"27086612",
                                    "createdAt":1547080532099,
                                    "updatedAt":1547080532099,
                                    "url": "https://webapp.customer.com",
                                    "resolution": "1280x720",
                                    "status": "started",
                                    "streamId": "d2334b35690a92f78945"
                                },
                                {
                                    "id":"d95f6496-df6e-4f49-86d6-832e00303602",
                                    "sessionId":"2_MX4yNzA4NjYxMn5-MTU0NzA4MDUwMDc2MH5STWRiSE1jZjVoV3lBQU9nN2JuNElUV3V-fg",
                                    "projectId":"27086612",
                                    "createdAt":1547080511760,
                                    "updatedAt":1547080518965,
                                    "url": "https://webapp2.customer.com",
                                    "resolution": "1280x720",
                                    "status":"stopped",
                                    "streamId": "d2334b35690a92f78945",
                                    "reason":"Maximum duration exceeded"
                                }
                            ]
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        render_list = self.opentok.list_renders()
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )

        expect(render_list).to(be_a(RenderList))
        expect(render_list).to(have_property(u("count"), 2))
        expect(render_list).to(have_property(u("items")))
        expect(render_list.items[0]).to(have_property(u("sessionId"), u("1_MX4yNzA4NjYxMn5-MTU0NzA4MDUyMTEzNn5sOXU5ZnlWYXplRnZGblV4RUo3dXJpZk1-fg")))
        expect(render_list.items[0]).to(have_property(u("createdAt"), u(1547080532099)))
        expect(render_list.items[0]).to(have_property(u("url"), u("https://webapp.customer.com")))
        expect(render_list.items[0]).to(have_property(u("status"), u("started")))
        expect(render_list.items[0]).to(have_property(u("streamId"), u("d2334b35690a92f78945")))
        expect(render_list.items[1]).to(have_property(u("sessionId"), u("2_MX4yNzA4NjYxMn5-MTU0NzA4MDUwMDc2MH5STWRiSE1jZjVoV3lBQU9nN2JuNElUV3V-fg")))
        expect(render_list.items[1]).to(have_property(u("createdAt"), u(1547080511760)))
        expect(render_list.items[1]).to(have_property(u("updatedAt"), u(1547080518965)))
        expect(render_list.items[1]).to(have_property(u("url"), u("https://webapp2.customer.com")))
        expect(render_list.items[1]).to(have_property(u("status"), u("stopped")))
        expect(render_list.items[1]).to(have_property(u("streamId"), u("d2334b35690a92f78945")))
        expect(render_list.items[1]).to(have_property(u("reason"), u("Maximum duration exceeded")))
