from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import User


class CommentBase(BaseModel):
    message: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    author: User
    post_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
