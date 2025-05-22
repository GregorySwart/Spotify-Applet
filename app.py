import os
import pathlib

import spotipy
from dotenv import load_dotenv
from flask import Flask, request, url_for, session, redirect
from spotipy.oauth2 import SpotifyOAuth

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
    sp_oauth = create_spotify_oauth()
    session.clear()

    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code, check_cache=False)
    session["token_info"] = token_info

    sp = spotipy.Spotify(auth=token_info["access_token"])
    user = sp.current_user()
    user_name = user["display_name"]

    user_liked_songs = sp.current_user_saved_tracks(limit=50, offset=0)["items"]

    response_str = ""
    response_str += f"<h1>Welcome, {user_name}</h1>\n"
    response_str += "<p>Liked songs:</p>"
    response_str += "<p>"
    for liked_song in user_liked_songs:
        song_name = str(liked_song["track"]["name"])
        artists = ", ".join([a["name"] for a in liked_song["track"]["artists"]])
        response_str += f'{song_name} - {artists}</br>'
    response_str += "</p>"

    return response_str


@app.route('/getTracks')
def get_tracks():
    return "Super cool playlist"


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)

    delete_cache()
    return redirect('https://open.spotify.com/logout')  # Hacky way to log user out - TODO disable spotipy caching


def create_spotify_oauth():
    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for('authorize', _external=True),
        scope="user-library-read",
        cache_path=None
    )
    delete_cache()
    return sp_oauth


def delete_cache():
    cache_path = f"{os.getcwd()}\\.cache"
    cache_file = pathlib.Path(cache_path)
    pathlib.Path.unlink(cache_file, missing_ok=True)


if __name__ == "__main__":
    app.run(debug=True)
