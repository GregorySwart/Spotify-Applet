from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app = Flask(__name__)

app.secret_key = "super_secret"
app.config["SESSION_COOKIE_NAME"] = "My Cookie"


@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/authorize')
def authorize():
    return "Redirect page"


@app.route('/getTracks')
def get_tracks():
    return "Super cool playlist"


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for('authorize', _external=True),
        scope="user-library-read"
    )


if __name__ == "__main__":
    app.run()
