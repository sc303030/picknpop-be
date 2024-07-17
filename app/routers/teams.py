from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas import team as team_schema
from app.db.database import get_db
from app.api import crud

router = APIRouter()


@router.get("/", response_model=List[team_schema.Team])
def read_teams(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    teams = crud.get_teams(db, skip=skip, limit=limit)
    return teams
