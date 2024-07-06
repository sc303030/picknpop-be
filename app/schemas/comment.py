from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CommentBase(BaseModel):
    message: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
