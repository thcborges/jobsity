from csv import DictReader

from tqdm import tqdm

from jobsity.app.app import App
from jobsity.core.helpers.path import DATA_PATH
from jobsity.core.service.kafka import get_producer


class ReadTripsApp(App):
    __source_file = DATA_PATH / 'input' / 'trips.csv'
    __topic = 'trips'

    def _send_data(self):
        producer = get_producer()
        with open(self.__source_file, newline='') as file:
            reader = DictReader(file)
            try:
                for row in tqdm(reader):
                    producer.send(self.__topic, row)
            except KeyboardInterrupt:
                producer.flush()
        producer.flush()
        producer.close()

    def run(self):
        self._send_data()
