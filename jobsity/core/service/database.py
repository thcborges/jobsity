from functools import wraps

import psycopg2
import psycopg2.extensions
from decouple import config

from jobsity.logging import get_logging

logging = get_logging(__name__)


def with_connected_database(database: str):
    def database_decorator(func):
        @wraps(func)
        def wrapper_connection(*args, **kwargs):
            uri, connector = {
                'postgres': (config('POSTGRES_URI'), psycopg2.connect)
            }.get(database)

            logging.info('Connecting to %s database', database)
            connection = connector(uri)
            cursor = connection.cursor()

            value = func(connection, cursor, *args, **kwargs)

            logging.info('Closing connection to %s', database)
            cursor.close()
            connection.close()

            return value

        return wrapper_connection

    return database_decorator
