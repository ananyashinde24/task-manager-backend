from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from repository.user_repository import UserRepository
from security import verify_token
from models.User import User

import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
    )

    logger.info("Authenticating user from JWT token.")

    payload = verify_token(token)

    if payload is None:
        logger.warning("Token verification failed.")
        raise credentials_exception

    username = payload.get("sub")

    if username is None:
        logger.warning("Token does not contain username.")
        raise credentials_exception

    logger.debug(
        "Fetching user '%s' from database.",
        username,
    )

    repository = UserRepository(db)

    user = await repository.get_user_by_username(username)

    if user is None:
        logger.warning(
            "User '%s' not found in database.",
            username,
        )
        raise credentials_exception

    logger.info(
        "User '%s' authenticated successfully.",
        username,
    )

    return user


async def require_admin(
    current_user: User = Depends(get_current_user),
):

    logger.info(
        "Checking admin privileges for user '%s'.",
        current_user.username,
    )

    if current_user.role != "ADMIN":

        logger.warning(
            "User '%s' attempted to access an admin endpoint.",
            current_user.username,
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    logger.info(
        "Admin access granted to user '%s'.",
        current_user.username,
    )

    return current_user