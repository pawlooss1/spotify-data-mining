from __future__ import annotations

from typing import List

import sqlalchemy.orm

from db import Table, Instance

_CONNECTION_TYPES = {
    'sqlite': "sqlite:///{db_name}"
}


class Connection:
    def __init__(self, url: str):
        self._engine = sqlalchemy.create_engine(url)

    def create_ddl(self, base: Table) -> None:
        base.metadata.create_all(self._engine)

    def insert(self, obj: Instance) -> None:
        with sqlalchemy.orm.Session(self._engine) as session:
            session.add(obj)
            session.commit()

    def insert_all(self, objects: List[Instance]) -> None:
        with sqlalchemy.orm.Session(self._engine) as session:
            session.add_all(objects)
            session.commit()

    def select_all(self, table: Table) -> List[Instance]:
        with sqlalchemy.orm.Session(self._engine) as session:
            return session.query(table).all()

    def delete(self, obj: Instance) -> None:
        with sqlalchemy.orm.Session(self._engine) as session:
            session.delete(obj)
            session.commit()


def connection_factory(connector_type: str, db_name: str, username: str = "", password: str = "") -> Connection:
    conn_str = _CONNECTION_TYPES[connector_type]
    return Connection(conn_str.format(db_name=db_name, username=username, password=password))
