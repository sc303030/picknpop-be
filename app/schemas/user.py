from pydantic import BaseModel


class User(BaseModel):
    username: str
    nickname: str
    avatar: str

    class Config:
        orm_mode = True
