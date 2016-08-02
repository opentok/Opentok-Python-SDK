from datetime import datetime, date
from six import iteritems, PY2, PY3, u
import json
import pytz
from enum import Enum
if PY3:
    from datetime import timezone

# compat
from six.moves import map

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime)  or isinstance(obj, date) else None

class Callback(object):
    """Represents an callback registered in OpenTok.

    :ivar created_at:
       The time at which the archive was created, in milliseconds since the UNIX epoch.

    :ivar id:
       The callback ID.

    :ivar group:
       The group of events this callback is registered for.

    :ivar event:
       The event this callback is registered for.

    :ivar url:
       The registered callback URL.
    """

    def __init__(self, sdk, values):
        self.sdk = sdk
        self.id = values.get('id')
        if PY2:
            self.created_at = datetime.fromtimestamp(values.get('createdAt') / 1000, pytz.UTC)
        if PY3:
            self.created_at = datetime.fromtimestamp(values.get('createdAt') // 1000, timezone.utc)
        self.group = values.get('group')
        self.event = values.get('event')
        self.url = values.get('url')

    def unregister(self):
        """
        Unregisters an OpenTok callback.
        """
        self.sdk.unregister_callback(self.id)
        # TODO: invalidate this object

    def attrs(self):
        """
        Returns a dictionary of the archive's attributes.
        """
        return dict((k, v) for k, v in iteritems(self.__dict__) if k is not "sdk")

    def json(self):
        """
        Returns a JSON representation of the archive.
        """
        return json.dumps(self.attrs(), default=dthandler, indent=4)

class CallbackList(object):

    def __init__(self, sdk, values):
        self.items = list(map(lambda x: Callback(sdk, x), values))

    def __iter__(self):
        for x in self.items:
            yield x

    def attrs(self):
        return map(Callback.attrs, self.items)

    def json(self):
        return json.dumps(self.attrs(), default=dthandler, indent=4)

    def __len__(self):
        return len(self.items)
