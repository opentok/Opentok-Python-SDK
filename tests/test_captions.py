import unittest
import textwrap
import httpretty
import json
from sure import expect

from expects import *
from opentok import Client, __version__
from opentok.captions import Captions


class OpenTokCaptionsTest(unittest.TestCase):
    def setUp(self):
        self.api_key = "123456"
        self.api_secret = "1234567890abcdef1234567890abcdef1234567890"
        self.opentok = Client(self.api_key, self.api_secret)
        self.session_id = "2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4"
        self.token = "1234-5678-9012"
        self.response_body = textwrap.dedent(
            """ \
                {
                    "captionsId": "7c0680fc-6274-4de5-a66f-d0648e8d3ac2"
                }
            """
        )

    @httpretty.activate
    def test_start_captions(self):
        httpretty.register_uri(
            httpretty.POST,
            f"https://api.opentok.com/v2/project/{self.api_key}/captions",
            body=self.response_body,
            status=200,
            content_type="application/json",
        )

        captions = self.opentok.start_captions(
            self.session_id,
            self.token,
            language_code='en-GB',
            max_duration=10000,
            partial_captions=False,
            status_callback_url='https://example.com',
        )

        body = json.loads(httpretty.last_request().body.decode("utf-8"))
        expect(body).to(have_key("token"))

        expect(captions).to(be_a(Captions))
        expect(captions).to(
            have_property("captions_id", "7c0680fc-6274-4de5-a66f-d0648e8d3ac2")
        )

    @httpretty.activate
    def test_stop_captions(self):
        httpretty.register_uri(
            httpretty.POST,
            f"https://api.opentok.com/v2/project/{self.api_key}/captions/7c0680fc-6274-4de5-a66f-d0648e8d3ac2/stop",
            status=202,
            content_type="application/json",
        )

        self.opentok.stop_captions(captions_id='7c0680fc-6274-4de5-a66f-d0648e8d3ac2')

        request_url = httpretty.last_request().url
        assert (
            request_url
            == 'https://api.opentok.com/v2/project/123456/captions/7c0680fc-6274-4de5-a66f-d0648e8d3ac2/stop'
        )
