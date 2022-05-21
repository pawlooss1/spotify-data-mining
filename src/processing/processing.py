import itertools
import logging
import pandas as pd
import pycountry
from typing import Callable, Dict, Iterator, List

import utils
import scraper
from api import artists, tracks
from db import _conn, Base
from db.gateway import ArtistsGateway, ChartTracksGateway, ChartsGateway, CountriesGateway, TrackArtistsGateway, TracksGateway


logger = logging.getLogger("processing")

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
    return df.rename(columns={'track_id': 'id', 'name': 'title'})


def fetch_features(track_ids: List) -> pd.DataFrame:
    df = fetch(track_ids,
               chunk_size=100,
               fetch_fun=tracks.get_tracks_audio_features)
    return df.rename(columns={'track_id': 'id'})


def fetch_artists(artists_ids: List) -> pd.DataFrame:
    return fetch(artists_ids,
                 chunk_size=20,
                 fetch_fun=artists.get_artists)


def fetch(lst: List, chunk_size: int, fetch_fun: Callable[[List], Dict]) -> pd.DataFrame:
    return pd.DataFrame(itertools.chain.from_iterable(_fetch_chunks(lst, chunk_size, fetch_fun)))


def _fetch_chunks(lst: List, chunk_size: int, fn: Callable[[List], Dict]) -> Iterator[Dict]:
    chunked_list = utils.split_into_chunks(lst, chunk_size)
    for _, chunk in enumerate(chunked_list):
        yield fn(chunk)

def create_db() -> None:
    _conn.create_ddl(Base)
    # Create all countries
    ids = scraper.scrape_countries()
    ids[ids.index("global")] = "gl"
    names = ["Global" if code == "gl" else pycountry.countries.get(alpha_2=code).name
             for code in ids]
    create_countries(pd.DataFrame(list(zip(ids, names)), columns=['id', 'name']))


def create_countries(countries: pd.DataFrame) -> None:
    countries_gw.create_all(countries)


def create_tracks_and_artists(df_tracks: pd.DataFrame) -> None:
    df_features = fetch_features(df_tracks['id'].values)
    tracks_gw.create_all(df_tracks[['id', 'title']].merge(df_features,
                                                          how='left',
                                                          on='id'))
    artists_ids = set(itertools.chain.from_iterable(df_tracks['artists_ids'].values))
    df_artists = fetch_artists(artists_ids)
    artists_gw.create_all(df_artists)
    track_artists_ids = pd.DataFrame([[t_id, a_id]
                                     for t_id, a_ids in df_tracks[['id', 'artists_ids']].values
                                     for a_id in a_ids], columns=['track_id', 'artist_id'])
    track_artists_gw.create_all(track_artists_ids)


def create_chart(chart_info: pd.Series, chart: pd.DataFrame) -> None:
    logger.info(f"Procesing chart {chart_info['country_code']!r} {chart_info['date']!r}")

    df_tracks = fetch_tracks(chart['track_id'].values)
    create_tracks_and_artists(df_tracks)
    chart_id = charts_gw.create(chart_info)[0][0]
    chart['chart_id'] = chart_id
    chart.drop(['title', 'artist'], axis=1, inplace=True)
    chart_tracks_gw.create_all(chart)


if __name__ == "__main__":
    from scraper import scrape_chart
    ch = scrape_chart("2022-04-22--2022-04-29", "sv")
    tr = fetch_tracks(ch['track_id'])
    create_tracks_and_artists(tr)
