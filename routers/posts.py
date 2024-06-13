from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import crud
from db import database
from schemas import post as post_schema

router = APIRouter()


@router.post("/posts/", response_model=post_schema.Post)
def create_post(post: post_schema.PostCreate, db: Session = Depends(database.get_db)):
    return crud.create_post(db=db, post=post)


@router.get("/posts/", response_model=List[post_schema.Post])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_posts(db=db, skip=skip, limit=limit)


@router.get("/posts/{post_id}", response_model=post_schema.Post)
def read_post(post_id: int, db: Session = Depends(database.get_db)):
    db_post = crud.get_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put("/posts/{post_id}", response_model=post_schema.Post)
def update_post(
    post_id: int, post: post_schema.PostUpdate, db: Session = Depends(database.get_db)
):
    db_post = crud.update_post(db=db, post_id=post_id, post=post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
