from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_employee_by_id, get_team_by_id
from app.db.session import get_db
from app.model import EmployeeModel, TeamModel
from app.repository.employee import EmployeeRepository
from app.schema.employee import Employee, EmployeeCreate

router = APIRouter()


@router.get("/{employee_id}", response_model=Employee | None)
def get_employee(
    employee: EmployeeModel = Depends(get_employee_by_id),
) -> Employee | None:
    return Employee.from_orm(employee)


@router.post("/", response_model=Employee)
def create_employee(session: Session = Depends(get_db), *, employee: EmployeeCreate):
    return Employee.from_orm(
        EmployeeRepository.create(session=session, obj_in=employee.dict())
    )


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
