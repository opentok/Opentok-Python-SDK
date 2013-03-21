"""
OpenTok Python Library v0.91.0
http://www.tokbox.com/

Copyright 2011, TokBox, Inc.
"""


import urllib
import urllib2
import datetime
import calendar
import time
import hmac
import hashlib
import base64
import random


TIMEOUT = 10


class OpenTokException(BaseException):
    """Generic OpenTok Error. All other errors extend this."""
    pass


class RequestError(OpenTokException):
    """Indicates an error during the request. Most likely an error connecting to
    the OpenTok API servers. (HTTP 500 error).
    """
    pass


class AuthError(OpenTokException):
    """Indicates that the problem was likely with credentials. Check your API
    key and API secret and try again.
    """
    pass


class SessionProperties(object):
    echoSuppression_enabled = None
    multiplexer_numOutputStreams = None
    multiplexer_switchType = None
    multiplexer_switchTimeout = None
    p2p_preference = "p2p.preference" 

    def __iter__(self):
        d = {
            'echoSuppression.enabled': self.echoSuppression_enabled,
            'multiplexer.numOutputStreams': self.multiplexer_numOutputStreams,
            'multiplexer.switchType': self.multiplexer_switchType,
            'multiplexer.switchTimeout': self.multiplexer_switchTimeout,
            'p2p.preference': self.p2p_preference,
        }
        return d.iteritems()


class RoleConstants:
    """List of valid roles for a token."""
    SUBSCRIBER = 'subscriber' #Can only subscribe
    PUBLISHER = 'publisher'   #Can publish, subscribe, and signal
    MODERATOR = 'moderator'   #Can do the above along with  forceDisconnect and forceUnpublish


class OpenTokSession(object):

    def __init__(self, session_id):
        self.session_id = session_id

class OpenTokSDK(object):
    """Use this SDK to create tokens and interface with the server-side portion
    of the Opentok API.
    """
    TOKEN_SENTINEL = 'T1=='
    API_URL = 'http://api.opentok.com'

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret.strip()

    def generate_token(self, session_id=None, role=None, expire_time=None, connection_data=None, **kwargs):
        """
        Generate a token which is passed to the JS API to enable widgets to connect to the Opentok api.
        session_id: Specify a session_id to make this token only valid for that session_id.
        role: One of the constants defined in RoleConstants. Default is publisher, look in the documentation to learn more about roles.
        expire_time: Integer timestamp. You can override the default token expire time of 24h by choosing an explicit expire time. Can be up to 7d after create_time.
        """
        create_time = datetime.datetime.utcnow()
        if session_id is None:
            session_id = ''
        if not role:
            role = RoleConstants.PUBLISHER

        if role != RoleConstants.SUBSCRIBER and \
                role != RoleConstants.PUBLISHER and \
                role != RoleConstants.MODERATOR:
            raise OpenTokException('%s is not a valid role' % role)

        data_params = dict(
            session_id=session_id,
            create_time=calendar.timegm(create_time.timetuple()),
            role=role,
        )
        if expire_time is not None:
            if isinstance(expire_time, datetime.datetime):
                data_params['expire_time'] = calendar.timegm(expire_time.timetuple())
            else:
                try:
                    data_params['expire_time'] = int(expire_time)
                except (ValueError, TypeError):
                    raise OpenTokException('Expire time must be a number')

            if data_params['expire_time'] < time.time():
                raise OpenTokException('Expire time must be in the future')

            if data_params['expire_time'] > time.time() + 2592000:
                raise OpenTokException('Expire time must be in the next 30 days')

        if connection_data is not None:
            if len(connection_data) > 1000:
                raise OpenTokException('Connection data must be less than 1000 characters')
            data_params['connection_data'] = connection_data

        data_params['nonce'] = random.randint(0,999999)
        data_string = urllib.urlencode(data_params, True)

        sig = self._sign_string(data_string, self.api_secret)
        token_string = '%s%s' % (self.TOKEN_SENTINEL, base64.b64encode('partner_id=%s&sig=%s:%s' % (self.api_key, sig, data_string)))
        return token_string

    def create_session(self, location='', properties={}, **kwargs):
        """Create a new session in the OpenTok API. Returns an OpenTokSession
        object with a session_id property. location: IP address of the user
        requesting the session. This is used for geolocation to choose which
        datacenter the session will live on. properties: An instance of the
        SessionProperties object. Fill in the fields that you are interested in
        to use features of the groups API. Look in the documentation for more
        details. Also accepts any dict-like object.
        """
        #ip_passthru is a deprecated argument and has been replaced with location
        if 'ip_passthru' in kwargs:
            location = kwargs['ip_passthru']
        params = dict(api_key=self.api_key)
        params['location'] = location
        params.update(properties)
        dom = ''
        try:
            dom = self._do_request('/session/create', params)
        except RequestError:
            raise
        except Exception, e:
            raise RequestError('Failed to create session: %s' % str(e)  )

        try:
            error = dom.getElementsByTagName('error')
            if error:
                error = error[0]
                raise AuthError('Failed to create session (code=%s): %s' % (error.attributes['code'].value, error.firstChild.attributes['message'].value))

            session_id = dom.getElementsByTagName('session_id')[0].childNodes[0].nodeValue
            return OpenTokSession(session_id)
        except Exception, e:
            raise OpenTokException('Failed to generate session: %s' % str(e))


    def _sign_string(self, string, secret):
        return hmac.new(secret, string.encode('utf-8'), hashlib.sha1).hexdigest()

    def _do_request(self, url, params):
        import xml.dom.minidom as xmldom

        if '_token' in params: #Do token auth if _token is present, partner auth normally
            auth_header = ('X-TB-TOKEN-AUTH', params['_token'])
            del params['_token']
        else:
            auth_header = ('X-TB-PARTNER-AUTH', '%s:%s' % (self.api_key, self.api_secret))

        method = 'POST' if params else 'GET'
        data_string = urllib.urlencode(params, True)

        context_source = [
            ('method', method),
            ('Content-Type', 'application/x-www-form-urlencoded'),
            ('Content-Length', len(data_string)),
            auth_header
        ]

        req_string = self.API_URL + url
        try:
            opener = urllib2.build_opener()
            opener.addheaders = context_source
            if data_string:
                request = urllib2.Request(url=req_string, data=data_string)
            else: #GET if no data_string
                request = urllib2.Request(url=req_string)
            try:
                response = opener.open(request, timeout=TIMEOUT)
            except TypeError: #Python2.6 added the timeout keyword, if it doesn't get accepted, try without it
                response = opener.open(request)

            dom = xmldom.parseString(response.read())
            response.close()
        except urllib2.HTTPError, e:
            raise RequestError('Failed to send request: %s' % str(e))

        return dom
