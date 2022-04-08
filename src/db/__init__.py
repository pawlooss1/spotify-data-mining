from typing import Type

import sqlalchemy.orm

Base = sqlalchemy.orm.declarative_base()
Table = Type[Base]
Instance = Base
