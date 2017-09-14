from mongoengine import connect
from pymongo.errors import ServerSelectionTimeoutError
import sys

database_connection = None

def connect_db(url):
    global database_connection
    try:
        if not database_connection:
            database_connection = connect()
            database_connection.server_info()
    except ServerSelectionTimeoutError as connection_error:
        print connection_error
        sys.exit(1)

