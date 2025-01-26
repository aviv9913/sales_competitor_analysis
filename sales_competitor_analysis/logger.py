import logging
from logging import FileHandler
from math import log
from datetime import datetime
import os

logs_folder = "logs"
log_file_path = f"{logs_folder}/log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
os.makedirs(logs_folder, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler = FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
