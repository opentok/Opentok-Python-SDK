from datetime import datetime  # generate_token
import calendar                # generate_token
import base64                  # generate_token
import random                  # generate_token
import time                    # generate_token
import hmac                    # _sign_string
import hashlib                 # _sign_string
import requests                # create_session, archiving
import json                    # archiving
from socket import inet_aton   # create_session
import xml.dom.minidom as xmldom # create_session

# compat
from six.moves.urllib.parse import urlencode
from six import text_type, u, b, PY3
from enum import Enum

from .version import __version__
from .session import Session
from .archives import Archive, ArchiveList, OutputModes
from .exceptions import OpenTokException, RequestError, AuthError, NotFoundError, ArchiveError

class Roles(Enum):
    """List of valid roles for a token."""
    subscriber = u('subscriber')
    """A subscriber can only subscribe to streams."""
    publisher =  u('publisher')
    """A publisher can publish streams, subscribe to streams, and signal"""
    moderator =  u('moderator')
    """In addition to the privileges granted to a publisher, in clients using the OpenTok.js 2.2
    library, a moderator can call the `forceUnpublish()` and `forceDisconnect()` method of the
    Session object.
    """

class MediaModes(Enum):
    """List of valid settings for the mediaMode parameter of the OpenTok.create_session() method."""
    routed = u('disabled')
    """The session will transmit streams using the OpenTok Media Server."""
    relayed = u('enabled')
    """The session will attempt to transmit streams directly between clients. If two clients
    cannot send and receive each others' streams, due to firewalls on the clients' networks,
    their streams will be relayed using the OpenTok TURN Server."""

class ArchiveModes(Enum):
    """List of valid settings for the archive_mode parameter of the OpenTok.create_Session()
    method."""
    manual = u('manual')
    """The session will be manually archived."""
    always = u('always')
    """The session will be automatically archived."""

