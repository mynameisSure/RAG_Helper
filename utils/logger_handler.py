import logging
from .path_tool import get_abs_path
import os
from datetime import datetime

LOG_ROOT = get_abs_path("logs")
os.makedirs(LOG_ROOT, exist_ok=True)

DEFAULT_LOG_FORMAT = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s-%(filename)s:%(lineno)d - %(message)s")


def get_logger(
        name: str = "agent",
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        log_file=None):
    logger=logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)

    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    file_hander=logging.FileHandler(log_file)
    file_hander.setLevel(file_level)
    file_hander.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_hander)
    return logger


logger = get_logger()
if __name__ == "__main__":
    logger.debug("debug message")
    logger.error("error message")
    logger.info("info message")
    logger.warning("warning message")

