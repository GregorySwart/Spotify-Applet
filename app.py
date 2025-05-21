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
    return "Homepage"


@app.route('/redirect')
def redirect():
    return "Redirect page"


@app.route('/getTracks')
def get_tracks():
    return "Super cool playlist"


if __name__ == "__main__":
    app.run()
