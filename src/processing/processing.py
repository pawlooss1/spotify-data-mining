import itertools
import pandas as pd
from typing import Callable, Dict, Iterator, List

import utils
from api import artists, tracks
from db.gateway.gateway import ArtistsGateway, ChartTracksGateway, ChartsGateway, CountriesGateway, TrackArtistsGateway, TracksGateway


countries_gw = CountriesGateway()
artists_gw = ArtistsGateway()
tracks_gw = TracksGateway()
track_artists_gw = TrackArtistsGateway()
charts_gw = ChartsGateway()
chart_tracks_gw = ChartTracksGateway()


def fetch_tracks(track_ids: List) -> pd.DataFrame:
    df = fetch(track_ids,
               chunk_size=50,
               fetch_fun=tracks.get_tracks)
    df.rename(columns={'name': 'title'})
    return df


def fetch_features(track_ids: List) -> pd.DataFrame:
    df = fetch(track_ids,
               chunk_size=100,
               fetch_fun=tracks.get_tracks_audio_features)
    df.rename(columns={'track_id': 'id'})
    return df


def fetch_artists(artists_ids: List) -> pd.DataFrame:
    return fetch(artists_ids,
                 chunk_size=20,
                 fetch_dun=artists.get_artists)


def fetch(lst: List, chunk_size: int, fetch_fun: Callable[[List], Dict]) -> pd.DataFrame:
    return pd.DataFrame(itertools.chain.from_iterable(_fetch_chunks(lst, chunk_size, fetch_fun)))


def _fetch_chunks(lst: List, chunk_size: int, fn: Callable[[List], Dict]) -> Iterator[Dict]:
    n = len(lst) // chunk_size
    chunked_list = utils.split_into_chunks(lst, chunk_size)
    for i, chunk in enumerate(chunked_list):
        print(f"chunk {i}/{n}")
        yield fn(chunk)


def create_countries(countries: pd.DataFrame) -> None:
    countries_gw.create_all(countries)


def create_tracks_and_artists(tracks: pd.DataFrame,
                              features: pd.DataFrame,
                              artists: pd.DataFrame) -> None:
    tracks_gw.create_all(tracks[['id', 'title']].merge(features,
                                                       how='inner',
                                                       on='id'))
    artists_gw.create_all(artists)
    artists_ids = pd.DataFrame([[t_id, a_id]
                                for t_id, a_ids in tracks[['id', 'artists_ids']].values
                                for a_id in a_ids], columns=['track_id', 'artist_id'])
    track_artists_gw.create_all(artists_ids)


def create_chart(chart_info: pd.Series, chart: pd.DataFrame) -> None:
    chart_id = charts_gw.create(chart_info)
    chart['chart_id'] = chart_id
    chart_tracks_gw.create_all(chart)
