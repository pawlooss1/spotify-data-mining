import os
import datetime as dt
import pandas as pd
import pycountry

import processing
from db import Base
from db import _conn


CHARTS_PATH = "data/charts"


def _create_db() -> None:
    _conn.create_ddl(Base)
    # Create all countries
    ids = os.listdir(CHARTS_PATH)
    names = ["gl" if code == "global" else pycountry.countries.get(alpha_2=code).name
             for code in ids]
    processing.create_countries(pd.DataFrame(list(zip(ids, names)),
                                             columns=['id', 'name']))


def _create_charts() -> pd.DataFrame:
    for dirname, _, filenames in os.walk(CHARTS_PATH):
        for filename in filenames:
            country_code = dirname.replace('\\', '/').split('/')[-1]
            date_str = filename.split("--")[0]
            date_dt = dt.datetime.strptime(date_str, "%Y-%m-%d")
            chart_info = pd.Series({
                'country_code': country_code,
                'date': date_dt
            })
            chart = pd.read_csv(f"{dirname}/{filename}", sep=';')
            processing.create_chart(chart_info, chart)


def main():
    # Create DB
    _create_db()

    # Insert data
    _create_charts()


if __name__ == "__main__":
    main()