class OpenTok(object):
    """Use this SDK to create tokens and interface with the server-side portion
    of the Opentok API.
    """
    TOKEN_SENTINEL = 'T1=='
    """For internal use."""

    def __init__(self, api_key, api_secret, api_url='https://api.opentok.com'):
        self.api_key = str(api_key)
        self.api_secret = api_secret
        self.api_url = api_url
        self._proxies = None

    @property
    def proxies(self):
        return self._proxies

    @proxies.setter
    def proxies(self, proxies):
        self._proxies = proxies

    def generate_token(self, session_id, role=Roles.publisher, expire_time=None, data=None):
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
                    raise OpenTokException(u('Cannot generate token, invalid expire time {0}').format(expire_time))
        else:
            expire_time = int(time.time()) + (60*60*24) # 1 day

        # validations
        if not text_type(session_id):
            raise OpenTokException(u('Cannot generate token, session_id was not valid {0}').format(session_id))
        if not isinstance(role, Roles):
            raise OpenTokException(u('Cannot generate token, {0} is not a valid role').format(role))
        now = int(time.time())
        if expire_time < now:
            raise OpenTokException(u('Cannot generate token, expire_time is not in the future {0}').format(expire_time))
        if expire_time > now + (60*60*24*30):  # 30 days
            raise OpenTokException(u('Cannot generate token, expire_time is not in the next 30 days {0}').format(expire_time))
        if (data is not None) and len(data) > 1000:
            raise OpenTokException(u('Cannot generate token, data must be less than 1000 characters').format(data))

        # decode session id to verify api_key
        sub_session_id = session_id[2:]
        sub_session_id_bytes = sub_session_id.encode('utf-8')
        sub_session_id_bytes_padded = sub_session_id_bytes + (b('=') * (-len(sub_session_id_bytes) % 4))
        try:
            decoded_session_id = base64.b64decode(sub_session_id_bytes_padded, b('-_'))
            parts = decoded_session_id.decode('utf-8').split(u('~'))
        except Exception as e:
            raise OpenTokException(u('Cannot generate token, the session_id {0} was not valid').format(session_id))
        if self.api_key not in parts:
            raise OpenTokException(u('Cannot generate token, the session_id {0} does not belong to the api_key {1}').format(session_id, self.api_key))

        data_params = dict(
            session_id      = session_id,
            create_time     = now,
            expire_time     = expire_time,
            role            = role.value,
            connection_data = (data or None),
            nonce           = random.randint(0,999999)
        )
        data_string = urlencode(data_params, True)

        sig = self._sign_string(data_string, self.api_secret)
        decoded_base64_bytes = u('partner_id={api_key}&sig={sig}:{payload}').format(
            api_key = self.api_key,
            sig     = sig,
            payload = data_string
        )
        if PY3:
            decoded_base64_bytes = decoded_base64_bytes.encode('utf-8')
        token = u('{sentinal}{base64_data}').format(
            sentinal    = self.TOKEN_SENTINEL,
            base64_data = base64.b64encode(decoded_base64_bytes).decode()
        )
        return token

    def create_session(self, location=None, media_mode=MediaModes.relayed, archive_mode=ArchiveModes.manual):
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
            raise OpenTokException(u('Cannot create session, {0} is not a valid media mode').format(role))
        if not isinstance(archive_mode, ArchiveModes):
            raise OpenTokException(u('Cannot create session, {0} is not a valid archive mode').format(role))
        if archive_mode == ArchiveModes.always and media_mode != MediaModes.routed:
            raise OpenTokException(u('A session with always archive mode must also have the routed media mode.'))
        options[u('p2p.preference')] = media_mode.value
        options[u('archiveMode')] = archive_mode.value
        if location:
            # validate IP address
            try:
                inet_aton(location)
            except:
                raise OpenTokException(u('Cannot create session. Location must be either None or a valid IPv4 address {0}').format(location))
            options[u('location')] = location

        try:
            response = requests.post(self.session_url(), data=options, headers=self.headers(), proxies=self.proxies)
            response.encoding = 'utf-8'

            if response.status_code == 403:
                raise AuthError('Failed to create session, invalid credentials')
            if not response.content:
                raise RequestError()
            dom = xmldom.parseString(response.content)
        except Exception as e:
            raise RequestError('Failed to create session: %s' % str(e))

        try:
            error = dom.getElementsByTagName('error')
            if error:
                error = error[0]
                raise AuthError('Failed to create session (code=%s): %s' % (error.attributes['code'].value, error.firstChild.attributes['message'].value))

            session_id = dom.getElementsByTagName('session_id')[0].childNodes[0].nodeValue
            return Session(self, session_id, location=location, media_mode=media_mode, archive_mode=archive_mode)
        except Exception as e:
            raise OpenTokException('Failed to generate session: %s' % str(e))

    def headers(self):
        """For internal use."""
        return {
            'User-Agent': 'OpenTok-Python-SDK/' + __version__,
            'X-TB-PARTNER-AUTH': self.api_key + ':' + self.api_secret
        }

    def archive_headers(self):
        """For internal use."""
        result = self.headers()
        result['Content-Type'] = 'application/json'
        return result

    def session_url(self):
        """For internal use."""
        url = self.api_url + '/session/create'
        return url

    def archive_url(self, archive_id=None):
        """For internal use."""
        url = self.api_url + '/v2/partner/' + self.api_key + '/archive'
        if archive_id:
            url = url + '/' + archive_id
        return url

    def start_archive(self, session_id, has_audio=True, has_video=True, name=None, output_mode=OutputModes.composed):
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

        :rtype: The Archive object, which includes properties defining the archive,
          including the archive ID.
        """
        if not isinstance(output_mode, OutputModes):
            raise OpenTokException(u('Cannot start archive, {0} is not a valid output mode').format(output_mode))

        payload = {'name': name,
                   'sessionId': session_id,
                   'hasAudio': has_audio,
                   'hasVideo': has_video,
                   'outputMode': output_mode.value
        }

        response = requests.post(self.archive_url(), data=json.dumps(payload), headers=self.archive_headers(), proxies=self.proxies)

        if response.status_code < 300:
            return Archive(self, response.json())
        elif response.status_code == 403:
            raise AuthError()
        elif response.status_code == 400:
            raise RequestError("Session ID is invalid")
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
        response = requests.post(self.archive_url(archive_id) + '/stop', headers=self.archive_headers(), proxies=self.proxies)

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
        response = requests.delete(self.archive_url(archive_id), headers=self.archive_headers(), proxies=self.proxies)

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
        response = requests.get(self.archive_url(archive_id), headers=self.archive_headers(), proxies=self.proxies)

        if response.status_code < 300:
            return Archive(self, response.json())
        elif response.status_code == 403:
            raise AuthError()
        elif response.status_code == 404:
            raise NotFoundError("Archive not found")
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def get_archives(self, offset=None, count=None):
        """Returns an ArchiveList, which is an array of archives that are completed and in-progress,
        for your API key.

        :param int: offset Optional. The index offset of the first archive. 0 is offset
          of the most recently started archive. 1 is the offset of the archive that started prior to
          the most recent archive. If you do not specify an offset, 0 is used.
        :param int: count Optional. The number of archives to be returned. The maximum
          number of archives returned is 1000.

        :rtype: An ArchiveList object, which is an array of Archive objects.
        """
        params = {}
        if offset is not None:
            params['offset'] = offset
        if count is not None:
            params['count'] = count

        response = requests.get(self.archive_url() + "?" + urlencode(params), headers=self.archive_headers(), proxies=self.proxies)

        if response.status_code < 300:
            return ArchiveList(self, response.json())
        elif response.status_code == 403:
            raise AuthError()
        elif response.status_code == 404:
            raise NotFoundError("Archive not found")
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def _sign_string(self, string, secret):
        return hmac.new(secret.encode('utf-8'), string.encode('utf-8'), hashlib.sha1).hexdigest()
