from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.user import User
from app.schemas.team import TeamResponse


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    team_ids: List[int]


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    team_ids: Optional[List[int]] = None

    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    author: User
    created_at: datetime
    updated_at: datetime
    views: int

    class Config:
        from_attributes = True


class PostCreateResponse(Post):
    comment_count: int = 0
    emotion_count: int = 0

    class Config:
        from_attributes = True


class PostMain(Post):
    comment_count: int
    emotion_count: int

    class Config:
        from_attributes = True


class PostResponse(Post):
    teams: List[TeamResponse]

    class Config:
        from_attributes = True


class PostViewLog(PostBase):
    post_id: int
    recent_views: int

    class Config:
        from_attributes = True
