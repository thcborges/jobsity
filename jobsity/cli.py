import traceback

import click

from jobsity import (
    FakeTripsApp,
    LoadTripsApp,
    ReadTripsApp,
    TripsByBoundingBoxApp,
    TripsByRegionApp,
)
from jobsity.logging import config_logger, get_logging

logging = get_logging(__name__)


@click.group()
def main():
    config_logger()


def run(App, *args, **kwargs):
    try:
        App(*args, **kwargs).run()
    except BaseException as error:
        logging.error(str(error))
        logging.error(traceback.format_exc())


@main.command()
def read_trips():
    logging.info('Read trips')
    run(ReadTripsApp)


@main.command()
def fake_trips():
    logging.info('Fake trips')
    run(FakeTripsApp)


@main.command()
def load_trips():
    logging.info('Load trips')
    run(LoadTripsApp)


@main.command()
@click.argument('bounding_box')
def trips_by_bounding_box(bounding_box):
    """
    Show weekly average number of trips of a bounding box.

    BOUNDING_BOX is used to filter the table bounding box.
    """
    logging.info('Trips by bounding box %s', bounding_box)
    print(bounding_box)
    run(TripsByBoundingBoxApp, bounding_box)


@main.command()
@click.argument('region')
def trips_by_region(region):
    """
    Show weekly average number of trips of a region.

    REGION is used to filter the table region.
    """
    logging.info('Trips by region %s', region)
    run(TripsByRegionApp, region)
