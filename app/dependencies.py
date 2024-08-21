# dependencies.py
from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.jwt_token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    request: Request, token: Optional[str] = Depends(oauth2_scheme)
) -> Optional[int]:
    if token is None or "Authorization" not in request.headers:
        return None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        return verify_token(token, credentials_exception)
    except JWTError:
        raise credentials_exception
