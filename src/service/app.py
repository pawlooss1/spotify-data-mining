from flask import Flask, request, redirect

from api import CLIENT_ID
from api.artists import get_artists
from api.auth import get_access_token
from api.tracks import get_tracks_audio_features, get_tracks
from api.users import get_user_top_tracks
from domain.track import Track
from recommendation.engine import create_recommendations

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
    user_tracks_ids = [track['id'] for track in user_tracks]
    user_tracks_features = get_tracks_audio_features(user_tracks_ids)
    recommendations_ids = create_recommendations(user_tracks_features)
    recommendations_tracks = get_tracks(recommendations_ids)
    return format_response(recommendations_tracks)


def format_response(user_tracks: list):
    formatted_tracks = [format_track(track) for track in user_tracks]
    return {'tracks': formatted_tracks}


def format_track(track: Track) -> str:
    artist_names = [a.name for a in get_artists(track.artists_ids)]
    return f"{', '.join(artist_names)} - {track.name} {track.id}"


if __name__ == '__main__':
    app.run(host="localhost", port=8080)
