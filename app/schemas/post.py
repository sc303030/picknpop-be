from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import User


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    team_id: int


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    author: User
    team_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
