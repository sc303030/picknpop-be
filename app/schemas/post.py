from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
