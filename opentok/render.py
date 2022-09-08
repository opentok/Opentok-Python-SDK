import json

class Render:
    """Represents a render of an OpenTok session."""

    def __init__(self, kwargs):
        self.id = kwargs.get("id")
        self.sessionId = kwargs.get("sessionId")
        self.projectId = kwargs.get("projectId")
        self.createdAt = kwargs.get("createdAt")
        self.updatedAt = kwargs.get("updatedAt")
        self.url = kwargs.get("url")
        self.resolution = kwargs.get("resolution")
        self.status = kwargs.get("status")
        self.streamId = kwargs.get("streamId") or None
        self.reason = kwargs.get("reason") or None

    def json(self):
        """Returns a JSON representation of the render."""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
