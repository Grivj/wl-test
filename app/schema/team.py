from uuid import UUID

from pydantic import BaseModel


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    ...


class TeamUpdate(BaseModel):
    name: str | None = None


class TeamInDB(TeamBase):
    id: UUID

    class Config:
        orm_mode = True


class Team(TeamInDB):
    ...
