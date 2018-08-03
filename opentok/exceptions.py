class OpenTokException(Exception):
    """Defines exceptions thrown by the OpenTok SDK.
    """
    pass


class RequestError(OpenTokException):
    """Indicates an error during the request. Most likely an error connecting
    to the OpenTok API servers. (HTTP 500 error).
    """
    pass


class AuthError(OpenTokException):
    """Indicates that the problem was likely with credentials. Check your API
    key and API secret and try again.
    """
    pass


class NotFoundError(OpenTokException):
    """Indicates that the element requested was not found.  Check the parameters
    of the request.
    """
    pass


class ArchiveError(OpenTokException):
    """Indicates that there was a archive specific problem, probably the status
    of the requested archive is invalid.
    """
    pass

class SignalingError(OpenTokException):
    """Indicates that there was a signaling specific problem, one of the parameter
    is invalid or the type|data string doesn't have a correct size"""
    pass

class GetStreamError(OpenTokException):
    """Indicates that the data in the request is invalid, or the session_id or stream_id
    are invalid"""
    pass

class ForceDisconnectError(OpenTokException):
    """
    Indicates that there was a force disconnect specific problem:
    One of the arguments is invalid or the client specified by the connectionId property
    is not connected to the session
    """
    pass
