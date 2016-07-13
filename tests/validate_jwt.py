from six import u
from sure import expect
from jose import jwt
import time

def validate_jwt_header(self, jsonwebtoken):
    claims = jwt.decode(jsonwebtoken, self.api_secret, algorithms=[u('HS256')])
    claims.should.have.key(u('iss'))
    expect(claims[u('iss')]).to.equal(self.api_key)
    claims.should.have.key(u('ist'))
    expect(claims[u('ist')]).to.equal(u('project'))
    claims.should.have.key(u('exp'))
    expect(float(claims[u('exp')])).to.be.greater_than(float(time.time()))
    # todo: add test to check for anvil failure code if exp time is greater than anvil expects
    claims.should.have.key(u('jti'))
    expect(float(claims[u('jti')])).to.be.greater_than_or_equal_to(float(0))
    expect(float(claims[u('jti')])).to.be.lower_than(float(1))
