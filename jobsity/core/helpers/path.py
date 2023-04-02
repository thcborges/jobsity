from datetime import date
from pathlib import Path

from decouple import config

PROCESSED_FOLDER = '.processed'
DATA_PATH = Path(config('DATA_PATH'))


def get_root_path() -> Path:
    """Returns the root path to the package
    Returns:
        Path: root path to the package
    """
    return Path(__file__).parents[2]


def get_config_file(config: str) -> Path:
    root = get_root_path()

    config_file = {'logging': Path('conf/logging_custom.json')}.get(config)
    if not config_file:
        raise NotImplementedError(f'There is no config file for {config}')
    config_path = root / config_file
    return config_path


def get_logging_path() -> Path:
    root = get_root_path()
    today = date.today().strftime('%Y-%m-%d')
    logging_path = root / 'log' / today

    logging_path.mkdir(parents=True, exist_ok=True)
    return logging_path


def set_processed_folder(path: Path | str) -> Path:
    return Path(path) / PROCESSED_FOLDER


def is_processed_path(path: Path | str) -> bool:
    return PROCESSED_FOLDER in Path(path).parts


def get_s3_uri(local_path: Path) -> str:
    S3_BUCKET = config('S3_BUCKET')
    s3_root = ROOT_PATH.parents[1]
    s3_path = str(local_path).replace(str(s3_root), S3_BUCKET)
    return s3_path


ROOT_PATH = get_root_path()
QUERY_PATH = ROOT_PATH / 'core' / 'sql'
