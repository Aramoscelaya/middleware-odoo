import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name="middleware", logfile="logs/sync.log"):
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    fh = RotatingFileHandler(logfile, maxBytes=2_000_000, backupCount=5)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger
