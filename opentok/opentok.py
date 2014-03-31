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
from .archives import Archive, ArchiveList
from .exceptions import OpenTokException, RequestError, AuthError, NotFoundError, ArchiveError

class Roles(Enum):
    """List of valid roles for a token."""
    subscriber = u('subscriber')   # Can only subscribe
    publisher =  u('publisher')    # Can publish, subscribe, and signal
    moderator =  u('moderator')    # Can do the above along with forceDisconnect and forceUnpublish

class OpenTok(object):
    """Use this SDK to create tokens and interface with the server-side portion
    of the Opentok API.
    """
    TOKEN_SENTINEL = 'T1=='

    def __init__(self, api_key, api_secret, api_url='https://api.opentok.com'):
        self.api_key = str(api_key)
        self.api_secret = api_secret
        self.api_url = api_url

    def generate_token(self, session_id, role=Roles.publisher, expire_time=None, connection_data=None, **kwargs):
        """
        Generate a token which is passed to the JS API to enable widgets to connect to the Opentok api.
        session_id: Specify a session_id to make this token only valid for that session_id.
        role: One of the constants defined in RoleConstants. Default is publisher, look in the documentation to learn more about roles.
        expire_time: Integer timestamp. You can override the default token expire time of 24h by choosing an explicit expire time. Can be up to 7d after create_time.
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
        if (connection_data is not None) and len(connection_data) > 1000:
            raise OpenTokException(u('Cannot generate token, connection_data must be less than 1000 characters').format(connection_data))

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
            connection_data = (connection_data or None),
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

    def create_session(self, location=None, p2p=False):
        """Create a new session in the OpenTok API. Returns an OpenTokSession
        object with a session_id property. location: IP address of the user
        requesting the session. This is used for geolocation to choose which
        datacenter the session will live on. properties: An instance of the
        SessionProperties object. Fill in the fields that you are interested in
        to use features of the groups API. Look in the documentation for more
        details. Also accepts any dict-like object.
        """

        # build options
        options = {}
        if p2p:
            if not isinstance(p2p, bool):
                raise OpenTokException(u('Cannot create session. p2p must be a bool {0}').format(p2p))
            options[u('p2p.preference')] = u('enabled')
        if location:
            # validate IP address
            try:
                inet_aton(location)
            except:
                raise OpenTokException(u('Cannot create session. Location must be either None or a valid IPv4 address {0}').format(location))
            options[u('location')] = location

        try:
            response = requests.post(self.session_url(), data=options, headers=self.headers())
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
            return Session(session_id, location=location, p2p=p2p)
        except Exception as e:
            raise OpenTokException('Failed to generate session: %s' % str(e))

    def headers(self):
        return {
            'User-Agent': 'OpenTok-Python-SDK/' + __version__,
            'X-TB-PARTNER-AUTH': self.api_key + ':' + self.api_secret
        }

    def archive_headers(self):
        result = self.headers()
        result['Content-Type'] = 'application/json'
        return result

    def session_url(self):
        url = self.api_url + '/session/create'
        return url

    def archive_url(self, archive_id=None):
        url = self.api_url + '/v2/partner/' + self.api_key + '/archive'
        if archive_id:
            url = url + '/' + archive_id
        return url

    def start_archive(self, session_id, **kwargs):
        payload = {'name': kwargs.get('name'), 'sessionId': session_id}

        response = requests.post(self.archive_url(), data=json.dumps(payload), headers=self.archive_headers())

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
        response = requests.post(self.archive_url(archive_id) + '/stop', headers=self.archive_headers())

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
        response = requests.delete(self.archive_url(archive_id), headers=self.archive_headers())

        if response.status_code < 300:
            pass
        elif response.status_code == 403:
            raise AuthError()
        elif response.status_code == 404:
            raise NotFoundError("Archive not found")
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def get_archive(self, archive_id):
        response = requests.get(self.archive_url(archive_id), headers=self.archive_headers())

        if response.status_code < 300:
            return Archive(self, response.json())
        elif response.status_code == 403:
            raise AuthError()
        elif response.status_code == 404:
            raise NotFoundError("Archive not found")
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def get_archives(self, offset=None, count=None):
        params = {}
        if offset is not None:
            params['offset'] = offset
        if count is not None:
            params['count'] = count

        response = requests.get(self.archive_url() + "?" + urlencode(params), headers=self.archive_headers())

        if response.status_code < 300:
            return ArchiveList(response.json())
        elif response.status_code == 403:
            raise AuthError()
        elif response.status_code == 404:
            raise NotFoundError("Archive not found")
        else:
            raise RequestError("An unexpected error occurred", response.status_code)

    def _sign_string(self, string, secret):
        return hmac.new(secret.encode('utf-8'), string.encode('utf-8'), hashlib.sha1).hexdigest()

