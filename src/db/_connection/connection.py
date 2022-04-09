from __future__ import annotations

from typing import List, Dict, Any

import sqlalchemy.orm

from src.db import Table, Instance

_CONNECTION_TYPES = {
    'sqlite': "sqlite:///{address}/{db_name}",
    'postgres': "postgresql://{username}:{password}@{address}:{port}/{db_name}"
}


class Connection:
    def __init__(self, url: str):
        self._engine = sqlalchemy.create_engine(url)

    def create_ddl(self, base: Table) -> None:
        base.metadata.create_all(self._engine)

    def insert(self, obj: Instance) -> int:
        with sqlalchemy.orm.Session(self._engine) as session:
            session.add(obj)
            session.commit()
            return obj.id

    def insert_values(self, table: Table, values: Dict[str, Any]) -> None:
        self._engine.connect().execute(table.insert(), values)

    def insert_all_values(self, table: Table, values: List[Dict[str, Any]]) -> None:
        self._engine.connect().execute(table.insert(), values)

    def insert_all(self, objects: List[Instance]) -> None:
        with sqlalchemy.orm.Session(self._engine) as session:
            session.add_all(objects)
            session.commit()

    def select_all(self, table: Table) -> sqlalchemy.orm.Query:
        with sqlalchemy.orm.Session(self._engine) as session:
            return session.query(table)

    def delete(self, obj: Instance) -> None:
        with sqlalchemy.orm.Session(self._engine) as session:
            session.delete(obj)
            session.commit()


def connection_factory(connector_type: str,
                       address: str,
                       port: str,
                       db_name: str,
                       username: str,
                       password: str) -> Connection:
    conn_str = _CONNECTION_TYPES[connector_type]
    return Connection(conn_str.format(address=address,
                                      port=port,
                                      db_name=db_name,
                                      username=username,
                                      password=password))
