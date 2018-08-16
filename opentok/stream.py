from datetime import datetime, date
from six import iteritems, PY2, PY3, u
import json
from six.moves import map
dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime)  or isinstance(obj, date) else None

from .exceptions import GetStreamError

class Stream(object):
    """
    Represents an OpenTok stream
    """

    def __init__(self, kwargs):
        self.id = kwargs.get('id')
        self.videoType = kwargs.get('videoType')
        self.name = kwargs.get('name')
        self.layoutClassList = kwargs.get('layoutClassList')

    def attrs(self):
        """
        Returns a dictionary of the Stream's attributes.
        """
        return dict((k, v) for k, v in iteritems(self.__dict__))

    def json(self):
        """
        Returns a JSON representation of the Stream.
        """
        return json.dumps(self.attrs(), default=dthandler, indent=4)

class StreamList(object):
    """
    Represents a list of OpenTok stream objects
    """

    def __init__(self, values):
        self.count = values.get('count')
        self.items = list(map(lambda x: Stream(x), values.get('items', [])))

    def __iter__(self):
        for x in self.items:
            yield x

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __getitem__(self, key):
        return self.items.get(key)

    def __setitem__(self, key, item):
        raise GetStreamError(u('Cannot set item {0} for key {1} in Archive object').format(item, key))

    def __len__(self):
        return len(self.items)
