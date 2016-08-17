import unittest
from six import text_type, u, b, PY2, PY3
from mock import MagicMock
from expects import *
import datetime
import pytz
from .validate_jwt import validate_jwt_header

from opentok import OpenTok, Callback, __version__

class OpenTokCallbackTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        self.opentok = OpenTok(self.api_key, self.api_secret)

    def test_unregister_callback(self):
        callback_id = u('CALLBACKID')
        callback = Callback(self.opentok, {
            u('createdAt'): 1395183243556,
            u('id'): callback_id,
            u('group'): u('GROUP'),
            u('event'): u('EVENT'),
            u('url'): u('URL'),
        })

        expect(callback).to.have.property(u('id')).being.equal(callback_id)
        expect(callback).to.have.property(u('group')).being.equal(u('GROUP'))
        expect(callback).to.have.property(u('event')).being.equal(u('EVENT'))
        expect(callback).to.have.property(u('url')).being.equal(u('URL'))
        if PY2:
            created_at = datetime.datetime.fromtimestamp(1395183243, pytz.UTC)
        if PY3:
            created_at = datetime.datetime.fromtimestamp(1395183243, datetime.timezone.utc)
        expect(callback).to.have.property(u('created_at')).being.equal(created_at)

        self.opentok.unregister_callback = MagicMock()
        callback.unregister()
        self.opentok.unregister_callback.assert_called_with(callback_id)
