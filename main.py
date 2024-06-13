from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Union
from dotenv import load_dotenv
import os, sys

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import models, database
from routers import posts


# load_dotenv()
#
# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = "HS256"
#
# app = FastAPI()
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# class TokenData(BaseModel):
#     username: Union[str, None] = None
#
#
# def verify_token(token: str):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("username")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     return token_data
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     return verify_token(token)
#
#
# @app.post("/protected/")
# async def protected_post(
#     data: dict, current_user: TokenData = Depends(get_current_user)
# ):
#     return {
#         "message": "This is a protected POST endpoint",
#         "user": current_user.username,
#     }


models.Base.metadata.create_all(bind=database.engine)

apps = FastAPI()

apps.include_router(posts.router, prefix="", tags=["posts"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(apps, host="0.0.0.0", port=18000)
