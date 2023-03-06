from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_team_by_id
from app.db.session import get_db
from app.model import TeamModel
from app.repository.team import TeamRepository
from app.schema.employee import Employee
from app.schema.team import Team, TeamCreate

router = APIRouter()


@router.get("/{team_id}", response_model=Team | None)
async def get_team(team: TeamModel = Depends(get_team_by_id)) -> Team | None:
    return Team.from_orm(team)


@router.get("/{team_id}/employees", response_model=list[Employee])
async def get_team_employees(
    team: TeamModel = Depends(get_team_by_id),
) -> list[Employee]:
    return [Employee.from_orm(model) for model in team.employees]


@router.post("/", response_model=Team)
async def create_team(session: Session = Depends(get_db), *, team: TeamCreate) -> Team:
    """Create a new team if it doesn't exist already"""
    if TeamRepository.get_by_name(session, team.name):
        raise HTTPException(status_code=400, detail=f"Team {team.name} already exists")
    return Team.from_orm(TeamRepository.create(session=session, obj_in=team.dict()))


@router.get("/by_name/{name}", response_model=Team | None)
async def get_team_by_name(
    session: Session = Depends(get_db), *, name: str
) -> Team | None:
    """Get a team by name if it exists"""
    if model := TeamRepository.get_by_name(session=session, name=name):
        return Team.from_orm(model)
