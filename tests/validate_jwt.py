from six import u
from expects import *
from jose import jwt
import time

def validate_jwt_header(self, jsonwebtoken, test_claims_list=None):
    claims = jwt.decode(jsonwebtoken, self.api_secret, algorithms=[u('HS256')])
    if test_claims_list:
      for test_claim in test_claims_list:
        expect(claims).to(have_key(test_claim))
        expect(claims[test_claim]).to(equal(test_claims_list[test_claim]))
    expect(claims).to(have_key(u('iss')))
    expect(claims[u('iss')]).to(equal(self.api_key))
    expect(claims).to(have_key(u('ist')))
    expect(claims[u('ist')]).to(equal(u('project')))
    expect(claims).to(have_key(u('exp')))
    expect(float(claims[u('exp')])).to(be_above(float(time.time())))
    # todo: add test to check for anvil failure code if exp time is greater than anvil expects
    expect(claims).to(have_key(u('jti')))
    expect(float(claims[u('jti')])).to(be_above_or_equal(float(0)))
    expect(float(claims[u('jti')])).to(be_below(float(1)))
