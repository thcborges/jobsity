import json
import logging
import logging.config

from decouple import config

from jobsity.core.helpers.path import get_config_file, get_logging_path


def config_logger():
    logging_path = get_logging_path()
    config_file = get_config_file('logging')
    logging_config = json.loads(config_file.read_text())

    for handler in logging_config.get('handlers').values():
        if handler.get('filename'):
            handler['filename'] = logging_path / handler['filename']

    logging_config['handlers']['console']['level'] = config(
        'LOGGING_LEVEL', 'ERROR'
    )

    logging.config.dictConfig(logging_config)


def get_logging(name) -> logging.Logger:
    return logging.getLogger(name)
