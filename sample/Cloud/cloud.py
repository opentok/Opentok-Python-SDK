from flask import Flask, render_template, request
from opentok import OpenTok
import os

try:
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
    base_url = os.environ.get('PUBLIC_URL') or 'https://73399c05.ngrok.io'
except Exception:
    raise Exception('You must define API_KEY and API_SECRET environment variables')

app = Flask(__name__)
opentok = OpenTok(api_key, api_secret)
session = opentok.create_session()

print 'Registering callbacks'
callback_url = base_url + '/callback'
opentok.register_callback('connection', 'created', callback_url)
opentok.register_callback('connection', 'destroyed', callback_url)
opentok.register_callback('stream', 'created', callback_url)
opentok.register_callback('stream', 'destroyed', callback_url)
print 'Callbacks registered'

EVENTS = []

@app.route("/callback", methods = ['POST'])
def callback():
    EVENTS.insert(0, request.json)
    return '', 201

@app.route("/")
def index():
    key = api_key
    session_id = session.session_id
    token = opentok.generate_token(session_id)
    return render_template('index.html', api_key=key, session_id=session_id, token=token)

@app.route("/events")
def events():
    return render_template('events.html', events=EVENTS)

@app.route("/disconnect", methods = ['POST'])
def disconnect():
    content = request.form
    opentok.force_disconnect(content['sessionId'], content['connectionId'])
    return '', 201

@app.route("/signal", methods = ['POST'])
def signal():
    content = request.form
    opentok.signal(content['sessionId'], content['connectionId'], { 'type': 'chat', 'data': 'Hello!' })
    return '', 201

if __name__ == "__main__":
    app.run(debug=True)
