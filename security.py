#hashed password 
from passlib.context import CryptContext
from datetime import datetime, timezone,timedelta
from jose import JWTError,jwt

from dotenv import load_dotenv
import os 
load_dotenv()


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

#verify password 
def verify_password(password:str, hashed_password:str)->bool:
    return pwd_context.verify(
       password, hashed_password
    )

    #jwt token create 
def create_access_token(data: dict):
 
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({"exp": expire})

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

import logging

logger = logging.getLogger(__name__)

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError as e:
        logger.exception("JWT verification failed")
        print(e)          # temporary
        return None
