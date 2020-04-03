import logging
import sys

def create_logger(name: str, level=logging.DEBUG, stream=sys.stdout) -> logging.Logger:
    root = logging.getLogger(name=name)
    root.setLevel(level)

    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    return root