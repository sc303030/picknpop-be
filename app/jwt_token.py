from typing import Optional

from dotenv import load_dotenv
from fastapi import HTTPException
from jose import jwt, JWTError
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def verify_token(token: str, credentials_exception: HTTPException) -> Optional[int]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return int(user_id)
