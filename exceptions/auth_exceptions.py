import logging

logger = logging.getLogger(__name__)

class UserAlreadyExistsException(Exception):
    pass


class EmailAlreadyExistsException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass