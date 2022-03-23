from abc import ABC
from typing import List

from db import Table, Instance
from db.gateway import _conn
from db.tables import WeeklyChart, ChartTrack, Track


class IGateway(ABC):
    def __init__(self, table: Table):
        self._conn = _conn
        self._table = table

    def fetch_all(self) -> List[Instance]:
        return self._conn.select_all(self._table)

    def create(self, obj: Instance) -> None:
        self._conn.insert(obj)

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


class TracksGateway(IGateway):
    def __init__(self):
        super().__init__(Track)
