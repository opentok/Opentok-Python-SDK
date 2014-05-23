from datetime import datetime, date
from six import iteritems, PY2, PY3, u
import json
import pytz
if PY3:
    from datetime import timezone

# compat
from six.moves import map

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime)  or isinstance(obj, date) else None

class Archive(object):
    """Represents an archive of an OpenTok session.

    :ivar created_at:
       The time at which the archive was created, in milliseconds since the UNIX epoch.

    :ivar duration:
       The duration of the archive, in milliseconds.

    :ivar id:
       The archive ID.

    :ivar name:
       The name of the archive. If no name was provided when the archive was created, this is set
       to null.

    :ivar partnerId:
       The API key associated with the archive.

    :ivar reason:
       For archives with the status "stopped", this can be set to "90 mins exceeded", "failure",
       "session ended", or "user initiated". For archives with the status "failed", this can be set
       to "system failure".

    :ivar sessionId:
       The session ID of the OpenTok session associated with this archive.

    :ivar size:
       The size of the MP4 file. For archives that have not been generated, this value is set to 0.

    :ivar status:
       The status of the archive, which can be one of the following:

       * "available" -- The archive is available for download from the OpenTok cloud.
       * "failed" -- The archive recording failed.
       * "started" -- The archive started and is in the process of being recorded.
       * "stopped" -- The archive stopped recording.
       * "uploaded" -- The archive is available for download from the the upload target
         S3 bucket.

    :ivar url:
       The download URL of the available MP4 file. This is only set for an archive with the status set to
       "available"; for other archives, (including archives with the status "uploaded") this property is
       set to null. The download URL is obfuscated, and the file is only available from the URL for
       10 minutes. To generate a new URL, call the Archive.listArchives() or OpenTok.getArchive() method.
    """

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
        """
        Stops an OpenTok archive that is being recorded.

        Archives automatically stop recording after 90 minutes or when all clients have disconnected
        from the session being archived.
        """
        temp_archive = self.sdk.stop_archive(self.id)
        for k,v in iteritems(temp_archive.attrs()):
            setattr(self, k, v)

    def delete(self):
        """
        Deletes an OpenTok archive.

        You can only delete an archive which has a status of "available" or "uploaded". Deleting an
        archive removes its record from the list of archives. For an "available" archive, it also
        removes the archive file, making it unavailable for download.
        """
        self.sdk.delete_archive(self.id)
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

class ArchiveList(object):

    def __init__(self, sdk, values):
        self.count = values.get('count')
        self.items = list(map(lambda x: Archive(sdk, x), values.get('items', [])))

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

    def __getitem__(self, key):
        return self.items.get(key)

    def __setitem__(self, key, item):
        raise ArchiveError(u('Cannot set item {0} for key {1} in Archive object').format(item, key))

    def __len__(self):
        return len(self.items)
