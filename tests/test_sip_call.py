import unittest
import textwrap
import httpretty

from six import u
from expects import *
from opentok import Client, SipCall, __version__

from .validate_jwt import validate_jwt_header


class OpenTokSipCallTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.opentok = Client(self.api_key, self.api_secret)

        self.session_id = u("SESSIONID")
        self.token = u("TOKEN")
        self.sip_uri = u("sip:user@sip.partner.com;transport=tls")

    @httpretty.activate
    def test_sip_call_with_required_parameters(self):
        """
        Test dial() method using just the required parameters: session_id, token, sip_uri
        """
        sip_call = SipCall(
            {
                u("id"): u("b0a5a8c7-dc38-459f-a48d-a7f2008da853"),
                u("connectionId"): u("e9f8c166-6c67-440d-994a-04fb6dfed007"),
                u("streamId"): u("482bce73-f882-40fd-8ca5-cb74ff416036"),
            }
        )

        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/v2/project/{0}/dial").format(self.api_key),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "id": "b0a5a8c7-dc38-459f-a48d-a7f2008da853",
                            "connectionId": "e9f8c166-6c67-440d-994a-04fb6dfed007",
                            "streamId": "482bce73-f882-40fd-8ca5-cb74ff416036"
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        sip_call_response = self.opentok.dial(self.session_id, self.token, self.sip_uri)
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        expect(sip_call_response).to(be_an(SipCall))
        expect(sip_call_response).to(have_property(u("id"), sip_call.id))
        expect(sip_call_response).to(
            have_property(u("connectionId"), sip_call.connectionId)
        )
        expect(sip_call_response).to(have_property(u("streamId"), sip_call.streamId))

    @httpretty.activate
    def test_sip_call_with_aditional_options(self):
        """
        Test dial() method with aditional options
        """
        sip_call = SipCall(
            {
                u("id"): u("b0a5a8c7-dc38-459f-a48d-a7f2008da853"),
                u("connectionId"): u("e9f8c166-6c67-440d-994a-04fb6dfed007"),
                u("streamId"): u("482bce73-f882-40fd-8ca5-cb74ff416036"),
            }
        )

        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/v2/project/{0}/dial").format(self.api_key),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "id": "b0a5a8c7-dc38-459f-a48d-a7f2008da853",
                            "connectionId": "e9f8c166-6c67-440d-994a-04fb6dfed007",
                            "streamId": "482bce73-f882-40fd-8ca5-cb74ff416036"
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        # aditional options to establish the sip call
        options = {
            "from": "from@example.com",
            "headers": {"headerKey": "headerValue"},
            "auth": {"username": "username", "password": "password"},
            "secure": True,
            "observeForceMute": True,
            "video": True,
            "streams": ["stream-id-1", "stream-id-2"],
        }

        sip_call_response = self.opentok.dial(
            self.session_id, self.token, self.sip_uri, options
        )
        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        expect(sip_call_response).to(be_an(SipCall))
        expect(sip_call_response).to(have_property(u("id"), sip_call.id))
        expect(sip_call_response).to(
            have_property(u("connectionId"), sip_call.connectionId)
        )
        expect(sip_call_response).to(have_property(u("streamId"), sip_call.streamId))
        assert (
            b'"streams": ["stream-id-1", "stream-id-2"]}' in httpretty.last_request().body
        )
