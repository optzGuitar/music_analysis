import logging
from pathlib import Path

LOG_BASEPATH = Path(__file__).joinpath('./logs').resolve()

def make_logger(name: str) -> logging.Logger:
    log_ = logging.getLogger(name)
    format = logging.Formatter('[%(asctime)s].[%(levelname)s][%(module)s][%(funcName)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(str(LOG_BASEPATH.joinpath(f"./{name}.log")))
    handler.setFormatter(format)
    log_.addHandler(log_)
    return log_

main_logger = make_logger('composer')
cleanup_log = make_logger('cleanup')
miner_log = make_logger('miner')
