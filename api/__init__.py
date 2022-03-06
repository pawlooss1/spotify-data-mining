import base64
import os

import requests


def get_api_token():
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    authorization = f"Basic {base64.b64encode(bytes(f'{client_id}:{client_secret}', 'utf-8')).decode('utf-8')}"
    response = requests.post(
        url='https://accounts.spotify.com/api/token',
        data={'grant_type': 'client_credentials'},
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': authorization
        }
    )
    return response.json()['access_token']


token = get_api_token()
print(token)
