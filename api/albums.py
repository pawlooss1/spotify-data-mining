import requests

from api import token
from api.tracks import _create_track_from_json
from domain.album import Album
from domain.track import Track


def get_album(album_id: str, country_code: str = None) -> Album:
    json = requests.get(
        url=f'https://api.spotify.com/v1/albums/{album_id}',
        params={'market': country_code},
        headers={'Authorization': f'Bearer {token}'}
    ).json()
    return _create_album_from_json(json)


def get_albums(albums_ids: list[str], country_code: str = None) -> list[Album]:
    json = requests.get(
        url=f'https://api.spotify.com/v1/albums',
        params={'market': country_code, 'ids': ','.join(albums_ids)},
        headers={'Authorization': f'Bearer {token}'}
    ).json()
    return [_create_album_from_json(j) for j in json['albums']]


def get_album_tracks(album_id: str, country_code: str = None) -> list[Track]:
    json = requests.get(
        url=f'https://api.spotify.com/v1/albums/{album_id}/tracks',
        params={'market': country_code, 'limit': 50},
        headers={'Authorization': f'Bearer {token}'}
    ).json()
    return [_create_track_from_json(j) for j in json['items']]


def _create_album_from_json(json):
    return Album(json['id'], json['name'], json['type'], json.get('genres'), json.get('popularity'),
                 json['release_date'], json['total_tracks'], [artist['id'] for artist in json['artists']],
                 [track['id'] for track in json.get('tracks', {}).get('items', [])])
