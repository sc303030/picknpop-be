import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.dependencies import get_current_user
from app.schemas import post as post_schema
from app.api import crud

router = APIRouter()


@router.post("/", response_model=post_schema.Post)
def create_post(
    post: post_schema.PostCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return crud.create_post(db=db, post=post, user_id=user_id)


@router.get("/", response_model=List[post_schema.Post])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@router.get("/popular", response_model=List[post_schema.PostViewLog])
def get_popular_posts(db: Session = Depends(get_db)):
    return crud.get_popular_posts(db)


@router.get("/{post_id}", response_model=post_schema.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    crud.increment_post_views(db, db_post)
    return db_post


@router.put("/{post_id}", response_model=post_schema.Post)
def update_post(
    post_id: int, post: post_schema.PostUpdate, db: Session = Depends(get_db)
):
    db_post = crud.update_post(db=db, post_id=post_id, post=post)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
