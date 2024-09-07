from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.user import User


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    team_ids: List[int]


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    author: User
    created_at: datetime
    updated_at: datetime
    views: int

    class Config:
        from_attributes = True


class PostViewLog(PostBase):
    post_id: int
    recent_views: int

    class Config:
        from_attributes = True
