from datetime import datetime  # generate_token
import calendar  # generate_token
import base64  # generate_token
import random  # generate_token
import time  # generate_token
import hmac  # _sign_string
import hashlib  # _sign_string
import requests  # create_session, archiving
import json  # archiving
import platform  # user-agent
from socket import inet_aton  # create_session
import xml.dom.minidom as xmldom  # create_session
from jose import jwt  # _create_jwt_auth_header
import random  # _create_jwt_auth_header
import logging  # logging
import warnings  # Native. Used for notifying deprecations


# compat
from six.moves.urllib.parse import urlencode
from six import text_type, u, b, PY3
from enum import Enum

from .version import __version__
from .endpoints import Endpoints
from .session import Session
from .archives import Archive, ArchiveList, OutputModes
from .stream import Stream
from .streamlist import StreamList
from .sip_call import SipCall
from .broadcast import Broadcast
from .exceptions import (
    OpenTokException,
    RequestError,
    AuthError,
    NotFoundError,
    ArchiveError,
    SignalingError,
    GetStreamError,
    ForceDisconnectError,
    SipDialError,
    SetStreamClassError,
    BroadcastError,
)


class Roles(Enum):
    """List of valid roles for a token."""

    subscriber = u("subscriber")
    """A subscriber can only subscribe to streams."""
    publisher = u("publisher")
    """A publisher can publish streams, subscribe to streams, and signal"""
    moderator = u("moderator")
    """In addition to the privileges granted to a publisher, in clients using the OpenTok.js 2.2
    library, a moderator can call the `forceUnpublish()` and `forceDisconnect()` method of the
    Session object.
    """


class MediaModes(Enum):
    """List of valid settings for the mediaMode parameter of the OpenTok.create_session() method."""

    routed = u("disabled")
    """The session will transmit streams using the OpenTok Media Server."""
    relayed = u("enabled")
    """The session will attempt to transmit streams directly between clients. If two clients
    cannot send and receive each others' streams, due to firewalls on the clients' networks,
    their streams will be relayed using the OpenTok TURN Server."""


class ArchiveModes(Enum):
    """List of valid settings for the archive_mode parameter of the OpenTok.create_Session()
    method."""

    manual = u("manual")
    """The session will be manually archived."""
    always = u("always")
    """The session will be automatically archived."""


logger = logging.getLogger("opentok")



