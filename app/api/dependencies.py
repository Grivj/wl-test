from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.model import BalanceModel, EmployeeModel, TeamModel, VacationModel
from app.repository.balance import BalanceRepository
from app.repository.employee import EmployeeRepository
from app.repository.team import TeamRepository
from app.repository.vacation import VacationRepository
from app.service.employee import EmployeeService


async def get_employee_repository() -> EmployeeRepository:
    """Returns an instance of the employee repository."""
    return EmployeeRepository(EmployeeModel)


async def get_balance_repository() -> BalanceRepository:
    """Returns an instance of the balance repository."""
    return BalanceRepository(BalanceModel)


async def get_employee_service(
    db: Session = Depends(get_db),
    employee_repository: EmployeeRepository = Depends(get_employee_repository),
    balance_repository: BalanceRepository = Depends(get_balance_repository),
) -> EmployeeService:
    """Returns an instance of the employee service."""
    return EmployeeService(
        session=db,
        repository=employee_repository,
        balance_repository=balance_repository,
    )


async def get_employee_by_id(
    *,
    employee_service: EmployeeService = Depends(get_employee_service),
    employee_id: UUID,
) -> EmployeeModel:
    return employee_service.get_employee(employee_id)


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
