import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

LOGPATH = Path(__file__).parent.joinpath('./logs').resolve()
os.makedirs(LOGPATH, exist_ok=True)

def make_logger(name: str):
    path = os.path.join(LOGPATH, f'{name}.log')

    logger = logging.getLogger(name)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(module)s][%(funcName)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = RotatingFileHandler(
        path,
        mode="a",
        maxBytes=50 * 1024,
        backupCount=1,
        encoding=None,
        delay=False,
    )
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger

main_logger = make_logger('composer')
cleanup_log = make_logger('cleanup')
miner_log = make_logger('miner')
