class Endpoint(object):
    """
    For internal use.
    Class that provides the endpoint urls
    """
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def session_url(self):
        url = self.api_url + '/session/create'
        return url

    def archive_url(self, archive_id=None):
        url = self.api_url + '/v2/project/' + self.api_key + '/archive'
        if archive_id:
            url = url + '/' + archive_id
        return url

    def signaling_url(self, session_id, connection_id=None):
        url = self.api_url + '/v2/project/' + self.api_key + '/session/' + session_id

        if connection_id:
            url += '/connection/' + connection_id

        url += '/signal'
        return url

    def get_stream_url(self, session_id, stream_id):
        url = self.api_url + '/v2/project/' + self.api_key + '/session/' + session_id + '/stream/' + stream_id
        return url

