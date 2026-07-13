import logging
import os

from utils.log_filter import WarningErrorFilter

os.makedirs("logs", exist_ok=True)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

file_handler = logging.FileHandler("logs/app.log")
file_handler.setFormatter(formatter)

file_handler.addFilter(WarningErrorFilter())

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        file_handler,
        console_handler
    ],
    force=True
)


logger = logging.getLogger(__name__)