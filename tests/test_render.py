from lib2to3.pgen2 import token
import unittest
import textwrap
import httpretty
import json
from sure import expect

from six import u, PY2, PY3
from expects import *
from opentok import Client, Render, __version__
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
    