import os

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import team as team_schema
from app.db.database import get_db
from app.api import crud

router = APIRouter()

DJANGO_MEDIA_URL = os.getenv("DJANGO_MEDIA_URL")


@router.get("/", response_model=List[team_schema.Team])
def read_teams(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    teams = crud.get_teams(db, skip=skip, limit=limit)
    for team in teams:
        team.emblem = f"{DJANGO_MEDIA_URL}/{team.emblem}"
    return teams


@router.get("/{team_id}/posts")
def read_posts_by_team(team_id: int, db: Session = Depends(get_db)):
    posts = crud.get_posts_by_team(db, team_id=team_id)
    if posts is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return posts
