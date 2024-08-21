from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.schemas import emotion as emotion_schema
from app.api import crud
from app.db.database import get_db
from app.dependencies import get_current_user

router = APIRouter()


@router.get("/types", response_model=list[emotion_schema.EmotionType])
def read_emotion_types(skip: int = 0, db: Session = Depends(get_db)):
    emotion_types = crud.get_emotion_types(db, skip=skip)
    return emotion_types


@router.post("/posts/{post_id}/toggle_emotion", response_model=dict)
def toggle_user_emotion(
    post_id: int,
    emotion_type: emotion_schema.ToggleEmotion,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.toggle_emotion(
        db=db,
        user_id=user_id,
        post_id=post_id,
        emotion_type_id=emotion_type.emotion_type_id,
    )


@router.get(
    "/posts/{post_id}/counts",
    response_model=list[emotion_schema.EmotionResponse],
)
def get_emotion_counts(post_id: int, db: Session = Depends(get_db)):
    return crud.get_emotion_counts_by_post(db=db, post_id=post_id)


@router.get(
    "/posts/{post_id}/user_emotions",
    response_model=list[emotion_schema.UserEmotionStatus],
)
def get_user_emotion_status(
    post_id: int,
    db: Session = Depends(get_db),
    user_id: Optional[int] = Depends(get_current_user),
):
    return crud.get_user_emotion_status(db=db, user_id=user_id, post_id=post_id)
