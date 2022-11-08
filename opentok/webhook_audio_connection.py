import json
from six import iteritems

class WebhookAudioConnection:
    """Represents information about the audio streaming of an OpenTok session to a webhook."""

    def __init__(self, kwargs):
        self.id = kwargs.get("id")
        self.connectionId = kwargs.get("connectionId")

    def json(self):
        """Returns a JSON representation of the webhook audio connection information."""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def attrs(self):
        """
        Returns a dictionary of the webhook audio connection's attributes.
        """
        return dict((k, v) for k, v in iteritems(self.__dict__))
        