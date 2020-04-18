import logging
import sys

def create_logger(name: str, level=logging.DEBUG, stream=sys.stdout) -> logging.Logger:
    """
    Creates Logger.

    :param name: name of the logger
    :param level: logging level
    :param stream: stream to pass logs to

    :return: Logger
    """

    logger = logging.getLogger(name=name)
    logger.setLevel(level)

    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger