import os

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import team as team_schema
from app.db.database import get_db
from app.api import crud
from app.schemas import post as post_schema

router = APIRouter()


@router.get("/", response_model=List[team_schema.Team])
def read_teams(skip: int = 0, db: Session = Depends(get_db)):
    teams = crud.get_teams(db, skip=skip)
    return teams


@router.get("/{team_id}/posts", response_model=List[post_schema.PostMain])
def read_posts_by_team(team_id: int, db: Session = Depends(get_db)):
    posts = crud.get_posts_by_team(db, team_id=team_id)
    if posts is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return posts