class Client(object):

    """Use this SDK to create tokens and interface with the server-side portion
    of the Opentok API.
    """

    TOKEN_SENTINEL = "T1=="
    """For internal use."""

    def __init__(
        self,
        api_key,
        api_secret,
        api_url="https://api.opentok.com",
        timeout=None,
        app_version=None,
    ):
        self.api_key = str(api_key)
        self.api_secret = api_secret
        self.timeout = timeout
        self._proxies = None
        self.endpoints = Endpoints(api_url, self.api_key)
        self._app_version = __version__ if app_version == None else app_version
        # JWT custom claims - Default values
        self._jwt_livetime = 3  # In minutes

    @property
    def proxies(self):
        return self._proxies

    @proxies.setter
    def proxies(self, proxies):
        self._proxies = proxies

    @property
    def app_version(self):
        return self._app_version

    @app_version.setter
    def app_version(self, value):
        self._app_version = value

    @property
    def jwt_livetime(self):
        return self._jwt_livetime

    @jwt_livetime.setter
    def jwt_livetime(self, minutes):
        self._jwt_livetime = minutes

    def generate_token(
        self,
        session_id,
        role=Roles.publisher,
        expire_time=None,
        data=None,
        initial_layout_class_list=[],
    ):
        """
        Generates a token for a given session.

        :param String session_id: The session ID of the session to be accessed by the client using
          the token.

        :param String role: The role for the token. Valid values are defined in the Role
          class:

          * `Roles.subscriber` -- A subscriber can only subscribe to streams.

          * `Roles.publisher` -- A publisher can publish streams, subscribe to
            streams, and signal. (This is the default value if you do not specify a role.)

          * `Roles.moderator` -- In addition to the privileges granted to a
            publisher, in clients using the OpenTok.js 2.2 library, a moderator can call the
            `forceUnpublish()` and `forceDisconnect()` method of the
            Session object.

        :param int expire_time: The expiration time of the token, in seconds since the UNIX epoch.
          The maximum expiration time is 30 days after the creation time. The default expiration
          time is 24 hours after the token creation time.

        :param String data: A string containing connection metadata describing the
          end-user. For example, you can pass the user ID, name, or other data describing the
          end-user. The length of the string is limited to 1000 characters. This data cannot be
          updated once it is set.

        :param list initial_layout_class_list: An array of class names (strings)
          to be used as the initial layout classes for streams published by the client. Layout
          classes are used in customizing the layout of videos in
          `live streaming broadcasts <https://tokbox.com/developer/guides/broadcast/#live-streaming>`_ and
          `composed archives <https://tokbox.com/developer/guides/archiving/layout-control.html>`_

        :rtype:
          The token string.
        """

        # normalize
        # expire_time can be an integer, a datetime object, or anything else that can be coerced into an integer
        # after this block it will only be an integer
        if expire_time is not None:
            if isinstance(expire_time, datetime):
                expire_time = calendar.timegm(expire_time.utctimetuple())
            else:
                try:
                    expire_time = int(expire_time)
                except (ValueError, TypeError):
                    raise OpenTokException(
                        u("Cannot generate token, invalid expire time {0}").format(
                            expire_time
                        )
                    )
        else:
            expire_time = int(time.time()) + (60 * 60 * 24)  # 1 day

        # validations
        if not text_type(session_id):
            raise OpenTokException(
                u("Cannot generate token, session_id was not valid {0}").format(
                    session_id
                )
            )
        if not isinstance(role, Roles):
            raise OpenTokException(
                u("Cannot generate token, {0} is not a valid role").format(role)
            )
        now = int(time.time())
        if expire_time < now:
            raise OpenTokException(
                u("Cannot generate token, expire_time is not in the future {0}").format(
                    expire_time
                )
            )
        if expire_time > now + (60 * 60 * 24 * 30):  # 30 days
            raise OpenTokException(
                u(
                    "Cannot generate token, expire_time is not in the next 30 days {0}"
                ).format(expire_time)
            )
        if data and len(data) > 1000:
            raise OpenTokException(
                u("Cannot generate token, data must be less than 1000 characters")
            )
        if initial_layout_class_list and not all(
            text_type(c) for c in initial_layout_class_list
        ):
            raise OpenTokException(
                u(
                    "Cannot generate token, all items in initial_layout_class_list must be strings"
                )
            )
        initial_layout_class_list_serialized = u(" ").join(initial_layout_class_list)
        if len(initial_layout_class_list_serialized) > 1000:
            raise OpenTokException(
                u(
                    "Cannot generate token, initial_layout_class_list must be less than 1000 characters"
                )
            )

        # decode session id to verify api_key
        sub_session_id = session_id[2:]
        sub_session_id_bytes = sub_session_id.encode("utf-8")
        sub_session_id_bytes_padded = sub_session_id_bytes + (
            b("=") * (-len(sub_session_id_bytes) % 4)
        )
        try:
            decoded_session_id = base64.b64decode(sub_session_id_bytes_padded, b("-_"))
            parts = decoded_session_id.decode("utf-8").split(u("~"))
        except Exception as e:
            raise OpenTokException(
                u("Cannot generate token, the session_id {0} was not valid").format(
                    session_id
                )
            )
        if self.api_key not in parts:
            raise OpenTokException(
                u(
                    "Cannot generate token, the session_id {0} does not belong to the api_key {1}"
                ).format(session_id, self.api_key)
            )

        data_params = dict(
            session_id=session_id,
            create_time=now,
            expire_time=expire_time,
            role=role.value,
            nonce=random.randint(0, 999999),
            initial_layout_class_list=initial_layout_class_list_serialized,
        )
        if data:
            data_params["connection_data"] = data
        data_string = urlencode(data_params, True)

        sig = self._sign_string(data_string, self.api_secret)
        decoded_base64_bytes = u("partner_id={api_key}&sig={sig}:{payload}").format(
            api_key=self.api_key, sig=sig, payload=data_string
        )
        if PY3:
            decoded_base64_bytes = decoded_base64_bytes.encode("utf-8")
        token = u("{sentinal}{base64_data}").format(
            sentinal=self.TOKEN_SENTINEL,
            base64_data=base64.b64encode(decoded_base64_bytes).decode(),
        )
        return token

    def create_session(
        self,
        location=None,
        media_mode=MediaModes.relayed,
        archive_mode=ArchiveModes.manual,
    ):
        """
        Creates a new OpenTok session and returns the session ID, which uniquely identifies
        the session.

        For example, when using the OpenTok JavaScript library, use the session ID when calling the
        OT.initSession() method (to initialize an OpenTok session).

        OpenTok sessions do not expire. However, authentication tokens do expire (see the
        generateToken() method). Also note that sessions cannot explicitly be destroyed.

        A session ID string can be up to 255 characters long.

        Calling this method results in an OpenTokException in the event of an error.
        Check the error message for details.

        You can also create a session using the OpenTok
        `REST API <https://tokbox.com/opentok/api/#session_id_production>`_ or
        `the OpenTok dashboard <https://dashboard.tokbox.com/projects>`_.

        :param String media_mode: Determines whether the session will transmit streams using the
             OpenTok Media Router (MediaMode.routed) or not (MediaMode.relayed). By default,
             the setting is MediaMode.relayed.

             With the media_mode property set to MediaMode.relayed, the session
             will attempt to transmit streams directly between clients. If clients cannot connect
             due to firewall restrictions, the session uses the OpenTok TURN server to relay
             audio-video streams.

             The `OpenTok Media
             Router <https://tokbox.com/opentok/tutorials/create-session/#media-mode>`_
             provides the following benefits:

               * The OpenTok Media Router can decrease bandwidth usage in multiparty sessions.
                   (When the mediaMode property is set to  MediaMode.relayed, each client must send
                   a separate audio-video stream to each client subscribing to it.)

               * The OpenTok Media Router can improve the quality of the user experience through
                 audio fallback and video recovery (see https://tokbox.com/platform/fallback). With
                 these features, if a client's connectivity degrades to a degree that
                 it does not support video for a stream it's subscribing to, the video is dropped on
                 that client (without affecting other clients), and the client receives audio only.
                 If the client's connectivity improves, the video returns.

               * The OpenTok Media Router supports the archiving feature, which lets
                 you record, save, and retrieve OpenTok sessions (see http://tokbox.com/platform/archiving).

        :param String archive_mode: Whether the session is automatically archived
            (ArchiveModes.always) or not (ArchiveModes.manual). By default,
            the setting is ArchiveModes.manual, and you must call the
            start_archive() method of the OpenTok object to start archiving. To archive the session
            (either automatically or not), you must set the media_mode parameter to
            MediaModes.routed.

        :param String location: An IP address that the OpenTok servers will use to
            situate the session in its global network. If you do not set a location hint,
            the OpenTok servers will be based on the first client connecting to the session.

        :rtype: The Session object. The session_id property of the object is the session ID.
        """

        # build options
        options = {}
        if not isinstance(media_mode, MediaModes):
            raise OpenTokException(
                u("Cannot create session, {0} is not a valid media mode").format(
                    media_mode
                )
            )
        if not isinstance(archive_mode, ArchiveModes):
            raise OpenTokException(
                u("Cannot create session, {0} is not a valid archive mode").format(
                    archive_mode
                )
            )
        if archive_mode == ArchiveModes.always and media_mode != MediaModes.routed:
            raise OpenTokException(
                u(
                    "A session with always archive mode must also have the routed media mode."
                )
            )
        options[u("p2p.preference")] = media_mode.value
        options[u("archiveMode")] = archive_mode.value
        if location:
            # validate IP address
            try:
                inet_aton(location)
            except:
                raise OpenTokException(
                    u(
                        "Cannot create session. Location must be either None or a valid IPv4 address {0}"
                    ).format(location)
                )
            options[u("location")] = location

        try:
            logger.debug(
                "POST to %r with params %r, headers %r, proxies %r",
                self.endpoints.session_url(),
                options,
                self.headers(),
                self.proxies,
            )
            response = requests.post(
                self.endpoints.get_session_url(),
                data=options,
                headers=self.get_headers(),
                proxies=self.proxies,
                timeout=self.timeout,
            )
            response.encoding = "utf-8"

            if response.status_code == 403:
                raise AuthError("Failed to create session, invalid credentials")
            if not response.content:
                raise RequestError()
            dom = xmldom.parseString(response.content.decode("utf-8"))
        except Exception as e:
            raise RequestError("Failed to create session: %s" % str(e))

        try:
            error = dom.getElementsByTagName("error")
            if error:
                error = error[0]
                raise AuthError(
                    "Failed to create session (code=%s): %s"
                    % (
                        error.attributes["code"].value,
                        error.firstChild.attributes["message"].value,
                    )
                )

            session_id = (
                dom.getElementsByTagName("session_id")[0].childNodes[0].nodeValue
            )
            return Session(
                self,
                session_id,
                location=location,
                media_mode=media_mode,
                archive_mode=archive_mode,
            )
        except Exception as e:
            raise OpenTokException("Failed to generate session: %s" % str(e))

    def get_headers(self):
        """For internal use."""
        return {
            "User-Agent": "OpenTok-Python-SDK/"
            + self.app_version
            + " python/"
            + platform.python_version(),
            "X-OPENTOK-AUTH": self._create_jwt_auth_header(),
        }

    def headers(self):
        warnings.warn(
            "opentok.headers is deprecated (use opentok.get_headers instead).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_headers()

    def get_json_headers(self):
        """For internal use."""
        result = self.get_headers()
        result["Content-Type"] = "application/json"
        return result

    def json_headers(self):
        warnings.warn(
            "opentok.json_headers is deprecated (use opentok.get_json_headers instead).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_json_headers()

    def start_archive(
        self,
        session_id,
        has_audio=True,
        has_video=True,
        name=None,
        output_mode=OutputModes.composed,
        resolution=None,
        layout=None,
    ):
        """
        Starts archiving an OpenTok session.

        Clients must be actively connected to the OpenTok session for you to successfully start
        recording an archive.

        You can only record one archive at a time for a given session. You can only record archives
        of sessions that use the OpenTok Media Router (sessions with the media mode set to routed);
        you cannot archive sessions with the media mode set to relayed.

        For more information on archiving, see the
        `OpenTok archiving <https://tokbox.com/opentok/tutorials/archiving/>`_ programming guide.

        :param String session_id: The session ID of the OpenTok session to archive.
        :param String name: This is the name of the archive. You can use this name
          to identify the archive. It is a property of the Archive object, and it is a property
          of archive-related events in the OpenTok.js library.
        :param Boolean has_audio: if set to True, an audio track will be inserted to the archive.
          has_audio is an optional parameter that is set to True by default. If you set both
          has_audio and has_video to False, the call to the start_archive() method results in
          an error.
        :param Boolean has_video: if set to True, a video track will be inserted to the archive.
          has_video is an optional parameter that is set to True by default.
        :param OutputModes output_mode: Whether all streams in the archive are recorded
          to a single file (OutputModes.composed, the default) or to individual files
          (OutputModes.individual).
        :param String resolution (Optional): The resolution of the archive, either "640x480" (the default)
          or "1280x720". This parameter only applies to composed archives. If you set this
          parameter and set the output_mode parameter to OutputModes.individual, the call to the
          start_archive() method results in an error.
        :param Dictionary 'layout' optional: Specify this to assign the initial layout type for the
            archive.

            String 'type': Type of layout. Valid values for the layout property are "bestFit" (best fit),
            "custom" (custom), "horizontalPresentation" (horizontal presentation), "pip" (picture-in-picture),
            and "verticalPresentation" (vertical presentation)). If you specify a "custom" layout type, set
            the stylesheet property of the layout object to the stylesheet.

            String 'stylesheet' optional: Custom stylesheet to use for layout. Must set 'type' to custom,
            and cannot use 'screenshareType'

            String 'screenshareType' optional: Layout to use for screenshares. If this is set, you must
            set 'type' to 'bestFit'

        :rtype: The Archive object, which includes properties defining the archive,
          including the archive ID.
        """
        if not isinstance(output_mode, OutputModes):
            raise OpenTokException(
                u("Cannot start archive, {0} is not a valid output mode").format(
                    output_mode
                )
            )

        if resolution and output_mode == OutputModes.individual:
            raise OpenTokException(
                u(
                    "Invalid parameters: Resolution cannot be supplied for individual output mode."
                )
            )

        payload = {
            "name": name,
            "sessionId": session_id,
            "hasAudio": has_audio,
            "hasVideo": has_video,
            "outputMode": output_mode.value,
            "resolution": resolution,
        }

        if layout is not None:
            payload['layout'] = layout

        logger.debug(
            "POST to %r with params %r, headers %r, proxies %r",
            self.endpoints.archive_url(),
            json.dumps(payload),
            self.json_headers(),
            self.proxies,
        )

        response = requests.post(
            self.endpoints.get_archive_url(),
            data=json.dumps(payload),
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code < 300:
            return Archive(self, response.json())
        elif response.status_code == 403:
            raise AuthError()
        elif response.status_code == 400:
            """
            The HTTP response has a 400 status code in the following cases:
            You do not pass in a session ID or you pass in an invalid session ID.
            No clients are actively connected to the OpenTok session.
            You specify an invalid resolution value.
            The outputMode property is set to "individual" and you set the resolution property and (which is not supported in individual stream archives).
            """
            raise RequestError(response.json().get("message"))
        elif response.status_code == 404:
            raise NotFoundError("Session not found")
        elif response.status_code == 409:
            raise ArchiveError(response.json().get("message"))
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def stop_archive(self, archive_id):
        """
        Stops an OpenTok archive that is being recorded.

        Archives automatically stop recording after 90 minutes or when all clients have disconnected
        from the session being archived.

        @param [String] archive_id The archive ID of the archive you want to stop recording.

        :rtype: The Archive object corresponding to the archive being stopped.
        """
        logger.debug(
            "POST to %r with headers %r, proxies %r",
            self.endpoints.archive_url(archive_id) + "/stop",
            self.json_headers(),
            self.proxies,
        )

        response = requests.post(
            self.endpoints.get_archive_url(archive_id) + "/stop",
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code < 300:
            return Archive(self, response.json())
        elif response.status_code == 403:
            raise AuthError()
        elif response.status_code == 404:
            raise NotFoundError("Archive not found")
        elif response.status_code == 409:
            raise ArchiveError("Archive is not in started state")
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def delete_archive(self, archive_id):
        """
        Deletes an OpenTok archive.

        You can only delete an archive which has a status of "available" or "uploaded". Deleting an
        archive removes its record from the list of archives. For an "available" archive, it also
        removes the archive file, making it unavailable for download.

        :param String archive_id: The archive ID of the archive to be deleted.
        """
        logger.debug(
            "DELETE to %r with headers %r, proxies %r",
            self.endpoints.archive_url(archive_id),
            self.json_headers(),
            self.proxies,
        )

        response = requests.delete(
            self.endpoints.get_archive_url(archive_id),
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code < 300:
            pass
        elif response.status_code == 403:
            raise AuthError()
        elif response.status_code == 404:
            raise NotFoundError("Archive not found")
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def get_archive(self, archive_id):
        """Gets an Archive object for the given archive ID.

        :param String archive_id: The archive ID.

        :rtype: The Archive object.
        """
        logger.debug(
            "GET to %r with headers %r, proxies %r",
            self.endpoints.archive_url(archive_id),
            self.json_headers(),
            self.proxies,
        )

        response = requests.get(
            self.endpoints.get_archive_url(archive_id),
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code < 300:
            return Archive(self, response.json())
        elif response.status_code == 403:
            raise AuthError()
        elif response.status_code == 404:
            raise NotFoundError("Archive not found")
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def get_archives(self, offset=None, count=None, session_id=None):
        """Returns an ArchiveList, which is an array of archives that are completed and in-progress,
        for your API key.

        :param int: offset Optional. The index offset of the first archive. 0 is offset
          of the most recently started archive. 1 is the offset of the archive that started prior to
          the most recent archive. If you do not specify an offset, 0 is used.
        :param int: count Optional. The number of archives to be returned. The maximum
          number of archives returned is 1000.
        :param string: session_id Optional. Used to list archives for a specific session ID.

        :rtype: An ArchiveList object, which is an array of Archive objects.
        """
        params = {}
        if offset is not None:
            params["offset"] = offset
        if count is not None:
            params["count"] = count
        if session_id is not None:
            params["sessionId"] = session_id

        endpoint = self.endpoints.get_archive_url() + "?" + urlencode(params)

        logger.debug(
            "GET to %r with headers %r, proxies %r",
            endpoint,
            self.json_headers(),
            self.proxies,
        )

        response = requests.get(
            endpoint,
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code < 300:
            return ArchiveList(self, response.json())
        elif response.status_code == 403:
            raise AuthError()
        elif response.status_code == 404:
            raise NotFoundError("Archive not found")
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def list_archives(self, offset=None, count=None, session_id=None):
        """
        New method to get archive list, it's alternative to 'get_archives()',
        both methods exist to have backwards compatible
        """
        return self.get_archives(offset, count, session_id)

    def send_signal(self, session_id, payload, connection_id=None):
        """
        Send signals to all participants in an active OpenTok session or to a specific client
        connected to that session.

        :param String session_id: The session ID of the OpenTok session that receives the signal

        :param Dictionary payload: Structure that contains both the type and data fields. These
        correspond to the type and data parameters passed in the client signal received handlers

        :param String connection_id: The connection_id parameter is an optional string used to
        specify the connection ID of a client connected to the session. If you specify this value,
        the signal is sent to the specified client. Otherwise, the signal is sent to all clients
        connected to the session
        """
        logger.debug(
            "POST to %r with params %r, headers %r, proxies %r",
            self.endpoints.signaling_url(session_id, connection_id),
            json.dumps(payload),
            self.json_headers(),
            self.proxies,
        )

        response = requests.post(
            self.endpoints.get_signaling_url(session_id, connection_id),
            data=json.dumps(payload),
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code == 204:
            pass
        elif response.status_code == 400:
            raise SignalingError(
                "One of the signal properties - data, type, sessionId or connectionId - is invalid."
            )
        elif response.status_code == 403:
            raise AuthError(
                "You are not authorized to send the signal. Check your authentication credentials."
            )
        elif response.status_code == 404:
            raise SignalingError(
                "The client specified by the connectionId property is not connected to the session."
            )
        elif response.status_code == 413:
            raise SignalingError(
                "The type string exceeds the maximum length (128 bytes), or the data string exceeds the maximum size (8 kB)."
            )
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def signal(self, session_id, payload, connection_id=None):
        warnings.warn(
            "opentok.signal is deprecated (use opentok.send_signal instead).",
            DeprecationWarning,
            stacklevel=2,
        )
        self.send_signal(session_id, payload, connection_id)

    def get_stream(self, session_id, stream_id):
        """
        Returns an Stream object that contains information of an OpenTok stream:

        -id: The stream ID
        -videoType: "camera" or "screen"
        -name: The stream name (if one was set when the client published the stream)
        -layoutClassList: It's an array of the layout classes for the stream
        """
        endpoint = self.endpoints.get_stream_url(session_id, stream_id)

        logger.debug(
            "GET to %r with headers %r, proxies %r",
            endpoint,
            self.json_headers(),
            self.proxies,
        )

        response = requests.get(
            endpoint,
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code == 200:
            return Stream(response.json())
        elif response.status_code == 400:
            raise GetStreamError(
                "Invalid request. This response may indicate that data in your request data is invalid JSON. Or it may indicate that you do not pass in a session ID or you passed in an invalid stream ID."
            )
        elif response.status_code == 403:
            raise AuthError("You passed in an invalid OpenTok API key or JWT token.")
        elif response.status_code == 408:
            raise GetStreamError("You passed in an invalid stream ID.")
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def list_streams(self, session_id):
        """
        Returns a list of Stream objects that contains information of all
        the streams in a OpenTok session, with the following attributes:

        -count: An integer that indicates the number of streams in the session
        -items: List of the Stream objects
        """
        endpoint = self.endpoints.get_stream_url(session_id)

        logger.debug(
            "GET to %r with headers %r, proxies %r",
            endpoint,
            self.json_headers(),
            self.proxies,
        )

        response = requests.get(
            endpoint,
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code == 200:
            return StreamList(response.json())
        elif response.status_code == 400:
            raise GetStreamError(
                "Invalid request. This response may indicate that data in your request data is invalid JSON. Or it may indicate that you do not pass in a session ID or you passed in an invalid stream ID."
            )
        elif response.status_code == 403:
            raise AuthError("You passed in an invalid OpenTok API key or JWT token.")
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def force_disconnect(self, session_id, connection_id):
        """
        Sends a request to disconnect a client from an OpenTok session

        :param String session_id: The session ID of the OpenTok session from which the
        client will be disconnected

        :param String connection_id: The connection ID of the client that will be disconnected
        """
        endpoint = self.endpoints.force_disconnect_url(session_id, connection_id)

        logger.debug(
            "DELETE to %r with headers %r, proxies %r",
            endpoint,
            self.json_headers(),
            self.proxies,
        )

        response = requests.delete(
            endpoint,
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code == 204:
            pass
        elif response.status_code == 400:
            raise ForceDisconnectError(
                "One of the arguments - sessionId or connectionId - is invalid."
            )
        elif response.status_code == 403:
            raise AuthError(
                "You are not authorized to forceDisconnect, check your authentication credentials."
            )
        elif response.status_code == 404:
            raise ForceDisconnectError(
                "The client specified by the connectionId property is not connected to the session."
            )
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def set_archive_layout(self, archive_id, layout_type, stylesheet=None, screenshare_type=None):
        """
        Use this method to change the layout of videos in an OpenTok archive

        :param String archive_id: The ID of the archive that will be updated

        :param String layout_type: The layout type for the archive. Valid values are:
        'bestFit', 'custom', 'horizontalPresentation', 'pip' and 'verticalPresentation'

        :param String stylesheet optional: CSS used to style the custom layout.
        Specify this only if you set the type property to 'custom'

        :param String screenshare_type optional: Layout to use for screenshares. Must
        set 'layout_type' to 'bestFit'
        """
        payload = {
            "type": layout_type,
        }

        if screenshare_type is not None:
            payload["screenshareType"] = screenshare_type

        if layout_type == "custom":
            if stylesheet is not None:
                payload["stylesheet"] = stylesheet

        endpoint = self.endpoints.set_archive_layout_url(archive_id)

        logger.debug(
            "PUT to %r with params %r, headers %r, proxies %r",
            endpoint,
            json.dumps(payload),
            self.json_headers(),
            self.proxies,
        )

        response = requests.put(
            endpoint,
            data=json.dumps(payload),
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code == 200:
            pass
        elif response.status_code == 400:
            raise ArchiveError(
                "Invalid request. This response may indicate that data in your request data is invalid JSON. It may also indicate that you passed in invalid layout options."
            )
        elif response.status_code == 403:
            raise AuthError("Authentication error.")
        else:
            raise RequestError("OpenTok server error.", response.status_code)

    def dial(self, session_id, token, sip_uri, options=[]):
        """
        Use this method to connect a SIP platform to an OpenTok session. The audio from the end
        of the SIP call is added to the OpenTok session as an audio-only stream. The OpenTok Media
        Router mixes audio from other streams in the session and sends the mixed audio to the SIP
        endpoint

        :param String session_id: The OpenTok session ID for the SIP call to join

        :param String token: The OpenTok token to be used for the participant being called

        :param String sip_uri: The SIP URI to be used as destination of the SIP call initiated from
        OpenTok to the SIP platform

        :param Dictionary options optional: Aditional options with the following properties:

            String 'from': The number or string that will be sent to the final SIP number
            as the caller

            Dictionary 'headers': Defines custom headers to be added to the SIP INVITE request
            initiated from OpenTok to the SIP platform. Each of the custom headers must
            start with the "X-" prefix, or the call will result in a Bad Request (400) response

            Dictionary 'auth': Contains the username and password to be used in the the SIP
            INVITE request for HTTP digest authentication, if it is required by the SIP platform
            For example:

                'auth': {
                    'username': 'username',
                    'password': 'password'
                }

            Boolean 'secure': A Boolean flag that indicates whether the media must be transmitted
            encrypted (true) or not (false, the default)

        :rtype: A SipCall object, which contains data of the SIP call: id, connectionId and streamId
        """
        payload = {"sessionId": session_id, "token": token, "sip": {"uri": sip_uri}}

        if "from" in options:
            payload["sip"]["from"] = options["from"]

        if "headers" in options:
            payload["sip"]["headers"] = options["headers"]

        if "auth" in options:
            payload["sip"]["auth"] = options["auth"]

        if "secure" in options:
            payload["sip"]["secure"] = options["secure"]

        endpoint = self.endpoints.dial_url()

        logger.debug(
            "POST to %r with params %r, headers %r, proxies %r",
            endpoint,
            json.dumps(payload),
            self.json_headers(),
            self.proxies,
        )

        response = requests.post(
            endpoint,
            data=json.dumps(payload),
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code == 200:
            return SipCall(response.json())
        elif response.status_code == 400:
            raise SipDialError("Invalid request. Invalid session ID.")
        elif response.status_code == 403:
            raise AuthError("Authentication error.")
        elif response.status_code == 404:
            raise SipDialError("The session does not exist.")
        elif response.status_code == 409:
            raise SipDialError(
                "You attempted to start a SIP call for a session that "
                "does not use the OpenTok Media Router."
            )
        else:
            raise RequestError("OpenTok server error.", response.status_code)

    def set_stream_class_lists(self, session_id, payload):
        """
        Use this method to change layout classes for OpenTok streams. The layout classes
        define how the streams are displayed in the layout of a composed OpenTok archive

        :param String session_id: The ID of the session of the streams that will be updated

        :param List payload: A list defining the class lists to apply to the streams.
        Each element in the list is a dictionary with two properties: 'id' and 'layoutClassList'.
        The 'id' property is the stream ID (a String), and the 'layoutClassList' is an array of
        class names (Strings) to apply to the stream. For example:

            payload = [
                {'id': '7b09ec3c-26f9-43d7-8197-f608f13d4fb6', 'layoutClassList': ['focus']},
                {'id': '567bc941-6ea0-4c69-97fc-70a740b68976', 'layoutClassList': ['top']},
                {'id': '307dc941-0450-4c09-975c-705740d08970', 'layoutClassList': ['bottom']}
            ]
        """
        items_payload = {"items": payload}

        endpoint = self.endpoints.set_stream_class_lists_url(session_id)

        logger.debug(
            "PUT to %r with params %r, headers %r, proxies %r",
            endpoint,
            json.dumps(items_payload),
            self.json_headers(),
            self.proxies,
        )

        response = requests.put(
            endpoint,
            data=json.dumps(items_payload),
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code == 200:
            pass
        elif response.status_code == 400:
            raise SetStreamClassError(
                "Invalid request. This response may indicate that data in your request data "
                "is invalid JSON. It may also indicate that you passed in invalid layout options."
            )
        elif response.status_code == 403:
            raise AuthError("Authentication error.")
        else:
            raise RequestError("OpenTok server error.", response.status_code)

    def start_broadcast(self, session_id, options):
        """
        Use this method to start a live streaming for an OpenTok session. This broadcasts the
        session to an HLS (HTTP live streaming) or to RTMP streams. To successfully start
        broadcasting a session, at least one client must be connected to the session. You can only
        start live streaming for sessions that use the OpenTok Media Router (with the media mode set
        to routed); you cannot use live streaming with sessions that have the media mode set to
        relayed

        :param String session_id: The session ID of the OpenTok session you want to broadcast

        :param Dictionary options, with the following properties:

            Dictionary 'layout' optional: Specify this to assign the initial layout type for the
            broadcast.

                String 'type': Type of layout. Valid values for the layout property are "bestFit" (best fit),
                "custom" (custom), "horizontalPresentation" (horizontal presentation), "pip" (picture-in-picture),
                and "verticalPresentation" (vertical presentation)). If you specify a "custom" layout type, set
                the stylesheet property of the layout object to the stylesheet.

                String 'stylesheet' optional: Custom stylesheet to use for layout. Must set 'type' to custom,
                and cannot use 'screenshareType'

                String 'screenshareType' optional: Layout to use for screenshares. If this is set, you must
                set 'type' to 'bestFit'

            Integer 'maxDuration' optional: The maximum duration for the broadcast, in seconds.
            The broadcast will automatically stop when the maximum duration is reached. You can
            set the maximum duration to a value from 60 (60 seconds) to 36000 (10 hours). The
            default maximum duration is 2 hours (7200 seconds)

            Dictionary 'outputs': This object defines the types of broadcast streams you want to
            start (both HLS and RTMP). You can include HLS, RTMP, or both as broadcast streams.
            If you include RTMP streaming, you can specify up to five target RTMP streams. For
            each RTMP stream, specify 'serverUrl' (the RTMP server URL), 'streamName' (the stream
            name, such as the YouTube Live stream name or the Facebook stream key), and
            (optionally) 'id' (a unique ID for the stream)

            String 'resolution' optional: The resolution of the broadcast, either "640x480"
            (SD, the default) or "1280x720" (HD)

        :rtype A Broadcast object, which contains information of the broadcast: id, sessionId
        projectId, createdAt, updatedAt, resolution, status and broadcastUrls
        """
        payload = {"sessionId": session_id}

        payload.update(options)

        endpoint = self.endpoints.broadcast_url()

        logger.debug(
            "POST to %r with params %r, headers %r, proxies %r",
            endpoint,
            json.dumps(payload),
            self.json_headers(),
            self.proxies,
        )

        response = requests.post(
            endpoint,
            data=json.dumps(payload),
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code == 200:
            return Broadcast(response.json())
        elif response.status_code == 400:
            raise BroadcastError(
                "Invalid request. This response may indicate that data in your request data is "
                "invalid JSON. It may also indicate that you passed in invalid layout options. "
                "Or you have exceeded the limit of five simultaneous RTMP streams for an OpenTok "
                "session. Or you specified and invalid resolution."
            )
        elif response.status_code == 403:
            raise AuthError("Authentication error.")
        elif response.status_code == 409:
            raise BroadcastError("The broadcast has already started for the session.")
        else:
            raise RequestError("OpenTok server error.", response.status_code)

    def stop_broadcast(self, broadcast_id):
        """
        Use this method to stop a live broadcast of an OpenTok session

        :param String broadcast_id: The ID of the broadcast you want to stop

        :rtype A Broadcast object, which contains information of the broadcast: id, sessionId
        projectId, createdAt, updatedAt and resolution
        """

        endpoint = self.endpoints.broadcast_url(broadcast_id, stop=True)

        logger.debug(
            "POST to %r with headers %r, proxies %r",
            endpoint,
            self.json_headers(),
            self.proxies,
        )
    
        response = requests.post(
            endpoint,
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code == 200:
            return Broadcast(response.json())
        elif response.status_code == 400:
            raise BroadcastError(
                "Invalid request. This response may indicate that data in your request "
                "data is invalid JSON."
            )
        elif response.status_code == 403:
            raise AuthError("Authentication error.")
        elif response.status_code == 409:
            raise BroadcastError(
                "The broadcast (with the specified ID) was not found or it has already "
                "stopped."
            )
        else:
            raise RequestError("OpenTok server error.", response.status_code)

    def get_broadcast(self, broadcast_id):
        """
        Use this method to get details on a broadcast that is in-progress.

        :param String broadcast_id: The ID of the broadcast you want to stop

        :rtype A Broadcast object, which contains information of the broadcast: id, sessionId
        projectId, createdAt, updatedAt, resolution, broadcastUrls and status
        """

        endpoint = self.endpoints.broadcast_url(broadcast_id)

        logger.debug(
            "GET to %r with headers %r, proxies %r",
            endpoint,
            self.json_headers(),
            self.proxies,
        )

        response = requests.get(
            endpoint,
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code == 200:
            return Broadcast(response.json())
        elif response.status_code == 400:
            raise BroadcastError(
                "Invalid request. This response may indicate that data in your request "
                "data is invalid JSON."
            )
        elif response.status_code == 403:
            raise AuthError("Authentication error.")
        elif response.status_code == 409:
            raise BroadcastError("No matching broadcast found (with the specified ID).")
        else:
            raise RequestError("OpenTok server error.", response.status_code)

    def set_broadcast_layout(self, broadcast_id, layout_type, stylesheet=None, screenshare_type=None):
        """
        Use this method to change the layout type of a live streaming broadcast

        :param String broadcast_id: The ID of the broadcast that will be updated

        :param String layout_type: The layout type for the broadcast. Valid values are:
        'bestFit', 'custom', 'horizontalPresentation', 'pip' and 'verticalPresentation'

        :param String stylesheet optional: CSS used to style the custom layout.
        Specify this only if you set the type property to 'custom'

        :param String screenshare_type optional: Layout to use for screenshares. Must
        set 'layout_type' to 'bestFit'
        """
        payload = {
            "type": layout_type,
        }

        if screenshare_type is not None:
            payload["screenshareType"] = screenshare_type

        if layout_type == "custom":
            if stylesheet is not None:
                payload["stylesheet"] = stylesheet

        endpoint = self.endpoints.broadcast_url(broadcast_id, layout=True)

        logger.debug(
            "PUT to %r with params %r, headers %r, proxies %r",
            endpoint,
            json.dumps(payload),
            self.json_headers(),
            self.proxies,
        )

        response = requests.put(
            endpoint,
            data=json.dumps(payload),
            headers=self.get_json_headers(),
            proxies=self.proxies,
            timeout=self.timeout,
        )

        if response.status_code == 200:
            pass
        elif response.status_code == 400:
            raise BroadcastError(
                "Invalid request. This response may indicate that data in your request data is "
                "invalid JSON. It may also indicate that you passed in invalid layout options."
            )
        elif response.status_code == 403:
            raise AuthError("Authentication error.")
        else:
            raise RequestError("OpenTok server error.", response.status_code)

    def _sign_string(self, string, secret):
        return hmac.new(
            secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha1
        ).hexdigest()

    def _create_jwt_auth_header(self):
        payload = {
            "ist": "project",
            "iss": self.api_key,
            "iat": int(time.time()),  # current time in unix time (seconds)
            "exp": int(time.time())
            + (60 * self._jwt_livetime),  # 3 minutes in the future (seconds)
            "jti": "{0}".format(0, random.random()),
        }

        return jwt.encode(payload, self.api_secret, algorithm="HS256")

class OpenTok(Client):
    def __init__(
        self,
        api_key,
        api_secret,
        api_url="https://api.opentok.com",
        timeout=None,
        app_version=None,
    ):
        warnings.warn(
            "OpenTok class is deprecated (Use Client class instead)",
            DeprecationWarning,
            stacklevel=2,
        )
        super(OpenTok, self).__init__(
            api_key,
            api_secret,
            api_url=api_url,
            timeout=timeout,
            app_version=app_version
        )
