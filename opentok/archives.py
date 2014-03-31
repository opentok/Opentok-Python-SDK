from datetime import datetime, date
from six import iteritems, PY2, PY3
import json
import pytz
if PY3:
    from datetime import timezone

# compat
from six.moves import map

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime)  or isinstance(obj, date) else None

class Archive(object):

    def __init__(self, sdk, values):
        self.sdk = sdk
        self.id = values.get('id')
        self.name = values.get('name')
        self.status = values.get('status')
        self.session_id = values.get('sessionId')
        self.partner_id = values.get('partnerId')
        if PY2:
            self.created_at = datetime.fromtimestamp(values.get('createdAt') / 1000, pytz.UTC)
        if PY3:
            self.created_at = datetime.fromtimestamp(values.get('createdAt') // 1000, timezone.utc)
        self.size = values.get('size')
        self.duration = values.get('duration')
        self.url = values.get('url')

    def stop(self):
        temp_archive = self.sdk.stop_archive(self.id)
        for k,v in iteritems(temp_archive.attrs()):
            setattr(self, k, v)

    def delete(self):
        self.sdk.delete_archive(self.id)
        # TODO: invalidate this object

    def attrs(self):
        return dict((k, v) for k, v in iteritems(self.__dict__) if k is not "sdk")

    def json(self):
        return json.dumps(self.attrs(), default=dthandler, indent=4)

class ArchiveList(object):

    def __init__(self, values):
        self.count = values.get('count')
        self.items = map(lambda x: Archive(self, x), values.get('items', []))

    def __iter__(self):
        for x in self.items:
            yield x

    def attrs(self):
        return {
            'count': self.count,
            'items': map(Archive.attrs, self.items)
        }

    def json(self):
        return json.dumps(self.attrs(), default=dthandler, indent=4)


