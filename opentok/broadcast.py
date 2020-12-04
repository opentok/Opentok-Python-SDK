import json


class Broadcast(object):
    """
    Represents a live streaming broadcast
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

    def json(self):
        """
        Returns a JSON representation of the broadcast
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
