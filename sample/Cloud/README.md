# OpenTok Cloud API Sample Python

This simple demo app shows how to use the OpenTok Python SDK to do the following:

* Register callbacks to receive notifications for streams and connections created and destroyed
  in an OpenTok session

* Send arbitrary messages to clients in an OpenTok session

* Disconnect participants in OpenTok sessions

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

Then add your OpenTok API Key and API secret to the environment variables. There are a few ways to
do this, but the simplest way is to add them using the command line:

```
(venv)$ export API_KEY=0000000
(venv)$ export API_SECRET=abcdef1234567890abcdef01234567890abcdef
```

This sample app needs to be reachable from OpenTok servers in order to receive notifications.
Usually, your machine doesn't have a public IP address. There are a number of public services
that can help you overcome that limitation. For example you can use
[localtunnel](https://localtunnel.github.io).

First, install localtunnel and start the process to listen for HTTP requests on the port where your
server is listening (by default 5000 in this sample app):

```
npm install -g localtunnel
lt --port 5000
```

You will get a public URL from the `lt` command. Add it to the `PUBLIC_URL` environment variable:

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

The explanations focus on a separate piece of functionality defined by the OpenTok Cloud API.

### Registering callbacks

First, the sample app registers callbacks for all the events defined by the OpenTok Cloud API.
By default, the app uses a single URL to receive all the events, but you can register a different
URL for each event if that simplifies your implementation:

```python
callback_url = base_url + '/callback
opentok.register_callback('connection', 'created', callback_url)
opentok.register_callback('connection', 'destroyed', callback_url)
opentok.register_callback('stream', 'created', callback_url)
opentok.register_callback('stream', 'destroyed', callback_url)
```

To register a callback for an OpenTok Cloud event, call the `OpenTok.register_callback()` method
of the OpenTok Python SDK. The first parameter, `'group'`, defining the group of events you are
interested in, can be set to `'archive'`, `'connection'`, or `'stream'`. The second parameter,
`'type'`, can be set to `'status'` for `'archive'` events, and it can be set to `'created'` or `'destroyed'` for the connection and stream groups. The third parameter sets the callback URL.
This app sets callback URLs to be called when OpenTok connections or streams are created or
destroyed.

The next step is to define a route to handle the HTTP callback requests coming from OpenTok to your
server. The sample app we use a single route/URL to receive all events, and we store the events
in a list.

```python
EVENTS = []

@app.route("/callback", methods = ['POST'])
def callback():
    EVENTS.insert(0, request.json)
    return '', 201
```

The list of events is displayed in the /events test page (<http://localhost:5000/events>). That is
a simple template page showing the events that are stored in the `EVENTS` list.

### Sending signals

In the sample app we register a URL (/signal) to send signals to a specific connection in a session.
That URL is called from the /events (<http://localhost:5000/events>) page. The content of the signal
is fixed in the sample app, but you can change it for your specific use case:

```python
@app.route("/signal", methods = ['POST'])
def signal():
    content = request.form
    opentok.signal(content['sessionId'], content['connectionId'], { 'type': 'chat', 'data': 'Hello!' })
    return '', 201
```

To send a signal, call the `OpenTok.signal()` method of the OpenTok Python SDK. The first parameter
is the ID of the OpenTok session, and the second parameter is the connection ID of the client to
receive the signal. The second parameter is optional, and you can leave it empty to send the signal
to all clients connected to the session. The third parameter defines the `type` and `data` strings
to send as the signal payload.

This is the server-side equivalent to the signal() method in the OpenTok client SDKs. See
<https://www.tokbox.com/developer/guides/signaling/js/>.

### Disconnecting participants

The sample app registers a URL (/disconnect) to disconnect a specific connection from a session.
That URL is called from the /events (<http://localhost:5000/events>) page.

```python
@app.route("/disconnect", methods = ['POST'])
def disconnect():
    content = request.form
    opentok.force_disconnect(content['sessionId'], content['connectionId'])
    return '', 201
```

To disconnect a client from a session, call the `OpenTok.force_disconnect()` method of the OpenTok
Python SDK. The first parameter is the session ID, and the second parameter is the connection ID of
the client to disconnect.

This is the server-side equivalent to the forceDisconnect() method in OpenTok.js:
<https://www.tokbox.com/developer/guides/moderation/js/#force_disconnect>.