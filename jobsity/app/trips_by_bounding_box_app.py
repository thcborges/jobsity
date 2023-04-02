from jobsity.app.app import App
from jobsity.core.dao import TripsDao
from jobsity.core.helpers.show_data import show_list_dict


class TripsByBoundingBoxApp(App):
    def __init__(self, bounding_box: str) -> None:
        super().__init__()
        self.bounding_box = bounding_box

    def get_data(self) -> list[dict[str, any]]:
        return TripsDao.get_trips_by_bounding_box(self.bounding_box)

    def run(self):
        data = self.get_data()
        print(data)
        show_list_dict(data)
