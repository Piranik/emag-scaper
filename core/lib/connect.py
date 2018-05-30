from mongoengine import connect
from pymongo.errors import ServerSelectionTimeoutError
import sys

database_connection = None

def connect_db(url):
    global database_connection
    try:
        if not database_connection:
            print url
            database_connection = connect(host=url)
            database_connection.server_info()
    except ServerSelectionTimeoutError as connection_error:
        print connection_error
        sys.exit(1)
    return database_connection

