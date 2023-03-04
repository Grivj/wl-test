from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.schema.employee import Employee, EmployeeCreate

router = APIRouter()


@router.get("/{employee_id}", response_model=Employee | None)
def get_employee(session: Session = Depends(get_db), *, employee_id: UUID):
    return EmployeeRepository.get(session=session, id=employee_id)


@router.post("/", response_model=Employee)
def create_employee(session: Session = Depends(get_db), *, employee: EmployeeCreate):
    return EmployeeRepository.create(session=session, obj_in=employee.dict())
