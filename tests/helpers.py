from six import text_type, u, b, PY3
from six.moves.urllib.parse import parse_qs
import base64
import hmac
import hashlib


def token_decoder(token):
    token_data = {}
    # remove sentinal
    encoded = token[4:]
    decoded = base64.b64decode(encoded.encode("utf-8"))
    # decode the bytes object back to unicode with utf-8 encoding
    if PY3:
        decoded = decoded.decode()
    parts = decoded.split(u(":"))
    for decoded_part in iter(parts):
        token_data.update(parse_qs(decoded_part))
    # TODO: probably a more elegent way
    for k in iter(token_data):
        token_data[k] = token_data[k][0]
    token_data[u("data_string")] = parts[1]
    return token_data


def token_signature_validator(token, secret):
    decoded = token_decoder(token)
    signature = hmac.new(
        secret.encode(u("utf-8")),
        decoded[u("data_string")].encode("utf-8"),
        hashlib.sha1,
    ).hexdigest()
    return signature == decoded[u("sig")]
