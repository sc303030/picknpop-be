from datetime import datetime

from pydantic import BaseModel

from app.schemas.user import User


class PostBase(BaseModel):
    id: int
    title: str
    content: str


class PostCreate(PostBase):
    team_id: int


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    author: User
    team_id: int
    created_at: datetime
    updated_at: datetime
    views: int

    class Config:
        from_attributes = True


class PostViewLogBase(PostBase):
    recent_views: int

    class Config:
        from_attributes = True
