import datetime as dt
import glob
import json
import os
from typing import Tuple, List, Dict

import pandas as pd
import pycountry
from dotenv import load_dotenv

from db import Table, Base
from db._connection.connection import Connection, connection_factory
from db.gateway.gateway import TracksGateway, ChartsGateway, ChartTracksGateway, ArtistsGateway, TrackArtistsGateway
from db.tables import Track, WeeklyChart, ChartTrack, Artist


def _create_tables(conn: Connection, base: Table) -> None:
    # Create DDL
    conn.create_ddl(base)


def _insert_tracks(gw_t: TracksGateway, gw_ta: TrackArtistsGateway) -> None:
    # Insert tracks
    tracks_path = "../data/features.csv"
    df = pd.read_csv(tracks_path)
    tracks = [Track(**track[1].to_dict()) for track in df.iloc[:, df.columns != 'artists_ids'].iterrows()]
    gw_t.create_all(tracks)
    _insert_track_artists(gw_ta, df[['track_id', 'artists_ids']].values)


def _insert_artists(gw: ArtistsGateway) -> None:
    # Insert artists
    artists_path = "../data/artists.csv"
    df = pd.read_csv(artists_path)
    artists = [Artist(**artist[1].to_dict()) for artist in df.iterrows()]
    gw.create_all(artists)


def _insert_track_artists(gw: TrackArtistsGateway, tracks: List[List[str]]) -> None:
    # Insert track artists
    track_artists = [{'track_id': t[0], 'artist_id': a} for t in tracks for a in json.loads(t[1])]
    gw.create_all(track_artists)


def _insert_charts_and_tracks(gw_charts: ChartsGateway, gw_tracks: ChartTracksGateway) -> None:
    # Insert charts
    charts_path = "../data/charts"
    for country_path in glob.glob(f"{charts_path}/*"):
        print(f"Loading charts for {country_path[-2:]}:")
        for chart_path in glob.glob(f"{country_path}/*"):
            print(f"\t{chart_path[-26:]}")
            chart_path = os.path.normpath(chart_path)
            chart_path = chart_path.replace("\\", '/')
            chart_id = _insert_chart(gw_charts, chart_path)
            _insert_chart_tracks(gw_tracks, chart_path, chart_id)


def _insert_chart(gw: ChartsGateway, chart_path: str) -> int:
    country_code, chart_name = chart_path.split('/')[-2:]
    country, date = _parse_chart(country_code, chart_name)
    chart = WeeklyChart(country=country, date=date)
    return gw.create(chart)


def _parse_chart(country_code: str, chart_name: str) -> Tuple[str, dt.date]:
    country = pycountry.countries.get(alpha_2=country_code.upper()).name if len(country_code) == 2 else country_code
    date_str = chart_name.split("--")[0]
    date = dt.datetime.strptime(date_str, "%Y-%m-%d").date()
    return country, date


def _insert_chart_tracks(gw: ChartTracksGateway, chart_path: str, chart_id: int) -> None:
    # Insert chart tracks
    df = pd.read_csv(chart_path, sep=';')
    df.drop(['title', 'artist'], axis=1, inplace=True)
    df['chart_id'] = chart_id
    chart_tracks = [ChartTrack(**track[1].to_dict()) for track in df.iterrows()]
    gw.create_all(chart_tracks)


def main() -> None:
    load_dotenv()
    conn_type = os.environ['DB_TYPE']
    db_addr = os.environ['DB_ADDRESS']
    db_port = os.environ['DB_PORT']
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USERNAME']
    db_password = os.environ['DB_PASSWORD']
    conn = connection_factory(conn_type, db_addr, db_port, db_name, db_user, db_password)

    artists_gw = ArtistsGateway()
    tracks_gw = TracksGateway()
    track_artists_gw = TrackArtistsGateway()
    charts_gw = ChartsGateway()
    chart_tracks_gw = ChartTracksGateway()

    # Init DB
    _create_tables(conn, Base)
    _insert_artists(artists_gw)
    _insert_tracks(tracks_gw, track_artists_gw)
    _insert_charts_and_tracks(charts_gw, chart_tracks_gw)

    tracks = chart_tracks_gw.fetch_all()
    print(tracks)


if __name__ == "__main__":
    main()
