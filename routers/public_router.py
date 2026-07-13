from fastapi import APIRouter, Depends 

from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.ext.asyncio import AsyncSession 

from database import get_db 
from repository.user_repository import UserRepository
from services.auth_services import AuthService

from schemas.user_schema import (
    UserRegister,
    UserLogin,
)

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
):

    logger.info(
        "Received registration request for user '%s'.",
        user_data.username,
    )

    repository = UserRepository(db)
    service = AuthService(repository)

    response = await service.register_user(user_data)

    logger.info(
        "Registration request completed for user '%s'.",
        user_data.username,
    )

    return response


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):

    logger.info(
        "Received login request for user '%s'.",
        form_data.username,
    )

    repository = UserRepository(db)
    service = AuthService(repository)

    user_data = UserLogin(
        username=form_data.username,
        password=form_data.password,
    )

    response = await service.login_user(user_data)

    logger.info(
        "Login request completed for user '%s'.",
        form_data.username,
    )

    return response