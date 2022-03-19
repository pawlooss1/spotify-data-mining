import os

from dotenv import load_dotenv

from db._connection.connection import connection_factory

load_dotenv()
_conn = connection_factory(
    connector_type=os.environ['DB_TYPE'],
    db_name=os.environ['DB_NAME'],
    username=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'])
