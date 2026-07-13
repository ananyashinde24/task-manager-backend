import logging


class WarningErrorFilter(logging.Filter):

    def filter(self, record):
        return record.levelno in (
            logging.WARNING,
            logging.ERROR
        )