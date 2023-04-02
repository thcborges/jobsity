from psycopg2.extensions import cursor

from jobsity.core.helpers.query import QueryFactory
from jobsity.core.service.database import with_connected_database


class TripsDao:
    @staticmethod
    @with_connected_database('postgres')
    def get_trips_by_region(
        _, cursor: cursor, region: str
    ) -> list[dict[str, any]]:
        HEADER = ['region', 'week_average_trips']
        query = QueryFactory('trips_by_region').get()
        cursor.execute(query, (region,))
        return [
            {column: data for column, data in zip(HEADER, line)}
            for line in cursor.fetchall()
        ]

    @staticmethod
    @with_connected_database('postgres')
    def get_trips_by_bounding_box(
        _, cursor: cursor, bounding_box: str
    ) -> list[dict[str, any]]:
        HEADER = ['bounding_box', 'week_average_trips']
        query = QueryFactory(
            'trips_by_bounding_box', bounding_box=bounding_box
        ).get()
        cursor.execute(query)
        return [
            {column: data for column, data in zip(HEADER, line)}
            for line in cursor.fetchall()
        ]
