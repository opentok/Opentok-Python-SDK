import time
import urllib2
import unittest
from xml.dom.minidom import parseString

from OpenTokSDK import OpenTokSDK, OpenTokException


class TestPythonSDK(unittest.TestCase):

    api_key = -1
    api_secret = ""
    api_url = OpenTokSDK.STAGING_URL
    o = None

    def setUp(self):
        self.o = OpenTokSDK(self.api_key, self.api_secret)

    def test_create_session(self):
        s = self.o.create_session()
        self.assertIsNotNone(s.session_id, "Python SDK tests: create session (no params): did not return a session id")
        xml = self.get_session_info(s.session_id)
        self.assertEqual(s.session_id, xml.getElementsByTagName('session_id')[0].childNodes[0].data, \
            "Python SDK tests: Session id not found")

        s = self.o.create_session('216.38.134.114')
        self.assertIsNotNone(s.session_id, "Python SDK tests: create session (no params): did not return a session id")
        xml = self.get_session_info(s.session_id)
        self.assertEqual(s.session_id, xml.getElementsByTagName('session_id')[0].childNodes[0].data, \
            "Python SDK tests: Session id not found")

    def test_num_output_streams(self):
        s = self.o.create_session('127.0.0.1', properties={"multiplexer.numOutputStreams": 0})
        xml = self.get_session_info(s.session_id)
        self.assertEqual('0', xml.getElementsByTagName('numOutputStreams')[0].childNodes[0].data, \
            'Python SDK tests: multiplexer.numOutputStreams not set to 0')

        s = self.o.create_session('127.0.0.1', properties = {"multiplexer.numOutputStreams": 1})
        xml = self.get_session_info(s.session_id)
        self.assertEqual('1', xml.getElementsByTagName('numOutputStreams')[0].childNodes[0].data, \
            'Python SDK tests: multiplexer.numOutputStreams not set to 1')

        s = self.o.create_session('127.0.0.1', properties = {"multiplexer.numOutputStreams": 5})
        xml = self.get_session_info(s.session_id)
        self.assertEqual('5', xml.getElementsByTagName('numOutputStreams')[0].childNodes[0].data, \
            'Python SDK tests: multiplexer.numOutputStreams not set to 5')

        s = self.o.create_session('127.0.0.1', properties = {"multiplexer.numOutputStreams": 100})
        xml = self.get_session_info(s.session_id)
        self.assertEqual('100', xml.getElementsByTagName('numOutputStreams')[0].childNodes[0].data, \
            'Python SDK tests: multiplexer.numOutputStreams not set to 100')

        s = self.o.create_session('127.0.0.1')
        xml = self.get_session_info(s.session_id)
        self.assertEqual([], xml.getElementsByTagName('numOutputStreams'),
            'Python SDK tests: multiplexer.numOutputStreams should not be set')

    def test_switch_type(self):
        s = self.o.create_session(properties = {"multiplexer.switchType":  0})
        xml = self.get_session_info(s.session_id)
        self.assertEqual('0', xml.getElementsByTagName('switchType')[0].childNodes[0].data, \
            'Python SDK tests: multiplexer.switchType not 0')

        s = self.o.create_session(properties = {"multiplexer.switchType":  1})
        xml = self.get_session_info(s.session_id)
        self.assertEqual('1', xml.getElementsByTagName('switchType')[0].childNodes[0].data, \
            'Python SDK tests: multiplexer.switchType not 1')

        s = self.o.create_session()
        xml = self.get_session_info(s.session_id)
        self.assertEqual([], xml.getElementsByTagName('switchType'),
            'Python SDK tests: multiplexer.switchType should not be set')

    def test_switch_timeout(self):
        s = self.o.create_session(properties = {"multiplexer.switchTimeout": 1200})
        xml = self.get_session_info(s.session_id)
        self.assertEqual('1200', xml.getElementsByTagName('switchTimeout')[0].childNodes[0].data, \
            'Python SDK tests: multiplexer.switchTimeout not properly set (should be 1200)')

        s = self.o.create_session(properties = {"multiplexer.switchTimeout": 2000})
        xml = self.get_session_info(s.session_id)
        self.assertEqual('2000', xml.getElementsByTagName('switchTimeout')[0].childNodes[0].data, \
            'Python SDK tests: multiplexer.switchTimeout not properly set (should be 2000)')

        s = self.o.create_session(properties = {"multiplexer.switchTimeout": 100000})
        xml = self.get_session_info(s.session_id)
        self.assertEqual('100000', xml.getElementsByTagName('switchTimeout')[0].childNodes[0].data, \
            'Python SDK tests: multiplexer.switchType not properly set (should be 100000)')

    def test_p2p_preference(self):
        s = self.o.create_session(properties = {"p2p.preference": 'enabled'})
        xml = self.get_session_info(s.session_id)
        self.assertEqual('enabled', xml.getElementsByTagName('preference')[0].childNodes[0].data, \
            'Python SDK tests: multiplexer.p2p_preference not enabled')

        s = self.o.create_session(properties = {"p2p.preference": 'disabled'})
        xml = self.get_session_info(s.session_id)
        self.assertEqual('disabled', xml.getElementsByTagName('preference')[0].childNodes[0].data, \
            'Python SDK tests: multiplexer.p2p_preference not disabled')

    def test_echo_suppression(self):
        s = self.o.create_session(properties = {"echoSuppression.enabled": 'true'})
        xml = self.get_session_info(s.session_id)
        self.assertEqual('True', xml.getElementsByTagName('enabled')[0].childNodes[0].data, \
            'Python SDK tests: echo suppression not showing enabled')

        s = self.o.create_session(properties = {"echoSuppression.enabled": 'false'})
        xml = self.get_session_info(s.session_id)
        self.assertEqual('False', xml.getElementsByTagName('enabled')[0].childNodes[0].data, \
            'Python SDK tests: echo suppression not showing disabled')

    def test_roles(self):
        s = self.o.create_session()

        # default: publisher
        t = self.o.generate_token(s.session_id)
        xml = self.get_token_info(t)
        role = xml.getElementsByTagName('role')[0].childNodes[0].data
        role = role.strip()
        self.assertEqual('publisher', role, 'Python SDK tests: default role not publisher')
        self.assertNotEqual([], xml.getElementsByTagName('subscribe'), \
            'Python SDK tests: token default permissions should include subscribe')
        self.assertNotEqual([], xml.getElementsByTagName('publish'), \
            'Python SDK tests: token default permissions should include publish')
        self.assertNotEqual([], xml.getElementsByTagName('signal'), \
            'Python SDK tests: token default permissions should include signal')
        self.assertEqual([], xml.getElementsByTagName('forceunpublish'), \
            'Python SDK tests: token default permissions should include forceunpublish')
        self.assertEqual([], xml.getElementsByTagName('forcedisconnect'), \
            'Python SDK tests: token default permissions should include forcedisconnect')
        self.assertEqual([], xml.getElementsByTagName('record'), \
            'Python SDK tests: token default permissions should include record')
        self.assertEqual([], xml.getElementsByTagName('playback'), \
            'Python SDK tests: token default permissions should include playback')

        # publisher
        t = self.o.generate_token(s.session_id, "publisher")
        xml = self.get_token_info(t)
        role = xml.getElementsByTagName('role')[0].childNodes[0].data
        role = role.strip()
        self.assertEqual('publisher', role, 'Python SDK tests: role not publisher')
        self.assertNotEqual([], xml.getElementsByTagName('subscribe'), \
            'Python SDK tests: token publisher permissions should include subscribe')
        self.assertNotEqual([], xml.getElementsByTagName('publish'), \
            'Python SDK tests: token publisher permissions should include publish')
        self.assertNotEqual([], xml.getElementsByTagName('signal'), \
            'Python SDK tests: token publisher permissions should include signal')
        self.assertEqual([], xml.getElementsByTagName('forceunpublish'), \
            'Python SDK tests: token publisher permissions should not include forceunpublish')
        self.assertEqual([], xml.getElementsByTagName('forcedisconnect'), \
            'Python SDK tests: token publisher permissions should not include forcedisconnect')
        self.assertEqual([], xml.getElementsByTagName('record'), \
            'Python SDK tests: token publisher permissions should not include record')
        self.assertEqual([], xml.getElementsByTagName('playback'), \
            'Python SDK tests: token publisher permissions should not include playback')

        # moderator
        t = self.o.generate_token(s.session_id, "moderator")
        xml = self.get_token_info(t)
        role = xml.getElementsByTagName('role')[0].childNodes[0].data
        role = role.strip()
        self.assertEqual('moderator', role, 'Python SDK tests: role not moderator')
        self.assertNotEqual([], xml.getElementsByTagName('subscribe'), \
            'Python SDK tests: token moderator permissions should include subscribe')
        self.assertNotEqual([], xml.getElementsByTagName('publish'), \
            'Python SDK tests: token moderator permissions should include publish')
        self.assertNotEqual([], xml.getElementsByTagName('signal'), \
            'Python SDK tests: token moderator permissions should include signal')
        self.assertNotEqual([], xml.getElementsByTagName('forceunpublish'), \
            'Python SDK tests: token moderator permissions should include forceunpublish')
        self.assertNotEqual([], xml.getElementsByTagName('forcedisconnect'), \
            'Python SDK tests: token moderator permissions should include forcedisconnect')
        self.assertNotEqual([], xml.getElementsByTagName('record'), \
            'Python SDK tests: token moderator permissions should include record')
        self.assertNotEqual([], xml.getElementsByTagName('playback'), \
            'Python SDK tests: token moderator permissions should include playback')

        # subscriber
        t = self.o.generate_token(s.session_id, "subscriber")
        xml = self.get_token_info(t)
        role = xml.getElementsByTagName('role')[0].childNodes[0].data
        role = role.strip()
        self.assertEqual('subscriber', role, 'Python SDK tests: role not subscriber')
        self.assertNotEqual([], xml.getElementsByTagName('subscribe'), \
            'Python SDK tests: token subscriber permissions should include subscribe')
        self.assertEqual([], xml.getElementsByTagName('publish'), \
            'Python SDK tests: token subscriber permissions should not include publish')
        self.assertEqual([], xml.getElementsByTagName('signal'), \
            'Python SDK tests: token subscriber permissions should not include signal')
        self.assertEqual([], xml.getElementsByTagName('forceunpublish'), \
            'Python SDK tests: token subscriber permissions should not include forceunpublish')
        self.assertEqual([], xml.getElementsByTagName('forcedisconnect'), \
            'Python SDK tests: token subscriber permissions should not include forcedisconnect')
        self.assertEqual([], xml.getElementsByTagName('record'), \
            'Python SDK tests: token subscriber permissions should not include record')
        self.assertEqual([], xml.getElementsByTagName('playback'), \
            'Python SDK tests: token subscriber permissions should not include playback')

        # garbage data
        try:
            t = self.o.generate_token(s.session_id, 'ads')
            raise AssertionError('Python SDK tests: invalid role should be rejected')

        except OpenTokException:
            pass # expected

    def test_old_session(self):
        s_id = '1abc70a34d069d2e6a1e565f3958b5250b435e32'
        t = self.o.generate_token(s_id)
        xml = self.get_token_info(t)
        self.assertEqual(s_id, xml.getElementsByTagName('session_id')[0].childNodes[0].data, \
            'Python SDK test: creating token with old session id failed')

    def test_expire_time(self):
        s = self.o.create_session()

        # past
        tm = time.time() - 1000
        try:
            t = self.o.generate_token(s.session_id, expire_time=tm)
            raise AssertionError('Python SDK tests: expire time in past should be rejected')
        except OpenTokException:
            pass

        # near future
        tm = time.time() + 6 * 24 * 60 * 60
        t = self.o.generate_token(s.session_id, expire_time=tm)
        xml = self.get_token_info(t)
        self.assertEqual(str(int(tm)), xml.getElementsByTagName('expire_time')[0].childNodes[0].data,\
            'Python SDK tests: expire time not set')

        # far future
        tm = time.time() + 8 * 24 * 60 * 60
        try:
            t = self.o.generate_token(s.session_id, expire_time=tm)
            raise AssertionError('Python SDK tests: expire time more than 7 days away should be rejected')
        except OpenTokException:
            pass

        # garbage data
        try:
            t = self.o.generate_token(s.session_id, expire_time="asdf")
            raise AssertionError('Python SDK tests: non numberic expire time should be rejected')
        except OpenTokException:
            pass

    def test_connection_data(self):
        s = self.o.create_session()

        test_string = 'test data'
        t = self.o.generate_token(s.session_id, connection_data=test_string)
        xml = self.get_token_info(t)
        self.assertEqual(test_string, xml.getElementsByTagName('connection_data')[0].childNodes[0].data,\
            'Python SDK tests: connection data not correct')

        # Should reject over 1000 characters of connection data
        test_string = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' + \
            'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb' + \
            'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc' + \
            'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd' + \
            'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee' + \
            'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee' + \
            'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' + \
            'gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg' + \
            'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh' + \
            'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii' + \
            'jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj' + \
            'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk' + \
            'llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll' + \
            'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm' + \
            'nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn' + \
            'oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'
        try:
            t = self.o.generate_token(s.session_id, connection_data=test_string)
            raise AssertionError('Python SDK tests: long connection data should be rejected')
        except OpenTokException:
            pass # expected

    def get_session_info(self, session_id, token = 'devtoken'):
        try:
            url = self.api_url + '/session/' + session_id + '?extended=true'
            req = urllib2.Request(url, '', { 'X-TB-TOKEN-AUTH': token })
            response = urllib2.urlopen(req)
            dom = parseString(response.read())
            response.close()

            return dom
        except urllib2.HTTPError, e:
            print "HTTP Error: failed to send request"

    def get_token_info(self, token):
        try:
            url = self.api_url + '/token/validate'
            req = urllib2.Request(url, '', { 'X-TB-TOKEN-AUTH': token })
            response = urllib2.urlopen(req)
            dom = parseString(response.read())
            response.close()

            return dom
        except urllib2.HTTPError, e:
            print "HTTP Error: failed to send request"

    def assertIsNotNone(self, obj, msg):
        if obj is None:
            raise AssertionError(msg)

    def assertIsNone(self, obj, msg):
        if obj is not None:
            raise AssertionError(msg)

if __name__ == '__main__':
        unittest.main()
