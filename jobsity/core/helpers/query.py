from pathlib import Path

from jobsity.core.helpers.path import QUERY_PATH
from jobsity.logging import get_logging

logging = get_logging(__name__)


class QueryFactory:
    __queries = {
        'insert_trip': QUERY_PATH / 'insert_trip.sql',
        'trips_by_region': QUERY_PATH / 'trips_by_region.sql',
        'trips_by_bounding_box': QUERY_PATH / 'trips_by_bounding_box.sql',
    }

    def __init__(self, query: str, **kwargs) -> None:
        self.__file: Path = self.__queries.get(query)
        self.__kwargs = kwargs
        logging.info('Getting %s query from %s file', query, self.__file)

    def get(self) -> str:
        if not self.__file.is_file():
            logging.error('Requested file %s does not exists', self.__file)
            raise FileNotFoundError(f'Query file "{self.__file} not found"')
        return self.__file.read_text().format(**self.__kwargs)
