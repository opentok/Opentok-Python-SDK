import pytest
import unittest
from six import u, b
from six.moves.urllib.parse import parse_qs
from expects import *
import httpretty
from .validate_jwt import validate_jwt_header
import platform

from opentok import (
    Client,
    Session,
    MediaModes,
    ArchiveModes,
    OpenTokException,
    __version__,
)


class OpenTokSessionCreationTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u("123456")
        self.api_secret = u("1234567890abcdef1234567890abcdef1234567890")
        self.opentok = Client(self.api_key, self.api_secret)

    @httpretty.activate
    def test_create_default_session(self):
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/session/create"),
            body=u(
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'
            ),
            status=200,
            content_type=u("text/xml"),
        )

        session = self.opentok.create_session()

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            equal(
                u("OpenTok-Python-SDK/")
                + __version__
                + " python/"
                + platform.python_version()
            )
        )
        body = parse_qs(httpretty.last_request().body)
        expect(body).to(have_key(b("p2p.preference"), [b("enabled")]))
        expect(body).to(have_key(b("archiveMode"), [b("manual")]))
        expect(session).to(be_a(Session))
        expect(session).to(
            have_property(
                u("session_id"),
                u(
                    "1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg"
                ),
            )
        )
        expect(session).to(have_property(u("media_mode"), MediaModes.relayed))
        expect(session).to(have_property(u("location"), None))
        expect(session).to(have_property(u("e2ee"), False))

    @httpretty.activate
    def test_create_routed_session(self):
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/session/create"),
            body=u(
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'
            ),
            status=200,
            content_type=u("text/xml"),
        )

        session = self.opentok.create_session(media_mode=MediaModes.routed)

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        body = parse_qs(httpretty.last_request().body)
        expect(body).to(have_key(b("p2p.preference"), [b("disabled")]))
        expect(body).to(have_key(b("archiveMode"), [b("manual")]))
        expect(session).to(be_a(Session))
        expect(session).to(
            have_property(
                u("session_id"),
                u(
                    "1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg"
                ),
            )
        )
        expect(session).to(have_property(u("media_mode"), MediaModes.routed))
        expect(session).to(have_property(u("location"), None))
        expect(session).to(have_property(u("e2ee"), False))

    @httpretty.activate
    def test_failure_create_routed_session(self):
        # Session creation fails when server doesn't returns a XML
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/session/create"),
            body=u(
                '<html><head><meta charset="UTF-8"></head><body>Page not found</body></html>'
            ),
            status=200,
            content_type=u("text/xml"),
        )

        with pytest.raises(OpenTokException):
            self.opentok.create_session(media_mode=MediaModes.routed)

    @httpretty.activate
    def test_create_session_with_location_hint(self):
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/session/create"),
            body=u(
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'
            ),
            status=200,
            content_type=u("text/xml"),
        )

        session = self.opentok.create_session(location="12.34.56.78")

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        # ordering of keys is non-deterministic, must parse the body to see if it is correct
        body = parse_qs(httpretty.last_request().body)
        expect(body).to(have_key(b("location"), [b("12.34.56.78")]))
        expect(body).to(have_key(b("p2p.preference"), [b("enabled")]))
        expect(session).to(be_a(Session))
        expect(session).to(
            have_property(
                u("session_id"),
                u(
                    "1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg"
                ),
            )
        )
        expect(session).to(have_property(u("media_mode"), MediaModes.relayed))
        expect(session).to(have_property(u("location"), u("12.34.56.78")))
        expect(session).to(have_property(u("e2ee"), False))

    @httpretty.activate
    def test_create_routed_session_with_location_hint(self):
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/session/create"),
            body=u(
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'
            ),
            status=200,
            content_type=u("text/xml"),
        )

        session = self.opentok.create_session(
            location="12.34.56.78", media_mode=MediaModes.routed
        )

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        # ordering of keys is non-deterministic, must parse the body to see if it is correct
        body = parse_qs(httpretty.last_request().body)
        expect(body).to(have_key(b("location"), [b("12.34.56.78")]))
        expect(body).to(have_key(b("p2p.preference"), [b("disabled")]))
        expect(session).to(be_a(Session))
        expect(session).to(
            have_property(
                u("session_id"),
                u(
                    "1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg"
                ),
            )
        )
        expect(session).to(have_property(u("media_mode"), MediaModes.routed))
        expect(session).to(have_property(u("location"), u("12.34.56.78")))
        expect(session).to(have_property(u("e2ee"), False))

    @httpretty.activate
    def test_create_manual_archive_mode_session(self):
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/session/create"),
            body=u(
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'
            ),
            status=200,
            content_type=u("text/xml"),
        )

        session = self.opentok.create_session(
            media_mode=MediaModes.routed, archive_mode=ArchiveModes.manual
        )

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        body = parse_qs(httpretty.last_request().body)
        expect(body).to(have_key(b("p2p.preference"), [b("disabled")]))
        expect(body).to(have_key(b("archiveMode"), [b("manual")]))
        expect(session).to(be_a(Session))
        expect(session).to(
            have_property(
                u("session_id"),
                u(
                    "1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg"
                ),
            )
        )
        expect(session).to(have_property(u("media_mode"), MediaModes.routed))
        expect(session).to(have_property(u("archive_mode"), ArchiveModes.manual))
        expect(session).to(have_property(u("e2ee"), False))

    @httpretty.activate
    def test_create_always_archive_mode_session(self):
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/session/create"),
            body=u(
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'
            ),
            status=200,
            content_type=u("text/xml"),
        )

        session = self.opentok.create_session(
            media_mode=MediaModes.routed,
            archive_mode=ArchiveModes.always,
            archive_name="test_opentok_archive",
            archive_resolution="1920x1080",
        )

        validate_jwt_header(self, httpretty.last_request().headers[u("x-opentok-auth")])
        expect(httpretty.last_request().headers[u("user-agent")]).to(
            contain(u("OpenTok-Python-SDK/") + __version__)
        )
        body = parse_qs(httpretty.last_request().body)
        expect(body).to(have_key(b("p2p.preference"), [b("disabled")]))
        expect(body).to(have_key(b("archiveMode"), [b("always")]))
        expect(body).to(have_key(b("archiveName"), [b("test_opentok_archive")]))
        expect(body).to(have_key(b("archiveResolution"), [b("1920x1080")]))
        expect(session).to(be_a(Session))
        expect(session).to(
            have_property(
                u("session_id"),
                u(
                    "1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg"
                ),
            )
        )
        expect(session).to(have_property(u("media_mode"), MediaModes.routed))
        expect(session).to(have_property(u("archive_mode"), ArchiveModes.always))
        expect(session).to(have_property(u("e2ee"), False))

    def test_complains_about_always_archive_mode_and_relayed_session(self):
        with pytest.raises(OpenTokException):
            self.opentok.create_session(
                media_mode=MediaModes.relayed, archive_mode=ArchiveModes.always
            )

    def test_auto_archive_errors(self):
        with pytest.raises(OpenTokException):
            self.opentok.create_session(
                media_mode=MediaModes.routed,
                archive_mode=ArchiveModes.manual,
                archive_name="my_archive",
            )

        with pytest.raises(OpenTokException):
            self.opentok.create_session(
                media_mode=MediaModes.routed,
                archive_mode=ArchiveModes.manual,
                archive_resolution="640x480",
            )

        with pytest.raises(OpenTokException):
            self.opentok.create_session(
                media_mode=MediaModes.routed,
                archive_mode=ArchiveModes.always,
                archive_name="my_incredibly_long_name_that_is_definitely_going_to_be_over_the_80_character_limit_we_currently_impose",
            )

        with pytest.raises(OpenTokException):
            self.opentok.create_session(
                media_mode=MediaModes.routed,
                archive_mode=ArchiveModes.always,
                archive_resolution="10x10",
            )

    @httpretty.activate
    def test_create_session_with_e2ee(self):
        httpretty.register_uri(
            httpretty.POST,
            u("https://api.opentok.com/session/create"),
            body=u(
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'
            ),
            status=200,
            content_type=u("text/xml"),
        )

        session = self.opentok.create_session(e2ee=True)

        body = parse_qs(httpretty.last_request().body)
        expect(body).to(have_key(b("e2ee"), [b"true"]))
        expect(session).to(be_a(Session))
        expect(session).to(
            have_property(
                u("session_id"),
                u(
                    "1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg"
                ),
            )
        )
        expect(session).to(have_property(u("e2ee"), True))

    # TODO: all the cases that throw exceptions
    # TODO: custom api_url requests
