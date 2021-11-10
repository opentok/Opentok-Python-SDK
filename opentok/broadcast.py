import json
from enum import Enum
from six import iteritems, u


class Broadcast(object):
    """
    Represents a live streaming broadcast.

    :ivar streamMode:
        Whether streams included in the broadcast are selected automatically
        ("auto", the default) or manually ("manual"). 
    
    :ivar streams:
        A list of streams currently being broadcast. This is only set for a broadcast with
        the status set to "started"  and the stream_Mode set to "manual".
    """

    def __init__(self, kwargs):
        self.id = kwargs.get("id")
        self.sessionId = kwargs.get("sessionId")
        self.projectId = kwargs.get("projectId")
        self.createdAt = kwargs.get("createdAt")
        self.updatedAt = kwargs.get("updatedAt")
        self.resolution = kwargs.get("resolution")
        self.status = kwargs.get("status")
        self.broadcastUrls = kwargs.get("broadcastUrls")
        self.stream_mode = kwargs.get("streamMode", BroadcastStreamModes.auto)
        self.streams = kwargs.get("streams")

    def json(self):
        """
        Returns a JSON representation of the broadcast
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class BroadcastStreamModes(Enum):
    """"List of valid settings for the stream_mode parameter of the OpenTok.start_broadcast()
    method."""

    auto = u("auto")
    """Streams are automatically added to broadcast."""
    manual = u("manual")
    """Streams are included in the broadcast based on calls to the OpenTok.add_broadcast_stream()
    and OpenTok.remove_broadcast_stream() methods."""
