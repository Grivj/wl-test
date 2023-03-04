from uuid import UUID

from pydantic import BaseModel


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    ...


class Team(TeamBase):
    id: UUID

    class Config:
        orm_mode = True
