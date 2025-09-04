import logging

def setup_logging(level_name: str = "INFO"):
    level = getattr(logging, level_name.upper(), logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
    if level == logging.DEBUG:
        logging.getLogger("aiogram").setLevel(logging.DEBUG)

def get_logger(name: str):
    return logging.getLogger(name)
