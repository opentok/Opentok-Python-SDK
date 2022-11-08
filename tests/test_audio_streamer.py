import unittest
import textwrap
import httpretty
import json
from sure import expect

from six import u, PY2, PY3
from expects import *
from opentok import Client, WebhookAudioConnection, __version__
from opentok.exceptions import InvalidWebsocketOptionsError, InvalidMediaModeError
from .validate_jwt import validate_jwt_header


class OpenTokAudioStreamerLiteTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.opentok = Client(self.api_key, self.api_secret)
        self.session_id = u("2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4")
        self.token = u("1234-5678-9012")
        self.response_body = textwrap.dedent(
            u(
                """ \
                    {
                        "id": "b0a5a8c7-dc38-459f-a48d-a7f2008da853",
                        "connectionId": "e9f8c166-6c67-440d-994a-04fb6dfed007"
                    }
                """
            )
        )

    @httpretty.activate
    def test_stream_audio_to_websocket(self):
        httpretty.register_uri(
            httpretty.POST,
            u(f"https://api.opentok.com/v2/project/{self.api_key}/connect"),
            body=self.response_body,
            status=200,
            content_type=u("application/json"),
        )

        websocket_options = {
            "uri": "wss://service.com/ws-endpoint"
        }

        webhook_audio_connection = self.opentok.stream_audio_to_websocket(self.session_id, self.token, websocket_options)
                
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
        expect(webhook_audio_connection).to(be_a(WebhookAudioConnection))
        expect(webhook_audio_connection).to(
            have_property(u("id"), u("b0a5a8c7-dc38-459f-a48d-a7f2008da853"))
        )
        expect(webhook_audio_connection).to(
            have_property(u("connectionId"), u("e9f8c166-6c67-440d-994a-04fb6dfed007"))
        )

    @httpretty.activate
    def test_stream_audio_to_websocket_custom_options(self):
        httpretty.register_uri(
            httpretty.POST,
            u(f"https://api.opentok.com/v2/project/{self.api_key}/connect"),
            body=self.response_body,
            status=200,
            content_type=u("application/json"),
        )

        websocket_options = {
            "uri": "wss://service.com/ws-endpoint",
            "streams": ["stream-id-1", "stream-id-2"],
            "headers": {
                "websocketHeader": "Sent via Audio Streamer API"
            }
        }

        webhook_audio_connection = self.opentok.stream_audio_to_websocket(self.session_id, self.token, websocket_options)
                
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
        expect(webhook_audio_connection).to(be_a(WebhookAudioConnection))
        expect(webhook_audio_connection).to(
            have_property(u("id"), u("b0a5a8c7-dc38-459f-a48d-a7f2008da853"))
        )
        expect(webhook_audio_connection).to(
            have_property(u("connectionId"), u("e9f8c166-6c67-440d-994a-04fb6dfed007"))
        )

    @httpretty.activate
    def test_stream_audio_to_websocket_media_mode_error(self):
        httpretty.register_uri(
            httpretty.POST,
            u(f"https://api.opentok.com/v2/project/{self.api_key}/connect"),
            body={},
            status=409,
            content_type=u("application/json"),
        )

        websocket_options = {
            "uri": "wss://service.com/ws-endpoint"
        }

        session_id = "session-where-mediaMode=relayed-was-selected"

        with self.assertRaises(InvalidMediaModeError) as context:
            self.opentok.stream_audio_to_websocket(session_id, self.token, websocket_options)
        self.assertTrue("Only routed sessions are allowed to initiate Audio Streamer WebSocket connections." in str(context.exception))
                
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )

    def test_stream_audio_to_websocket_invalid_options_type_error(self):
        websocket_options = "wss://service.com/ws-endpoint"
        with self.assertRaises(InvalidWebsocketOptionsError) as context:
            self.opentok.stream_audio_to_websocket(self.session_id, self.token, websocket_options)
        self.assertTrue("Must pass websocket options as a dictionary." in str(context.exception))
    
    def test_stream_audio_to_websocket_missing_uri_error(self):
        websocket_options = {}
        with self.assertRaises(InvalidWebsocketOptionsError) as context:
            self.opentok.stream_audio_to_websocket(self.session_id, self.token, websocket_options)
        self.assertTrue("Provide a webhook URI." in str(context.exception))
