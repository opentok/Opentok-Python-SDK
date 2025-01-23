from six import u, PY3
from six.moves.urllib.parse import parse_qs
import base64
import hmac
import hashlib
from jwt import decode


def token_decoder(token: str, secret: str = None):
    token_data = {}
    if token.startswith("T1=="):
        encoded = token[4:]

        # decode the token from base64
        decoded = base64.b64decode(encoded.encode("utf-8"))
        # decode the bytes object back to unicode with utf-8 encoding
        if PY3:
            decoded = decoded.decode()
        parts = decoded.split(u(":"))
        for decoded_part in iter(parts):
            token_data.update(parse_qs(decoded_part))
        # TODO: probably a more elegant way
        for k in iter(token_data):
            token_data[k] = token_data[k][0]
        token_data[u("data_string")] = parts[1]
        return token_data

    encoded = token.replace('Bearer ', '').strip()
    return decode(encoded, secret, algorithms='HS256')


def token_signature_validator(token, secret):
    decoded = token_decoder(token)
    signature = hmac.new(
        secret.encode(u("utf-8")),
        decoded[u("data_string")].encode("utf-8"),
        hashlib.sha1,
    ).hexdigest()
    return signature == decoded[u("sig")]
