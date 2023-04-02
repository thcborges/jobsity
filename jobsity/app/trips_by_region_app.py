from jobsity.app.app import App
from jobsity.core.dao import TripsDao
from jobsity.core.helpers.show_data import show_list_dict


class TripsByRegionApp(App):
    def __init__(self, region: str) -> None:
        super().__init__()
        self.region = region

    def get_data(self) -> list[dict[str, any]]:
        return TripsDao.get_trips_by_region(self.region)

    def run(self):
        data = self.get_data()
        show_list_dict(data)
