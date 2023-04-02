from csv import DictReader
from random import randint

from decouple import config
from tqdm import tqdm

from jobsity.app.app import App
from jobsity.core.helpers.path import DATA_PATH
from jobsity.core.service.kafka import get_producer


class FakeTripsApp(App):
    __source_file = DATA_PATH / 'input' / 'trips.csv'
    __topic = 'trips'
    __total_trips = config('TRIPS_TOTAL', cast=int, default=100_000_000)

    def _read_file(self) -> list[dict[str, str]]:
        with open(self.__source_file, newline='') as file:
            reader = DictReader(file)
            rows = [row for row in reader]
        return rows

    def _get_message(self, data: list[dict[str, str]]):
        index = randint(0, len(data) - 1)
        return data[index]

    def _send_data(self, data: list[dict[str, str]]):
        producer = get_producer()
        try:
            for _ in tqdm(range(self.__total_trips)):
                message = self._get_message(data)
                producer.send(self.__topic, message)
        except KeyboardInterrupt:
            producer.flush()
        producer.close()

    def run(self):
        data = self._read_file()
        self._send_data(data)
