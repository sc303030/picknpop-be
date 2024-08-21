from typing import List, Optional

from pydantic import BaseModel


class EmotionTypeBase(BaseModel):
    name: str
    description: Optional[str] = None


class EmotionType(EmotionTypeBase):
    id: int

    class Config:
        from_attributes = True


class EmotionBase(BaseModel):
    id: int
    user_id: int
    post_id: int
    emotion_type_id: int

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


class EmotionResponse(BaseModel):
    emotion_type_id: int
    count: int


class UserEmotionStatus(BaseModel):
    emotion_type_id: int
    voted: bool


class ToggleEmotion(BaseModel):
    emotion_type_id: int
