import logging
from logging.handlers import RotatingFileHandler


def init():
    log_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s\t%(funcName)s(%(lineno)d) %(message)s')
    log_file = "log.txt"
    my_handler = RotatingFileHandler(log_file, mode='a', maxBytes=100 * 1024,
                                     backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    app_log = logging.getLogger('root')
    app_log.setLevel(logging.INFO)

    app_log.addHandler(my_handler)
