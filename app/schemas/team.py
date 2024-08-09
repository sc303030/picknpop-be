from pydantic import BaseModel
from typing import Optional


class TeamBase(BaseModel):
    name: str
    league: str


class TeamCreate(TeamBase):
    emblem: Optional[str] = None


class TeamUpdate(TeamBase):
    emblem: Optional[str] = None


class Team(TeamBase):
    id: int
    emblem: Optional[str] = None

    class Config:
        from_attributes = True
