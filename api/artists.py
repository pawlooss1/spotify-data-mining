import requests

from api import token
from domain.artist import Artist


def get_artist(artist_id):
    json = requests.get(
        url=f'https://api.spotify.com/v1/artists/{artist_id}',
        headers={'Authorization': f'Bearer {token}'}
    ).json()
    return Artist(json['id'], json['name'], json['followers']['total'], json['genres'], json['popularity'])


def get_artist_top_tracks(artist_id, country_code):
    return requests.get(
        url=f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks',
        params={'market': country_code},
        headers={'Authorization': f'Bearer {token}'}
    ).text
    return json
