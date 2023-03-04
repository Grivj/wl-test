from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.repository.team import TeamRepository
from app.schema.employee import Employee, EmployeeCreate

router = APIRouter()


@router.get("/{employee_id}", response_model=Employee | None)
def get_employee(
    session: Session = Depends(get_db), *, employee_id: UUID
) -> Employee | None:
    return EmployeeRepository.get_schema_by_id(
        session=session, id=employee_id, response_schema=Employee
    )


@router.post("/", response_model=Employee)
def create_employee(session: Session = Depends(get_db), *, employee: EmployeeCreate):
    return Employee.from_orm(
        EmployeeRepository.create(session=session, obj_in=employee.dict())
    )


@router.put("/{employee_id}/team", status_code=204)
def add_employee_to_team(
    session: Session = Depends(get_db), *, employee_id: UUID, team_id: UUID
):
    try:
        TeamRepository.add_employee(session, team_id, employee_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {"message": f"Employee {employee_id} added to team {team_id}"}


@router.delete("/{employee_id}/team", status_code=204)
def remove_employee_from_team(session: Session = Depends(get_db), *, employee_id: UUID):
    try:
        TeamRepository.remove_employee(session, employee_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {"message": "Removed team"}
