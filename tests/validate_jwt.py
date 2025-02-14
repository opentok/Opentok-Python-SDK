from six import u
from expects import *
from jwt import decode
import time


def validate_jwt_header(self, jsonwebtoken):
    claims = decode(jsonwebtoken, self.api_secret, algorithms=["HS256", "RS256"])
    expect(claims).to(have_key(u("iss")))
    expect(claims[u("iss")]).to(equal(self.api_key))
    expect(claims).to(have_key(u("ist")))
    expect(claims[u("ist")]).to(equal(u("project")))
    expect(claims).to(have_key(u("exp")))
    expect(float(claims[u("exp")])).to(be_above(float(time.time())))
    # todo: add test to check for anvil failure code if exp time is greater than anvil expects
    expect(claims).to(have_key(u("jti")))
    expect(float(claims[u("jti")])).to(be_above_or_equal(float(0)))
    expect(float(claims[u("jti")])).to(be_below(float(1)))
