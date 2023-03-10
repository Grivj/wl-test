from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_employee_by_id, get_team_by_id
from app.db.session import get_db
from app.model import EmployeeModel, TeamModel
from app.repository.balance import BalanceRepository
from app.repository.employee import EmployeeRepository
from app.schema.balance import Balance
from app.schema.employee import Employee, EmployeeCreate
from app.service.employee import EmployeeService

router = APIRouter()


@router.get("/{employee_id}", response_model=Employee | None)
def get_employee(
    employee: EmployeeModel = Depends(get_employee_by_id),
) -> Employee | None:
    return Employee.from_orm(employee)


@router.get("/{employee_id}/balance", response_model=Balance | None)
def get_employee_balance(
    session: Session = Depends(get_db),
    employee: EmployeeModel = Depends(get_employee_by_id),
) -> Balance | None:
    if not (balance := BalanceRepository.get_by_employee_id(session, employee.id)):
        return
    return Balance.from_orm(balance)


@router.post("/", response_model=Employee)
def create_employee(
    session: Session = Depends(get_db),
    *,
    employee: EmployeeCreate,
    balance_amount: int = 10,
):
    """Create a new employee with a vacation balance assigned to it"""
    employee_model = EmployeeService.create_with_balance(
        session=session, employee_create=employee, balance_amount=balance_amount
    )
    return Employee.from_orm(employee_model)


@router.put("/{employee_id}/team", status_code=status.HTTP_200_OK)
def add_employee_to_team(
    session: Session = Depends(get_db),
    *,
    employee: EmployeeModel = Depends(get_employee_by_id),
    team: TeamModel = Depends(get_team_by_id),
):
    EmployeeRepository.update_team(session, employee, team)
    return {"message": f"Employee {employee.id} joined the team {team.name}"}


@router.delete("/{employee_id}/team", status_code=status.HTTP_200_OK)
def remove_employee_from_team(
    session: Session = Depends(get_db),
    *,
    employee: EmployeeModel = Depends(get_employee_by_id),
):
    EmployeeRepository.remove_team(session, employee)
    return {"message": f"Employee {employee.id} left the team"}


@router.delete("/{employee_id}", status_code=status.HTTP_200_OK)
def delete_employee(
    session: Session = Depends(get_db),
    *,
    employee: EmployeeModel = Depends(get_employee_by_id),
):
    EmployeeRepository.delete(session, employee)
    return {"message": "Deleted employee"}
