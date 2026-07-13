from pydantic import BaseModel,field_validator,EmailStr,Field
import re
    
import logging

logger = logging.getLogger(__name__)

class UserRegister(BaseModel):

    username: str = Field(min_length=3,max_length=30)

    email: EmailStr

    password: str = Field(min_length=8,max_length=32)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value): #what happened to cls and what is value 

        value = value.strip()

        if not value:
            raise ValueError("Username cannot be empty.")

        return value
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        password = value 

        if not re.search(r"[A-Z]", password):
            raise ValueError(
            "Password must contain at least one uppercase letter."
        )

        if not re.search(r"[a-z]", password):
            raise ValueError(
            "Password must contain at least one lowercase letter."
        )

        if not re.search(r"\d", password):
            raise ValueError(
            "Password must contain at least one digit."
        )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError(
            "Password must contain at least one special character."
        )

        return value
class UserLogin(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):

    user_id: int

    username: str

    email: EmailStr

    role: str
class UserUpdate(BaseModel):

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=30,
    )

    email: EmailStr | None = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):

        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Username cannot be empty.")

        return value
class UserRoleUpdate(BaseModel):

    role: str

    @field_validator("role")
    @classmethod
    def validate_role(cls, value):

        value = value.upper()

        if value not in ["USER", "ADMIN"]:
            raise ValueError(
                "Role must be either USER or ADMIN."
            )

        return value
class TokenResponse(BaseModel):

    access_token: str

    token_type: str