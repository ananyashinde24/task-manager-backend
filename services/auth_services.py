from repository.user_repository import UserRepository
from models.User import User

from security import (
    verify_password,
    hash_password,
    create_access_token,
)

from schemas.user_schema import (
    UserRegister,
    UserLogin,
)

from exceptions.auth_exceptions import (
    UserAlreadyExistsException,
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)

import logging

logger = logging.getLogger(__name__)


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(
        self,
        user_data: UserRegister,
    ):

        logger.info(
            "Starting registration for user '%s'.",
            user_data.username,
        )

        existing_user = await self.repository.get_user_by_username(
            user_data.username
        )

        if existing_user:

            logger.warning(
                "Registration failed. Username '%s' already exists.",
                user_data.username,
            )

            raise UserAlreadyExistsException(
                "Username already exists."
            )

        existing_email = await self.repository.get_user_by_email(
            user_data.email
        )

        if existing_email:

            logger.warning(
                "Registration failed. Email already exists."
            )

            raise EmailAlreadyExistsException(
                "Email already exists."
            )

        logger.debug(
            "Hashing password for user '%s'.",
            user_data.username,
        )

        hashed_password = hash_password(
            user_data.password
        )

        logger.debug(
            "Password hashed successfully."
        )

        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        await self.repository.create_user(user)

        logger.info(
            "User '%s' registered successfully.",
            user.username,
        )

        return user

    async def login_user(
        self,
        user_data: UserLogin,
    ):

        logger.info(
            "Login attempt for user '%s'.",
            user_data.username,
        )

        user = await self.repository.get_user_by_username(
            user_data.username
        )

        if not user:

            logger.warning(
                "Login failed. User '%s' not found.",
                user_data.username,
            )

            raise InvalidCredentialsException(
                "Invalid username or password."
            )

        if not verify_password(
            user_data.password,
            user.hashed_password,
        ):

            logger.warning(
                "Login failed. Invalid password for user '%s'.",
                user_data.username,
            )

            raise InvalidCredentialsException(
                "Invalid username or password."
            )

        logger.debug(
            "Generating JWT token for user '%s'.",
            user.username,
        )

        access_token = create_access_token(
            {
                "sub": user.username,
                "role": user.role,
            }
        )

        logger.info(
            "User '%s' logged in successfully.",
            user.username,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }