from __future__ import annotations

import enum
import tables

import sqlalchemy.orm


class DataBases(enum.Enum):
    SQLITE = "sqlite:///{dbname}"


def db_factory(db: DataBases, dbname: str, username: str = "", password: str = "") -> DataBase:
    return DataBase(db.value.format(dbname=dbname, username=username, password=password))


class DataBase:
    def __init__(self, url: str):
        self._engine = sqlalchemy.create_engine(url)

    def create_ddl(self, base) -> None:
        base.metadata.create_all(self._engine)


def main() -> None:
    # Create DDL
    path = "../data/sqlite.db"
    db = db_factory(DataBases.SQLITE, path)
    db.create_ddl(tables.Base)

    # Insert


if __name__ == "__main__":
    main()
