from abc import ABC
from typing import List, Dict, Any

import pandas as pd

from src.db import Table, Instance
from src.db.gateway import _conn
from src.db.tables import WeeklyChart, ChartTrack, Track, Artist, track_artists


class IGateway(ABC):
    def __init__(self, table: Table):
        self._conn = _conn
        self._table = table

    def fetch_all(self) -> pd.DataFrame:
        query = self._conn.select_all(self._table)
        df = pd.DataFrame(record.__dict__ for record in query)
        return df.drop('_sa_instance_state', axis=1)

    def create(self, obj: Instance) -> int:
        return self._conn.insert(obj)

    def create_all(self, objects: List[Instance]) -> None:
        self._conn.insert_all(objects)

    def delete(self, obj: Instance) -> None:
        self._conn.delete(obj)


class ChartsGateway(IGateway):
    def __init__(self):
        super().__init__(WeeklyChart)


class ChartTracksGateway(IGateway):
    def __init__(self):
        super().__init__(ChartTrack)


class ArtistsGateway(IGateway):
    def __init__(self):
        super().__init__(Artist)


class TracksGateway(IGateway):
    def __init__(self):
        super().__init__(Track)


class TrackArtistsGateway(IGateway):
    def __init__(self):
        super().__init__(track_artists)

    def create(self, values: Dict[str, Any]) -> None:
        self._conn.insert_values(self._table, values)

    def create_all(self, values: List[Dict[str, Any]]) -> None:
        self._conn.insert_all_values(self._table, values)
