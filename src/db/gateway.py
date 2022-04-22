import pandas as pd
from abc import ABC

from db import _conn, Table
from db.tables import Country, WeeklyChart, ChartTrack, Track, Artist, track_artists


class IPandasGateway(ABC):
    def __init__(self, table: Table):
        self._conn = _conn
        self._table = table

    def fetch_all(self) -> pd.DataFrame:
        query = self._conn.select_all(self._table)
        df = pd.read_sql(query.statement, query.session.bind)
        return df.set_index('id')

    def create(self, row: pd.Series) -> int:
        obj = self._table(**row.to_dict())
        return self._conn.insert(obj)

    def create_all(self, df: pd.DataFrame) -> None:
        objects = [self._table(**row.to_dict()) for _, row in df.iterrows()]
        self._conn.insert_all(objects)


class CountriesGateway(IPandasGateway):
    def __init__(self):
        super().__init__(Country)


class ChartsGateway(IPandasGateway):
    def __init__(self):
        super().__init__(WeeklyChart)


class ChartTracksGateway(IPandasGateway):
    def __init__(self):
        super().__init__(ChartTrack)


class ArtistsGateway(IPandasGateway):
    def __init__(self):
        super().__init__(Artist)


class TracksGateway(IPandasGateway):
    def __init__(self):
        super().__init__(Track)


class TrackArtistsGateway(IPandasGateway):
    def __init__(self):
        super().__init__(track_artists)

    def create(self, row: pd.Series) -> None:
        self._conn.insert_values(self._table, row.to_dict())

    def create_all(self, df: pd.DataFrame) -> None:
        objects = [row.to_dict() for _, row in df.iterrows()]
        self._conn.insert_all_values(self._table, objects)
