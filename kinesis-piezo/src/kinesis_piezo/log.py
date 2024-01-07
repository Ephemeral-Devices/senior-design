"""
created by nikos at 5/2/21
"""
import logging

from .config import LOG_LEVEL, PROJECT_NAME

_LOG_LEVELS = {
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}

root = logging.getLogger(PROJECT_NAME.lower())
root.propagate = False
root.setLevel(logging.DEBUG)
logging_format = [
    # '[%(asctime)s]',
    "{%(filename)s:%(lineno)d}",
    "%(name)s",
    "%(threadName)s",
    "%(levelname)s",
    "-",
    "%(message)s",
]
formatter = logging.Formatter(" ".join(logging_format))

loggers = {}


# noinspection PyPep8Naming
def get_log(name):
    if loggers.get(name) is None:
        loggers[name] = logging.root.getChild(name)
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        loggers[name].addHandler(console)
    return loggers[name]


def set_log_level(level: str = None):
    lls = {*_LOG_LEVELS.keys()}
    assert LOG_LEVEL in lls, f"{LOG_LEVEL} not found in {[*_LOG_LEVELS]}."
    ll = (level or LOG_LEVEL).upper()
    assert ll in lls, f"{ll} not found in {[*_LOG_LEVELS]}."
    root.setLevel(_LOG_LEVELS[ll])