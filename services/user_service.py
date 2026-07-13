from repository.user_repository import UserRepository

from security import (
    hash_password,
    verify_password,
)
import logging

logger = logging.getLogger(__name__)
from exceptions.auth_exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_all_users(self):

        return await self.repository.get_all_users()

    async def get_user_by_id(
        self,user_id: int,):

        return await self.repository.get_user_by_id(user_id)

    async def update_user(
        self,
        user_id: int,
        updates: dict,
    ):

        # Check if email is being updated
        if "email" in updates:

            existing_user = await self.repository.get_user_by_email(
                updates["email"]
            )

            if existing_user and existing_user.user_id != user_id:

                raise EmailAlreadyExistsException(
                    "Email already exists."
                )

        return await self.repository.update_user(
            user_id,
            updates,
        )

    async def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str,
    ):

        user = await self.repository.get_user_by_id(
            user_id
        )

        if not user:

            return None

        if not verify_password(
            old_password,
            user.hashed_password,
        ):

            raise InvalidCredentialsException(
                "Current password is incorrect."
            )

        hashed_password = hash_password(
            new_password
        )

        updates = {
            "hashed_password": hashed_password
        }

        return await self.repository.update_user(
            user_id,
            updates,
        )

    async def update_user_role(
        self,
        user_id: int,
        role: str,
    ):

        return await self.repository.update_user_role(
            user_id,
            role,
        )

    async def delete_user_by_id(
        self,
        user_id: int,
    ):

        return await self.repository.delete_user_by_id(
            user_id,
        )

    async def delete_all_users(self):

        return await self.repository.delete_all_users()