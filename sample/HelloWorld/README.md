# OpenTok Hello World Python

This is a simple demo app that shows how you can use the OpenTok-Python-SDK to create Sessions,
generate Tokens with those Sessions, and then pass these values to a JavaScript client that can
connect and conduct a group chat.

## Running the App

First, we highly recommend setting up a [virtualenv](http://www.virtualenv.org/en/latest/).

```
$ virtualenv venv
$ source venv/bin/activate
```

Next, download the dependencies using [Pip](http://www.pip-installer.org/en/latest/), from the
current directory:

```
(venv)$ pip install -r requirements.txt
```

Then add your own API Key and API Secret to the environment variables. There are a few ways to do
this but the simplest would be to do it right in your shell.

```
(venv)$ export API_KEY=0000000
(venv)$ export API_SECRET=abcdef1234567890abcdef01234567890abcdef
```

Finally, start the server.

```
(venv)$ python helloworld.py
```

Visit <http://127.0.0.1:5000/> in your browser. Open it again in a second window. Smile! You've just
set up a group chat.

## Walkthrough

This demo application uses the [Flask web microframework](http://flask.pocoo.org/). It is similar to
many other popular web frameworks. We are only covering the very basics of the framework, but you can
learn more by following the links above.

### Main Application (helloworld.py)

The first thing done in this file is to import the dependencies we will be using. In this case that
is the Flask web framework, the os module, and most importantly the OpenTok SDK.

```python
from flask import Flask, render_template
from opentok import OpenTok
import os
```

Next this file performs some basic checks on the environment. If it cannot find the `API_KEY`and
`API_SECRET` environment variables, there is no point in continuing.

The object `app` is our application and its initialized by instantiating an object from Flask.
Then we initialize an instance of OpenTok as `opentok`. If this file is run as the main file, 
we should start running the app.

```python
app = Flask(__name__)
opentok = OpenTok(api_key, api_secret)

# ...

if __name__ == "__main__":
    app.run()
```

Now, lets discuss the Hello World application's functionality. We want to set up a group chat so
that any client that visits a page will connect to the same OpenTok Session. Once they are connected
they can Publish a Stream and Subscribe to all the other streams in that Session. So we just need
one Session object, and it needs to be accessible every time a request is made. On the next line we
simply call the `OpenTok` instance's `create_session` method to get a Session and store it in the
`session` variable. Alternatively, `session_id`s are commonly stored in databses for applications
that have many of them.

```python
session = opentok.create_session()
```

We only need one page, so we create one route handler for any HTTP GET requests to trigger.

```python
@app.route("/")
def hello():
  # ...
```

Now all we have to do is serve a page with the three values the client will need to connect to the
session: `api_key`, `session_id`, and `token`. The `api_key` is available in the outer scope so we
can just assign it. The `session_id` is available as the `session.session_id` attribute. The `token`
is generated freshly on this request by calling the `generate_token` method of the `opentok`
instance, and passing in the `session_id`. This is because a Token is a piece of information that
carries a specific client's permissions in a certain Session. Ideally, as we've done here, you
generate a unique token for each client that will connect.

```python
    key = api_key
    session_id = session.session_id
    token = opentok.generate_token(session_id)
```

Now all we have to do is serve a page with those three values. Lets call our `render_template`
helper that will pick up a template called `index.html` from the `templates/` directory in our
application and pass in the variables for it to include on the page.

```python
    return render_template('index.html', api_key=key, session_id=session_id, token=token)
```

### Main Template (templates/index.html)

This file simply sets up the HTML page for the JavaScript application to run, imports the
JavaScript library, and passes the values created by the server into the JavaScript application
inside `public/js/helloworld.js`

### JavaScript Applicaton (static/js/helloworld.js)

The group chat is mostly implemented in this file. At a high level, we connect to the given
Session, publish a stream from our webcam, and listen for new streams from other clients to
subscribe to.

For more details, read the comments in the file or go to the
[JavaScript Client Library](http://tokbox.com/opentok/libraries/client/js/) for a full reference.
