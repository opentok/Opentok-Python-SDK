class OpenTokException(BaseException):
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
