# OpenTok Cloud API Sample Python

This is a simple demo app that shows how you can use the OpenTok-Python-SDK to register
callbacks to receive notifications for streams and connections created and destroyed with your
API Key and also to send arbitrary messages and disconnect participants in OpenTok sessions
from your server.

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

This sample app needs to be reachable from OpenTok servers in order to receive notifications and
usually your machine doesn't have a public address.   There are a number of public services that
can help you overcome that limitation.    For example you can use [localtunnel](https://localtunnel.github.io).

First install localtunnel and start the process to listen for HTTP requests in the port where your
server is listening (by default 5000 in this sample app).
```
npm install -g localtunnel
lt --port 5000
```

You will get a public url from the "lt" command and you have to add it to the environment variables:

```
(venv)$ export PUBLIC_URL=http://orfsvirfmv.localtunnel.me
```

Finally, start the server.

```
(venv)$ python cloud.py
```

Visit <http://localhost:5000/> in your browser. Open it again in a second window. Smile! You've just
set up a group chat.

## Walkthrough

This demo application uses the same frameworks and libraries as the HelloWorld sample. If you have
not already gotten familiar with the code in that project, consider doing so before continuing.

The explanations below are separated by page. Each section will focus on a separate piece of functionality.

### Registering callbacks

The first thing the sample app does is to register callbacks for all the events part of Cloud API. In the
sample app we use a single url to receive all the events but you can register a different url for each event
if that simplifies your implementation.

```python
callback_url = base_url + '/callback
opentok.register_callback('connection', 'created', callback_url)
opentok.register_callback('connection', 'destroyed', callback_url)
opentok.register_callback('stream', 'created', callback_url)
opentok.register_callback('stream', 'destroyed', callback_url)
```

### Listening for events

The next step is to define a route to handle the HTTP callback requests coming from OpenTok to your
server.   In the sample app we use a single route/url to receive all the events and we store them in a
list.

```python
EVENTS = []

@app.route("/callback", methods = ['POST'])
def callback():
    EVENTS.insert(0, request.json)
    return '', 201
```

The list of events is shown in the /events test page.   That is a simple template page showing the events that
we have stored in the EVENTS list so far.

### Sending signals

In the sample app we register a url (/signal) to send signals to a specific connection in a session.   That url is used from
the /events page. The content of the signal is fixed in the sample app but you can change it for your specific use case.

```python
@app.route("/signal", methods = ['POST'])
def signal():
    content = request.form
    opentok.signal(content['sessionId'], content['connectionId'], { 'type': 'chat', 'data': 'Hello!' })
    return '', 201
```

To send a signal you use the signal method in the SDK.  The first parameter is the session where the participant is connected
to and the second parameter is the connectionId of that participant.   That second parameter is optional and you can leave
it empty if you want to send the signal to all the people connected to the session.

### Disconnecting participants

In the sample app we register a url (/disconnect) to disconnect a specific connection from a session.   That url is used from
the /events page.

```python
@app.route("/disconnect", methods = ['POST'])
def disconnect():
    content = request.form
    opentok.force_disconnect(content['sessionId'], content['connectionId'])
    return '', 201
```

To disconnect a participant you use the force_disconnect method in the SDK.  The first parameter is the session
where the participant is connected to and the second parameter is the connectionId of that participant.

That completes the walkthrough for this Cloud API sample application. Feel free to continue to use
this application to receive events from the sessions created for your API Key and try the signal
and force_disconnect APIs.
