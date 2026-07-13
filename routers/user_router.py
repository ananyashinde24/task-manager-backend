from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db

from models.User import User

from repository.user_repository import UserRepository
from services.user_service import UserService

from schemas.user_schema import (
    UserUpdate,
    UserRoleUpdate,
)

from dependencies.auth import (
    get_current_user,
    require_admin,
)

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/")
async def view_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):

    logger.info(
        "Received request to fetch all users."
    )

    repository = UserRepository(db)
    service = UserService(repository)

    response = await service.get_all_users()

    logger.info(
        "Fetch all users request completed."
    )

    return response


@router.get("/{user_id}")
async def view_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    logger.info(
        "Received request to fetch user with ID %d.",
        user_id,
    )

    repository = UserRepository(db)
    service = UserService(repository)

    response = await service.get_user_by_id(user_id)

    logger.info(
        "Fetch user request completed for user ID %d.",
        user_id,
    )

    return response


@router.patch("/{user_id}")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    logger.info(
        "Received request to update user with ID %d.",
        user_id,
    )

    repository = UserRepository(db)
    service = UserService(repository)

    updates = user_data.model_dump(exclude_unset=True)

    response = await service.update_user(
        user_id,
        updates,
    )

    logger.info(
        "Update user request completed for user ID %d.",
        user_id,
    )

    return response


@router.patch("/{user_id}/role")
async def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):

    logger.warning(
        "Received request to change role of user %d to '%s'.",
        user_id,
        role_data.role,
    )

    repository = UserRepository(db)
    service = UserService(repository)

    response = await service.update_user_role(
        user_id,
        role_data.role,
    )

    logger.warning(
        "Role update request completed for user %d.",
        user_id,
    )

    return response


@router.delete("/{user_id}")
async def delete_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):

    logger.warning(
        "Received request to delete user with ID %d.",
        user_id,
    )

    repository = UserRepository(db)
    service = UserService(repository)

    response = await service.delete_user_by_id(user_id)

    logger.warning(
        "Delete user request completed for user ID %d.",
        user_id,
    )

    return response


@router.delete("/")
async def delete_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):

    logger.warning(
        "Received request to delete all users."
    )

    repository = UserRepository(db)
    service = UserService(repository)

    response = await service.delete_all_users()

    logger.warning(
        "Delete all users request completed."
    )

    return response