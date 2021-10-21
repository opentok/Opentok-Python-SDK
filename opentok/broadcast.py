import json
from enum import Enum
from opentok.archives import StreamModes
from six import iteritems, u


class Broadcast(object):
    """
    Represents a live streaming broadcast

    :ivar streamMode:
        Determines the broadcast stream handling mode. It's set to 'auto' by
        default if you want all streams. To explicitly select specific streams 
        in the broadcast then set to 'manual'.
    
    :ivar streams:
        A list of streams in a broadcast.
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
    """"List of valid settings for the stream_mode parameter of the OpenTok.start_broadcast()"""

    auto = u("auto")
    """Streams will automatically be selected and added to broadcase"""
    manual = u("manual")
    """Customers select which streams get added to broadcast"""