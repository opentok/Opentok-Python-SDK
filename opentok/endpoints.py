import warnings


class Endpoints(object):
    """
    For internal use.
    Class that provides the endpoint urls
    """

    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def get_session_url(self):
        url = self.api_url + "/session/create"
        return url

    def session_url(self):
        warnings.warn(
            "endpoints.session_url is deprecated (use endpoints.get_session_url instead).",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.get_session_url()

    def get_archive_url(self, archive_id=None):
        url = self.api_url + "/v2/project/" + self.api_key + "/archive"
        if archive_id:
            url = url + "/" + archive_id
        return url

    def archive_url(self, archive_id=None):
        warnings.warn(
            "endpoints.archive_url is deprecated (use endpoints.get_archive_url instead).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_archive_url(archive_id)

    def get_signaling_url(self, session_id, connection_id=None):
        url = self.api_url + "/v2/project/" + self.api_key + "/session/" + session_id

        if connection_id:
            url += "/connection/" + connection_id

        url += "/signal"
        return url

    def signaling_url(self, session_id, connection_id=None):
        warnings.warn(
            "endpoints.signaling_url is deprecated (use endpoints.get_signaling_url instead).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_signaling_url(session_id, connection_id)

    def get_stream_url(self, session_id, stream_id=None):
        """ this method returns the url to get streams information """
        url = (
            self.api_url
            + "/v2/project/"
            + self.api_key
            + "/session/"
            + session_id
            + "/stream"
        )
        if stream_id:
            url = url + "/" + stream_id
        return url

    def broadcast_url(self, broadcast_id=None, stop=False, layout=False):
        warnings.warn(
            "endpoints.broadcast_url is deprecated (use endpoints.get_broadcast_url instead).",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_broadcast_url(broadcast_id, stop, layout)

    def force_disconnect_url(self, session_id, connection_id):
        """ this method returns the force disconnect url endpoint """
        url = (
            self.api_url
            + "/v2/project/"
            + self.api_key
            + "/session/"
            + session_id
            + "/connection/"
            + connection_id
        )
        return url

    def set_archive_layout_url(self, archive_id):
        """ this method returns the url to set the archive layout """
        url = (
            self.api_url
            + "/v2/project/"
            + self.api_key
            + "/archive/"
            + archive_id
            + "/layout"
        )
        return url

    def dial_url(self):
        """ this method returns the url to initialize a SIP call """
        url = self.api_url + "/v2/project/" + self.api_key + "/dial"
        return url

    def set_stream_class_lists_url(self, session_id):
        """ this method returns the url to set the stream class list """
        url = (
            self.api_url
            + "/v2/project/"
            + self.api_key
            + "/session/"
            + session_id
            + "/stream"
        )
        return url

    def get_broadcast_url(self, broadcast_id=None, stop=False, layout=False):
        """ this method returns urls for working with broadcast """
        url = self.api_url + "/v2/project/" + self.api_key + "/broadcast"

        if broadcast_id:
            url = url + "/" + broadcast_id
        if stop:
            url = url + "/stop"
        if layout:
            url = url + "/layout"
        return url
