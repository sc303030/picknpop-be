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
