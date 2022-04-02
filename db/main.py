import datetime as dt
import glob
import os
from typing import Tuple

import pandas as pd
import pycountry
from dotenv import load_dotenv

from db import Table, Base
from db._connection.connection import Connection, connection_factory
from db.gateway.gateway import TracksGateway, ChartsGateway, ChartTracksGateway
from db.tables import Track, WeeklyChart, ChartTrack


def _create_tables(conn: Connection, base: Table) -> None:
    # Create DDL
    conn.create_ddl(base)


def _insert_tracks(gw: TracksGateway) -> None:
    # Insert tracks
    tracks_path = "../data/features_with_empty_artists.csv"
    df = pd.read_csv(tracks_path)
    tracks = [Track(**track[1].to_dict()) for track in df.iterrows()]
    gw.create_all(tracks)


def _insert_charts_and_tracks(gw_charts: ChartsGateway, gw_tracks) -> None:
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

    tracks_gw = TracksGateway()
    charts_gw = ChartsGateway()
    chart_tracks_gw = ChartTracksGateway()

    # Init DB
    _create_tables(conn, Base)
    _insert_tracks(tracks_gw)
    _insert_charts_and_tracks(charts_gw, chart_tracks_gw)

    tracks = chart_tracks_gw.fetch_all()
    print(tracks)


if __name__ == "__main__":
    main()
