from pydantic import BaseModel


class User(BaseModel):
    id: int
    nickname: str
    avatar: str

    class Config:
        from_attributes = True
