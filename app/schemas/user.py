from pydantic import BaseModel


class User(BaseModel):
    nickname: str
    avatar: str

    class Config:
        orm_mode = True
