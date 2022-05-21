from flask import Flask, request, redirect

from api import CLIENT_ID
from api.auth import get_access_token
from api.users import get_user_top_tracks

app = Flask(__name__)

REDIRECT_URI = 'http://localhost:8080/recommendations'
AUTHORIZE_REDIRECT = f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=' \
                     f'http://localhost:8080/recommendations&scope=user-top-read'


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    params = request.args
    if 'code' not in params:
        return redirect(AUTHORIZE_REDIRECT)
    token = get_access_token(params['code'], REDIRECT_URI)
    user_tracks = get_user_top_tracks(token)
    return format_response(user_tracks)


def format_response(user_tracks: list):
    formatted_tracks = [format_track(track) for track in user_tracks]
    return {'tracks': formatted_tracks}


def format_track(track) -> str:
    return f"{track['artists'][0]['name']} - {track['name']}"


if __name__ == '__main__':
    app.run(host="localhost", port=8080)
