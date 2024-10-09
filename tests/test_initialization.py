import pytest
import unittest
import platform

from opentok import Client


class OpenTokInitializationTest(unittest.TestCase):
    def setUp(self):
        self.api_key = "123456"
        self.api_secret = "1234567890abcdef1234567890abcdef1234567890"
        self.api_url = "http://environment.example.com"

    def test_intialization(self):
        opentok = Client(self.api_key, self.api_secret)
        assert isinstance(opentok, Client)
        self.assertEqual(opentok.proxies, None)

    def test_set_proxies(self):
        opentok = Client(self.api_key, self.api_secret)
        opentok.proxies = {"https": "https://foo.bar"}
        self.assertEqual(opentok.proxies, {"https": "https://foo.bar"})

    def test_initialization_without_required_params(self):
        with pytest.raises(TypeError):
            opentok = Client()

    def test_initialization_with_api_url(self):
        opentok = Client(self.api_key, self.api_secret, self.api_url)
        assert isinstance(opentok, Client)

    def test_initialization_with_numeric_api_key(self):
        opentok = Client(123456, self.api_secret)
        assert isinstance(opentok, Client)

    def test_initialization_with_timeout(self):
        opentok = Client(self.api_key, self.api_secret, timeout=5)
        assert isinstance(opentok, Client)

    def test_user_agent(self):
        opentok = Client(self.api_key, self.api_secret, self.api_url)
        assert (
            opentok.user_agent
            == f"OpenTok-Python-SDK/{opentok.app_version} python/{platform.python_version()}"
        )

    def test_append_to_user_agent(self):
        opentok = Client(self.api_key, self.api_secret, self.api_url)
        opentok.append_to_user_agent("/my_appended_user_agent_string")
        assert (
            opentok.user_agent
            == f"OpenTok-Python-SDK/{opentok.app_version} python/{platform.python_version()}/my_appended_user_agent_string"
        )


if __name__ == "__main__":
    unittest.main()
