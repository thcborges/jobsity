from psycopg2.extensions import connection, cursor

from jobsity.core.helpers.query import QueryFactory
from jobsity.core.service.database import with_connected_database


class TripsDlo:
    @staticmethod
    @with_connected_database('postgres')
    def insert_trip(
        connection: connection, cursor: cursor, data: dict[str, str]
    ):
        query = QueryFactory('insert_trip').get()
        cursor.execute(query, data)
        connection.commit()
