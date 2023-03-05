from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.model import EmployeeModel, TeamModel, VacationModel
from app.repository.employee import EmployeeRepository
from app.repository.team import TeamRepository
from app.repository.vacation import VacationRepository


def get_employee_by_id(
    db: Session = Depends(get_db), *, employee_id: UUID
) -> EmployeeModel:
    """Returns an employee by id or raises an HTTPException if not found."""
    if not (employee := EmployeeRepository.get_by_id(db, employee_id)):
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


def get_team_by_id(db: Session = Depends(get_db), *, team_id: UUID) -> TeamModel:
    """Returns a team by id or raises an HTTPException if not found."""
    if not (team := TeamRepository.get_by_id(db, team_id)):
        raise HTTPException(status_code=404, detail="Team not found")
    return team


def get_vacation_by_id(
    db: Session = Depends(get_db), *, vacation_id: UUID
) -> VacationModel:
    """Returns a vacation by id or raises an HTTPException if not found."""
    if not (vacation := VacationRepository.get_by_id(db, vacation_id)):
        raise HTTPException(status_code=404, detail="Vacation not found")
    return vacation
