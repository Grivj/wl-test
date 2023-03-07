from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_employee_by_id,
    get_employee_service,
    get_team_by_id,
)
from app.db.session import get_db
from app.model import EmployeeModel, TeamModel
from app.repository.balance import BalanceRepository
from app.repository.employee import EmployeeRepository
from app.schema.balance import Balance
from app.schema.employee import Employee, EmployeeCreate
from app.service.employee import EmployeeService

router = APIRouter()


@router.get("/{employee_id}", response_model=Employee)
async def get_employee(employee: EmployeeModel = Depends(get_employee_by_id)):
    return employee


@router.get("/{employee_id}/balance", response_model=Balance | None)
async def get_employee_balance(
    session: Session = Depends(get_db),
    employee: EmployeeModel = Depends(get_employee_by_id),
) -> Balance | None:
    if not (balance := BalanceRepository.get_by_employee_id(session, employee.id)):
        return
    return Balance.from_orm(balance)


@router.post("/", response_model=Employee)
async def create_employee(
    *,
    employee_service: EmployeeService = Depends(get_employee_service),
    employee_create: EmployeeCreate,
    balance_amount: int = 10,
):
    """Create a new employee with a vacation balance assigned to it"""
    return employee_service.create_employee(
        employee_create=employee_create, balance_amount=balance_amount
    )


@router.put("/{employee_id}/team", status_code=status.HTTP_200_OK)
async def add_employee_to_team(
    session: Session = Depends(get_db),
    *,
    employee: EmployeeModel = Depends(get_employee_by_id),
    team: TeamModel = Depends(get_team_by_id),
):
    EmployeeRepository.update_team(session, employee, team)
    return {"message": f"Employee {employee.id} joined the team {team.name}"}


@router.delete("/{employee_id}/team", status_code=status.HTTP_200_OK)
async def remove_employee_from_team(
    session: Session = Depends(get_db),
    *,
    employee: EmployeeModel = Depends(get_employee_by_id),
):
    EmployeeRepository.remove_team(session, employee)
    return {"message": f"Employee {employee.id} left the team"}


@router.delete("/{employee_id}", status_code=status.HTTP_200_OK)
async def delete_employee(
    *,
    employee_service: EmployeeService = Depends(get_employee_service),
    employee: EmployeeModel = Depends(get_employee_by_id),
):
    employee_service.delete_employee(employee)
    return {"message": f"Employee {employee.id} deleted"}
