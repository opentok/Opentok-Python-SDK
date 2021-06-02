import unittest
from requests.models import Response

from six import text_type, u, b, PY2, PY3
from nose.tools import raises

import requests
import httpretty
from sure import expect
import random
import string

import json

import opentok
from opentok import Client, OpenTok


class OpenTokTest(unittest.TestCase):  
    def setUp(self):
        self.api_key = "123456"
        self.api_secret = "1234567890abcdef1234567890abcdef1234567890"
        self.session_id = "SESSIONID"
        self.opentok = Client(self.api_key, self.api_secret)
        token = string.ascii_letters+string.digits
        self.jwt_token_string = ''.join(random.choice(token[:100]))
        self.stream_id_1 = "Stream1"

    @httpretty.activate
    def test_mute_all_response(self):
        self.url = "https://api.opentok.com/v2/project/{0}/session/{1}/mute".format(
                                                                                self.api_key, 
                                                                                self.session_id)

        httpretty.register_uri(httpretty.POST, 
                                        self.url, 
                                        responses=[
                                            httpretty.Response(body="Testing text matches inside of the JSON file", 
                                                               content_type="application/json",
                                                               adding_headers= {"x-opentok-auth": self.jwt_token_string},
                                                               status=201)
                                        ])

    
        response = requests.post(self.url)

        response.status_code.should.equal(201)
        response.text.should.equal("Testing text matches inside of the JSON file")
        response.headers["x-opentok-auth"].should.equal(self.jwt_token_string)
        response.headers["Content-Type"].should.equal("application/json")

    @httpretty.activate
    def test_mute_stream_response(self):
        self.url = "https://api.opentok.com/v2/project/${0}/session/${1}/stream/${2}/mute".format(
                                                                                                self.api_key, 
                                                                                                self.session_id,
                                                                                                self.stream_id_1)

        httpretty.register_uri(httpretty.POST, 
                                        self.url, 
                                        responses=[
                                            httpretty.Response(body="Testing body of the JSON file", 
                                                               content_type="application/json",
                                                               adding_headers= {"x-opentok-auth": self.jwt_token_string},
                                                               status=201)
                                        ])

    
        response = requests.post(self.url)

        response.status_code.should.equal(201)
        response.text.should.equal("Testing body of the JSON file")
        response.headers["x-opentok-auth"].should.equal(self.jwt_token_string)
        response.headers["Content-Type"].should.equal("application/json")

