from pydantic import BaseModel


class User(BaseModel):
    nickname: str
    avatar: str

    class Config:
        from_attributes = True
