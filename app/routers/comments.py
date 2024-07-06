from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import models
from app.db.database import get_db
from app.dependencies import get_current_user
from app.schemas import comment as comment_schema
from app.api.crud import create_comment, get_comments

router = APIRouter()


@router.post("/posts/{post_id}/", response_model=comment_schema.Comment)
def create_comment_for_post(
    post_id: int,
    comment: comment_schema.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return create_comment(
        db=db, comment=comment, user_id=current_user.id, post_id=post_id
    )


@router.get("/posts/{post_id}/", response_model=List[comment_schema.Comment])
def read_comments_for_post(
    post_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    comments = get_comments(db, post_id=post_id, skip=skip, limit=limit)
    return comments
