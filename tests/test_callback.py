import unittest
from six import text_type, u, b, PY2, PY3
from nose.tools import raises
from mock import MagicMock
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
        })

        self.opentok.unregister_callback = MagicMock()
        callback.unregister()
        self.opentok.unregister_callback.assert_called_with(callback_id)


