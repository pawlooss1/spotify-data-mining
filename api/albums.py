import requests

from api import token


def get_album(album_id):
    json = requests.get(
        url=f'https://api.spotify.com/v1/albums/{album_id}',
        headers={'Authorization': f'Bearer {token}'}
    ).text
    return json
