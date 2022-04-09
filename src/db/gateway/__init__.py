import os

from dotenv import load_dotenv

from .._connection.connection import connection_factory

load_dotenv()
_conn = connection_factory(
    connector_type=os.environ['DB_TYPE'],
    address=os.environ['DB_ADDRESS'],
    port=os.environ['DB_PORT'],
    db_name=os.environ['DB_NAME'],
    username=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'])
