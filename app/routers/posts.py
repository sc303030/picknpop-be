import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.crud import update_post, delete_post
from app.db.database import get_db
from app.dependencies import get_current_user
from app.schemas import post as post_schema
from app.api import crud

router = APIRouter()


@router.post("/", response_model=post_schema.PostCreateResponse)
def create_post(
    post: post_schema.PostCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return crud.create_post(db=db, post=post, user_id=user_id)


@router.get("/", response_model=List[post_schema.PostMain])
def read_posts(skip: int = 0, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip)
    return posts


@router.get("/popular", response_model=List[post_schema.PostViewLog])
def get_popular_posts(db: Session = Depends(get_db)):
    return crud.get_popular_posts(db)


@router.get("/{post_id}", response_model=post_schema.PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db=db, post_id=post_id)
    crud.increment_post_views(db, db_post)
    return db_post


@router.put("/{post_id}")
def update_post_route(
    post_id: int, post_update: post_schema.PostUpdate, db: Session = Depends(get_db)
):
    return update_post(db=db, post_id=post_id, post_update=post_update)


@router.patch("/{post_id}")
def delete_post_route(post_id: int, db: Session = Depends(get_db)):
    return delete_post(db=db, post_id=post_id)
