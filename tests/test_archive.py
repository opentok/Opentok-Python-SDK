import unittest
from six import u, PY2, PY3
from expects import *
import httpretty
from sure import expect
import textwrap
import datetime
import pytz
from .validate_jwt import validate_jwt_header

from opentok import Client, Archive, __version__, OutputModes


class OpenTokArchiveTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.stream1 = "kjhk-09898-kjn"
        self.stream2 = "jnn-99kjk-88734r"
        self.opentok = Client(self.api_key, self.api_secret)

    @httpretty.activate
    def test_stop_archive(self):
        archive_id = u("ARCHIVEID")
        archive = Archive(
            self.opentok,
            {
                u("createdAt"): 1395183243556,
                u("duration"): 0,
                u("id"): archive_id,
                u("name"): u(""),
                u("partnerId"): 123456,
                u("reason"): u(""),
                u("sessionId"): u("SESSIONID"),
                u("size"): 0,
                u("status"): u("started"),
                u("hasAudio"): True,
                u("hasVideo"): True,
                u("outputMode"): OutputModes.composed.value,
                u("url"): None,
                u("maxBitrate"): 2000000,
            },
        )
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/v2/project/{0}/archive/{1}/stop").format(
                self.api_key, archive_id
            ),
            body=textwrap.dedent(
                u(
                    """\
                        {
                            "createdAt" : 1395183243556,
                            "duration" : 0,
                            "id" : "ARCHIVEID",
                            "name" : "",
                            "partnerId" : 123456,
                            "reason" : "",
                            "sessionId" : "SESSIONID",
                            "size" : 0,
                            "status" : "stopped",
                            "hasAudio": true,
                            "hasVideo": false,
                            "outputMode": "composed",
                            "url" : null,
                            "maxBitrate": 2000000
                        }
                    """
                )
            ),
            status=200,
            content_type=u("application/json"),
        )

        archive.stop()

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        expect(archive).to(be_an(Archive))
        expect(archive).to(have_property(u("id"), archive_id))
        expect(archive).to(have_property(u("name"), u("")))
        expect(archive).to(have_property(u("status"), u("stopped")))
        expect(archive).to(have_property(u("session_id"), u("SESSIONID")))
        expect(archive).to(have_property(u("partner_id"), 123456))
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395183243, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(
                1395183243, datetime.timezone.utc
            )
        expect(archive).to(have_property(u("created_at"), created_at))
        expect(archive).to(have_property(u("size"), 0))
        expect(archive).to(have_property(u("duration"), 0))
        expect(archive).to(have_property(u("has_audio"), True))
        expect(archive).to(have_property(u("has_video"), False))
        expect(archive).to(have_property(u("output_mode"), OutputModes.composed))
        expect(archive).to(have_property(u("url"), None))
        expect(archive).to(have_property(u("max_bitrate"), 2000000))

    @httpretty.activate
    def test_add_archive_stream(self):
        archive_id = u("ARCHIVEID")
        url = f"https://api.opentok.com/v2/project/{self.api_key}/archive/{archive_id}/streams"
        httpretty.register_uri(
            httpretty.PATCH, url, responses=[httpretty.Response(body=u(""), status=204)]
        )

        response = self.opentok.add_archive_stream(
            archive_id=archive_id, stream_id=self.stream1
        )
        assert response == None

    @httpretty.activate
    def test_remove_archive_stream(self):
        archive_id = u("ARCHIVEID")
        url = f"https://api.opentok.com/v2/project/{self.api_key}/archive/{archive_id}/streams"
        httpretty.register_uri(
            httpretty.PATCH, url, responses=[httpretty.Response(body=u(""), status=204)]
        )

        response = self.opentok.remove_archive_stream(
            archive_id=archive_id, stream_id=self.stream1
        )
        assert response == None

    @httpretty.activate
    def test_delete_archive(self):
        archive_id = u("ARCHIVEID")
        archive = Archive(
            self.opentok,
            {
                u("createdAt"): 1395183243556,
                u("duration"): 0,
                u("id"): archive_id,
                u("name"): u(""),
                u("partnerId"): 123456,
                u("reason"): u(""),
                u("sessionId"): u("SESSIONID"),
                u("size"): 0,
                u("status"): u("available"),
                u("hasAudio"): True,
                u("hasVideo"): True,
                u("outputMode"): OutputModes.composed.value,
                u("url"): None,
                u("maxBitrate"): 2000000,
            },
        )
        httpretty.register_uri(
            httpretty.DELETE,
            u("https://api.opentok.com/v2/project/{0}/archive/{1}").format(
                self.api_key, archive_id
            ),
            body=u(""),
            status=204,
        )

        archive.delete()

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        expect(httpretty.last_request().headers[u("content-type")]).to(
            equal(u("application/json"))
        )
        # TODO: test that the object is invalidated
