# Opentok

OpenTok is an API from TokBox that enables websites to weave live group video communication into their online experience. Check out <http://www.tokbox.com/> for more information.  
Please visit our [getting started page](http://www.tokbox.com/opentok/tools/js/gettingstarted) if you are unfamiliar with these concepts.  

## Installation

To install from PyPi using [pip](http://www.pip-installer.org/en/latest/), a package manager for Python. 
<pre>
pip install opentok
</pre>

If you get "Permission Denied" errorsm try running it with `sudo` in front:
<pre>
sudo pip install opentok
</pre>

## Requirements

You need an api-key and secret. Sign up at <http://www.tokbox.com/opentok/tools/js/apikey>.

# OpenTokSDK

In order to use any of the server side functions, you must first create an `OpenTokSDK` object with your developer credentials.  
`OpenTokSDK` takes 2 parameters:
> api_key (string) - Given to you when you register  
> api_secret (string) - Given to you when you register  

```python
import OpenTokSDK

# Creating an OpenTok Object
API_KEY = ''                # should be a string
API_SECRET = ''            # should be a string
OTSDK = OpenTokSDK.OpenTokSDK(API_KEY,API_SECRET)
```


## Creating Sessions
Use your `OpenTokSDK` object to create `session_id`  
`create_session` takes 1-2 parameters:
> location (string) -  OPTIONAL. a location so OpenTok can stream through the closest server  
> properties (object) - OPTIONAL. Set peer to peer as `enabled` or `disabled`. Disabled by default  

<pre>
# creating a simple session: closest streaming server will be automatically determined when user connects to session
session_id = OTSDK.create_session().session_id

# Creating Session object with p2p enabled
session_properties = {OTSDK.SessionProperties.p2p_preference: "enabled"}    # or disabled
session_id = OTSDK.create_session(None, sessionProperties ).session_id
</pre>

## Generating Tokens
With the generated sessionId, you can start generating tokens for each user.
`generate_token` takes in 1-4 properties:
> session_id (string) - REQUIRED  
> role (string) - OPTIONAL. subscriber, publisher, or moderator  
> expire_time (int) - OPTIONAL. Time when token will expire in unix timestamp  
> connection_data (string) - OPTIONAL. Metadata to store data (names, user id, etc)

<pre>
# Generating a token
token = OTSDK.generate_token(session_id, OTSDK.RoleConstants.PUBLISHER, "username=Bob,level=4")
</pre>

Possible Errors:
> "Null or empty session ID are not valid"  
> "An invalid session ID was passed"
