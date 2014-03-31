from datetime import datetime, date
from six import iteritems
import json

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime)  or isinstance(obj, date) else None

class Archive(object):

    def __init__(self, sdk, values):
        self.sdk = sdk
        self.id = values.get('id')
        self.name = values.get('name')
        self.status = values.get('status')
        self.session_id = values.get('sessionId')
        self.partner_id = values.get('partnerId')
        self.created_at = datetime.fromtimestamp(values.get('createdAt') / 1000)
        self.size = values.get('size')
        self.duration = values.get('duration')
        self.url = values.get('url')

    def stop(self):
        self.sdk.stop_archive(self.id)

    def delete(self):
        self.sdk.delete_archive(self.id)

    def attrs(self):
        return dict((k, v) for k, v in iteritems(self.__dict__) if k is not "sdk")

    def json(self):
        return json.dumps(self.attrs(), default=dthandler, indent=4)

class ArchiveList(object):

    def __init__(self, values):
        self.count = values.get('count')
        self.items = map(lambda x: OpenTokArchive(self, x), values.get('items', []))

    def __iter__(self):
        for x in self.items:
            yield x

    def attrs(self):
        return {
            'count': self.count,
            'items': map(OpenTokArchive.attrs, self.items)
        }

    def json(self):
        return json.dumps(self.attrs(), default=dthandler, indent=4)


