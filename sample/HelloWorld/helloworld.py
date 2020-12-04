from flask import Flask, render_template
from opentok import OpenTok
import os

try:
    api_key = os.environ["API_KEY"]
    api_secret = os.environ["API_SECRET"]
except Exception:
    raise Exception("You must define API_KEY and API_SECRET environment variables")

app = Flask(__name__)
opentok = OpenTok(api_key, api_secret)
session = opentok.create_session()


@app.route("/")
def hello():
    key = api_key
    session_id = session.session_id
    token = opentok.generate_token(session_id)
    return render_template(
        "index.html", api_key=key, session_id=session_id, token=token
    )


if __name__ == "__main__":
    app.debug = True
    app.run()
