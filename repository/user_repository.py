from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.User import User

import logging

logger = logging.getLogger(__name__)


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: User):

        logger.info(
            "Creating user '%s'.",
            user.username,
        )

        self.db.add(user)

        await self.db.commit()

        await self.db.refresh(user)

        logger.info(
            "User '%s' created successfully with ID %d.",
            user.username,
            user.user_id,
        )

        return user

    async def get_all_users(self):

        logger.debug("Fetching all users from database.")

        result = await self.db.execute(
            select(User)
        )

        users = result.scalars().all()

        logger.info(
            "Retrieved %d user(s) from database.",
            len(users),
        )

        return users

    async def get_user_by_id(
        self,
        user_id: int,
    ):

        logger.debug(
            "Fetching user with ID %d.",
            user_id,
        )

        result = await self.db.execute(
            select(User).where(
                User.user_id == user_id
            )
        )

        user = result.scalar_one_or_none()

        if user is None:

            logger.warning(
                "User with ID %d not found.",
                user_id,
            )

            return None

        logger.info(
            "User with ID %d retrieved successfully.",
            user_id,
        )

        return user

    async def get_user_by_username(
        self,
        username: str,
    ):

        logger.debug(
            "Fetching user '%s'.",
            username,
        )

        result = await self.db.execute(
            select(User).where(
                User.username == username
            )
        )

        user = result.scalar_one_or_none()

        if user is None:

            logger.warning(
                "User '%s' not found.",
                username,
            )

            return None

        logger.info(
            "User '%s' retrieved successfully.",
            username,
        )

        return user

    async def get_user_by_email(
        self,
        email: str,
    ):

        logger.debug(
            "Fetching user with email '%s'.",
            email,
        )

        result = await self.db.execute(
            select(User).where(
                User.email == email
            )
        )

        user = result.scalar_one_or_none()

        if user is None:

            logger.warning(
                "User with email '%s' not found.",
                email,
            )

            return None

        logger.info(
            "User with email '%s' retrieved successfully.",
            email,
        )

        return user

    async def update_user(
        self,
        user_id: int,
        updates: dict,
    ):

        logger.info(
            "Updating user with ID %d.",
            user_id,
        )

        user = await self.get_user_by_id(user_id)

        if user is None:
            return None

        logger.debug(
            "Applying updates %s to user %d.",
            updates,
            user_id,
        )

        for key, value in updates.items():

            if hasattr(user, key):
                setattr(user, key, value)

        await self.db.commit()

        await self.db.refresh(user)

        logger.info(
            "User with ID %d updated successfully.",
            user_id,
        )

        return user

    async def update_user_role(
        self,
        user_id: int,
        role: str,
    ):

        logger.info(
            "Updating role of user %d to '%s'.",
            user_id,
            role,
        )

        user = await self.get_user_by_id(user_id)

        if user is None:
            return None

        user.role = role

        await self.db.commit()

        await self.db.refresh(user)

        logger.info(
            "Role updated successfully for user %d.",
            user_id,
        )

        return user

    async def delete_user_by_id(
        self,
        user_id: int,
    ):

        logger.info(
            "Deleting user with ID %d.",
            user_id,
        )

        user = await self.get_user_by_id(user_id)

        if user is None:
            return None

        await self.db.delete(user)

        await self.db.commit()

        logger.info(
            "User with ID %d deleted successfully.",
            user_id,
        )

        return user

    async def delete_all_users(self):

        logger.warning(
            "Deleting all users from database."
        )

        result = await self.db.execute(
            select(User)
        )

        users = result.scalars().all()

        for user in users:
            await self.db.delete(user)

        await self.db.commit()

        logger.info(
            "Deleted %d user(s) successfully.",
            len(users),
        )

        return "All users deleted successfully."