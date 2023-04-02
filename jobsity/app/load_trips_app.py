import re
from datetime import datetime
from time import sleep

from jobsity.app.app import App
from jobsity.core.dlo.trips_dlo import TripsDlo
from jobsity.core.service.kafka import kafka_consumer
from jobsity.logging import get_logging

logging = get_logging(__name__)


class LoadTripsApp(App):
    @staticmethod
    def _to_datetime(message: dict[str, str]) -> dict[str, str | datetime]:
        DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        message['datetime'] = datetime.strptime(
            message.get('datetime'), DATETIME_FORMAT
        )
        return message

    @staticmethod
    def _convert_point(point: str) -> str:
        REGEX = r'POINT\s?\((\d+\.?\d*),?\s?(\d+\.?\d*)\)'
        match = re.match(REGEX, point)
        return f'({match.group(1)}, {match.group(2)})'

    def _convert_points(self, message: dict[str, str]) -> dict[str, str]:
        message['origin_coord'] = self._convert_point(
            message.get('origin_coord', '')
        )
        message['destination_coord'] = self._convert_point(
            message.get('destination_coord', '')
        )
        return message

    @kafka_consumer('trips', group_id='load_trip')
    def _get_data(message: dict[str, str], self):
        message = self._convert_points(message)
        message = self._to_datetime(message)
        logging.info('Inserting %s on the database', str(message))
        TripsDlo.insert_trip(message)

    def run(self):
        sleep(30)
        self._get_data()
