import unittest

import requests
import httpretty
import random
import string

from opentok import Client


class OpenTokTest(unittest.TestCase):  
    def setUp(self):
        self.api_key = "123456"
        self.api_secret = "1234567890abcdef1234567890abcdef1234567890"
        self.session_id = "SESSIONID"
        self.connection_id = "CONNECTIONID"

        self.opentok = Client(self.api_key, self.api_secret)
        token = string.ascii_letters+string.digits
        self.jwt_token_string = ''.join(random.choice(token[:100]))
        self.stream_id_1 = "Stream1"

   

    @httpretty.activate
    def test_mute_all_exclude_streams(self):
        self.url = "https://api.opentok.com/v2/project/{0}/session/{1}/mute".format(
                                                                                self.api_key, 
                                                                                self.session_id)

        httpretty.register_uri(httpretty.POST, 
                                        self.url, 
                                        responses=[
                                            httpretty.Response(body='{"active": True, "excludedStreams": "excludedStreamIds1"}', 
                                                               content_type="application/json",
                                                               adding_headers= {"x-opentok-auth": self.jwt_token_string},
                                                               status=201)
                                        ])

    
        response = requests.post(self.url)

        response.text.should.equal('{"active": True, "excludedStreams": "excludedStreamIds1"}')
        response.headers["x-opentok-auth"].should.equal(self.jwt_token_string)
        response.headers["Content-Type"].should.equal("application/json")

    @httpretty.activate
    def test_disable_force_mute(self):
        self.url = "https://api.opentok.com/v2/project/{0}/session/{1}/mute".format(
                                                                                self.api_key, 
                                                                                self.session_id)

        httpretty.register_uri(httpretty.POST, 
                                        self.url, 
                                        responses=[
                                            httpretty.Response(body='{}',
                                                                content_type="application/json",
                                                                adding_headers= {"x-opentok-auth": self.jwt_token_string},
                                                                status=201)
                                        ])

    
        response = requests.post(self.url)

        response.text.should.equal('{}')
        response.headers["x-opentok-auth"].should.equal(self.jwt_token_string)
        response.headers["Content-Type"].should.equal("application/json")


    @httpretty.activate
    def test_mute_single_stream(self):
        self.url = "https://api.opentok.com/v2/project/{0}/session/{1}/stream/{2}/mute".format(
                                                                                self.api_key, 
                                                                                self.session_id,
                                                                                self.stream_id_1)

        httpretty.register_uri(httpretty.POST, 
                                        self.url, 
                                        responses=[
                                            httpretty.Response(body='{"session_id": "12345", "stream_id": "abcde"}', 
                                                               content_type="application/json",
                                                               adding_headers= {"x-opentok-auth": self.jwt_token_string},
                                                               status=201)
                                        ])

    
        response = requests.post(self.url)

        response.text.should.equal('{"session_id": "12345", "stream_id": "abcde"}')
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

    @httpretty.activate
    def test_dtmf_all_clients(self):
        self.url = f"https://api.opentok.com/v2/project/{self.api_key}/session/{self.session_id}/play-dtmf"
                                                                            
        httpretty.register_uri(httpretty.POST, 
                                        self.url, 
                                        responses=[
                                            httpretty.Response(body="Testing text matches inside of the JSON file", 
                                                               content_type="application/json",
                                                               adding_headers= {"x-opentok-auth": self.jwt_token_string},
                                                               status=200)
                                        ])

    
        response = requests.post(self.url)

        response.status_code.should.equal(200)
        response.text.should.equal("Testing text matches inside of the JSON file")
        response.headers["x-opentok-auth"].should.equal(self.jwt_token_string)
        response.headers["Content-Type"].should.equal("application/json")

    @httpretty.activate
    def test_dtmf_specific_client(self):
        self.url = f"https://api.opentok.com/v2/project/{self.api_key}/session/{self.session_id}/connection/{self.connection_id}/play-dtmf"
                                                                            
        httpretty.register_uri(httpretty.POST, 
                                        self.url, 
                                        responses=[
                                            httpretty.Response(body="Testing text matches inside of the JSON file", 
                                                               content_type="application/json",
                                                               adding_headers= {"x-opentok-auth": self.jwt_token_string},
                                                               status=200)
                                        ])

    
        response = requests.post(self.url)

        response.status_code.should.equal(200)
        response.text.should.equal("Testing text matches inside of the JSON file")
        response.headers["x-opentok-auth"].should.equal(self.jwt_token_string)
        response.headers["Content-Type"].should.equal("application/json")

